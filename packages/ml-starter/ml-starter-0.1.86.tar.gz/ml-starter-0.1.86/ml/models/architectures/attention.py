"""Defines self-attention modules.

You can implement a self-attention model using the built-in PyTorch module:

.. code-block:: python

    from torch import nn

    self.attn = nn.TransformerEncoder(
        nn.TransformerEncoderLayer(
            d_model=512,
            nhead=8,
            dim_feedforward=2048,
            dropout=0.1,
            activation='relu',
            batch_first=True,
        ),
        num_layers=6,
    )

However, when doing inference, you will end up recomputing a lot of previous
states. Instead, you can use the equivalent implementation in this file:

.. code-block:: python

    from ml.models.architectures.attention import TransformerEncoder, TransformerEncoderLayer

    self.attn = TransformerEncoder(
        TransformerEncoderLayer(
            d_model=512,
            nhead=8,
            dim_feedforward=2048,
            dropout=0.1,
            # activation='relu',  Always ReLU
            # batch_first=True,  Always batch first
            is_causal=is_causal,  # Additional argument to support causal attention
            use_rotary=use_rotary,  # Additional argument to support rotary embeddings
        ),
        num_layers=6,
    )

    x, state = self.attn(x, state)

This also eliminates the need to pass in an attention mask; instead, simply use
the ``is_causal`` argument to the ``forward`` method and it will automatically
apply the mask for you. This will default to the more performant PyTorch
attention implementation.
"""

import copy
import functools
from typing import TypeVar, cast

import torch
import torch.nn.functional as F
from torch import Tensor, nn

from ml.models.embeddings import apply_rotary_embeddings, get_rotary_embeddings


@functools.lru_cache(maxsize=1)
@torch.no_grad()
def get_causal_mask(tsz_q: int, tsz_k: int, device: torch.device, dtype: torch.dtype) -> Tensor:
    """Gets a causal attention mask.

    Args:
        tsz_q: The number of query timesteps.
        tsz_k: The number of key timesteps.
        device: The device to create the mask on.
        dtype: The data type to create the mask with.

    Returns:
        The causal attention mask, of shape ``(Tq, Tk)``.
    """
    attn_mask = torch.ones(tsz_q, tsz_k, device=device, dtype=torch.bool)
    attn_mask = attn_mask.tril(diagonal=0)
    attn_mask_fl = torch.zeros(tsz_q, tsz_k, device=device, dtype=dtype).masked_fill(~attn_mask, -float("inf"))
    return attn_mask_fl


class MultiheadAttention(nn.Module):
    """Defines a streamable multihead attention layer.

    This is a slightly modified implementation of ``nn.MultiheadAttention``
    that is built into PyTorch. The main difference is that this version
    supports streaming inference for causal attention, by passing in a
    state tuple that contains the previously projected key and value tensors.

    Parameters:
        embed_dim: The input and output embedding dimension.
        num_heads: The number of attention heads.
        dropout: The dropout probability, applied to the attention matrix.
        bias: Whether to include a bias term in the projection layers.
        kdim: The dimension of the key projection. Defaults to ``embed_dim``.
        vdim: The dimension of the value projection. Defaults to ``embed_dim``.
        gqa_factor: The GQA factor to use, meaning the ratio of the number of
            queries to the number of keys. Higher values will result in more
            queries than keys, which can speed up inference.

    Inputs:
        query: The query tensor, of shape ``(B, T, C)``.
        key: The key tensor, of shape ``(B, T, C)``.
        value: The value tensor, of shape ``(B, T, C)``.
        state: The previous key and value tensors, of shape
            ``(B * H, T', C // H)``, where ``T'`` is the number of previous
            timesteps and ``H`` is the number of attention heads. This is
            only supported if ``is_causal=True``.
        is_causal: Whether to apply a causal mask to the attention matrix.
            Note that the "mask" is only applied implicitly and isn't actually
            instantiated as a tensor.

    Outputs:
        output: The output tensor, of shape ``(B, T, C)``, along with the
            key and value state for the next timestep.
    """

    __constants__ = [
        "num_heads",
        "gqa_factor",
        "kv_num_heads",
        "dropout",
        "head_dim",
        "max_kv_cache_len",
        "embed_dim",
        "kv_embed_dim",
        "kdim",
        "vdim",
        "_qkv_same_embed_dim",
    ]

    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        dropout: float = 0.0,
        bias: bool = True,
        kdim: int | None = None,
        vdim: int | None = None,
        gqa_factor: int = 1,
        max_kv_cache_len: int | None = None,
    ) -> None:
        super().__init__()

        assert embed_dim % num_heads == 0, f"`{embed_dim=}` must be divisible by `{num_heads=}`"
        assert num_heads % gqa_factor == 0, f"`{num_heads=}` must be divisible by `{gqa_factor=}`"

        # Stores some constant values.
        self.num_heads = num_heads
        self.gqa_factor = gqa_factor
        self.kv_num_heads = num_heads // gqa_factor
        self.dropout = dropout
        self.head_dim = embed_dim // num_heads
        self.max_kv_cache_len = max_kv_cache_len

        self.embed_dim = embed_dim
        self.kv_embed_dim = self.kv_num_heads * self.head_dim
        self.kdim = kdim if kdim is not None else embed_dim
        self.vdim = vdim if vdim is not None else embed_dim
        self._qkv_same_embed_dim = self.kdim == embed_dim and self.vdim == embed_dim

        if not self._qkv_same_embed_dim:
            self.q_proj_weight = nn.Parameter(torch.empty((embed_dim, embed_dim)))
            self.k_proj_weight = nn.Parameter(torch.empty((self.kv_embed_dim, self.kdim)))
            self.v_proj_weight = nn.Parameter(torch.empty((self.kv_embed_dim, self.vdim)))
            self.register_parameter("in_proj_weight", None)
        else:
            self.in_proj_weight = nn.Parameter(torch.empty((embed_dim + 2 * self.kv_embed_dim, embed_dim)))
            self.register_parameter("q_proj_weight", None)
            self.register_parameter("k_proj_weight", None)
            self.register_parameter("v_proj_weight", None)

        if bias:
            self.in_proj_bias = nn.Parameter(torch.empty(embed_dim + 2 * self.kv_embed_dim))
        else:
            self.register_parameter("in_proj_bias", None)
        self.out_proj = nn.Linear(embed_dim, embed_dim, bias=bias)

        self._reset_parameters()

    def _reset_parameters(self) -> None:
        if self._qkv_same_embed_dim:
            nn.init.xavier_uniform_(self.in_proj_weight)
        else:
            nn.init.xavier_uniform_(self.q_proj_weight)
            nn.init.xavier_uniform_(self.k_proj_weight)
            nn.init.xavier_uniform_(self.v_proj_weight)

        if self.in_proj_bias is not None:
            nn.init.constant_(self.in_proj_bias, 0.0)
            nn.init.constant_(self.out_proj.bias, 0.0)

    def forward(
        self,
        query: Tensor,
        key: Tensor,
        value: Tensor,
        state: Tensor | None = None,
        is_causal: bool = False,
        rotary_q: Tensor | None = None,
        rotary_k: Tensor | None = None,
        mask: Tensor | None = None,
    ) -> tuple[Tensor, Tensor]:
        assert query.dim() == 3 and key.dim() == 3 and value.dim() == 3

        # Computes query, key, and value projections
        qkw_splits = (self.embed_dim, self.kv_embed_dim, self.kv_embed_dim)
        if self._qkv_same_embed_dim:
            qw, kw, vw = self.in_proj_weight.split(qkw_splits, dim=0)
        else:
            qw, kw, vw = self.q_proj_weight, self.k_proj_weight, self.v_proj_weight
        qb, kb, vb = (None, None, None) if self.in_proj_bias is None else self.in_proj_bias.split(qkw_splits, dim=0)

        xq = F.linear(query, qw, qb)
        xk = F.linear(key, kw, kb)
        xv = F.linear(value, vw, vb)

        # Permutes (B, T, G * H * C) -> (B, G, H, T, C)
        xq = xq.unflatten(-1, (self.gqa_factor, self.kv_num_heads, self.head_dim)).permute(0, 2, 3, 1, 4)
        xk = xk.unflatten(-1, (1, self.kv_num_heads, self.head_dim)).permute(0, 2, 3, 1, 4)
        xv = xv.unflatten(-1, (1, self.kv_num_heads, self.head_dim)).permute(0, 2, 3, 1, 4)

        # Applies rotary embeddings.
        if rotary_q is not None:
            xq = apply_rotary_embeddings(xq.flatten(0, 2), rotary_q).view(xq.shape)
        if rotary_k is not None:
            xk = apply_rotary_embeddings(xk.flatten(0, 2), rotary_k).view(xk.shape)

        # Concatenates previous states
        if state is not None:
            if is_causal:
                raise ValueError(
                    "Causal attention with state will lead to incorrect results. Instead, when unrolling the "
                    "attention component, set `is_causal=False` and pass samples one-at-a-time."
                )
            if query.shape[1] != 1:
                raise ValueError(
                    "Using a state implies that you are using causal attention, but you are passing multiple query "
                    "vectors. Instead, when unrolling the attention component, set `is_causal=False` and pass "
                    "samples one-at-a-time."
                )

            prev_k, prev_v = state.unbind(0)
            xk = torch.cat((prev_k, xk), dim=-2)
            xv = torch.cat((prev_v, xv), dim=-2)
            if self.max_kv_cache_len is not None:
                xk = xk[:, -self.max_kv_cache_len :]
                xv = xv[:, -self.max_kv_cache_len :]

        # Computes attention
        dropout = self.dropout if self.training else 0.0
        if mask is None:
            xo = F.scaled_dot_product_attention(xq, xk, xv, dropout_p=dropout, is_causal=is_causal)
        else:
            xo = F.scaled_dot_product_attention(xq, xk, xv, attn_mask=mask[:, None, None], dropout_p=dropout)

        # Flattens (B, G, H, T, C) -> (B, T, G * H * C)
        xo = xo.permute(0, 3, 1, 2, 4).flatten(2)

        # Applies output projection
        xo = self.out_proj(xo)

        return xo, torch.stack((xk, xv), dim=0)

    def get_attn_matrix(
        self,
        query: Tensor,
        key: Tensor,
        state: Tensor | None = None,
        is_causal: bool = False,
        rotary_q: Tensor | None = None,
        rotary_k: Tensor | None = None,
        mask: Tensor | None = None,
    ) -> Tensor:
        """Computes the attention matrix for a given query and key.

        This function can be used for visualization purposes.

        Args:
            query: The query vector, with shape ``(B, Tq, C)``
            key: The key vector, with shape ``(B, Tk, C)``
            state: The previous state tensor.
            is_causal: Whether to apply a causal mask to the attention matrix.
                In this function, unlike in the forward pass, the mask is
                explicitly created if not provided.
            rotary_q: The rotary embeddings for the query tensor, of shape
                ``(G, H, C // H)``. If ``None``, don't apply rotary embeddings.
            rotary_k: The rotary embeddings for the key tensor, of shape
                ``(G, H, C // H)``. If ``None``, don't apply rotary embeddings.
            mask: The attention mask, of shape ``(B, Tq, Tk)``. If ``None``,
                don't apply an attention mask.

        Returns:
            The attention matrix, of shape ``(B, G, H, Tq, Tk)``.
        """
        assert query.dim() == 3 and key.dim() == 3

        # Computes query, key, and value projections
        qkw_splits = (self.embed_dim, self.kv_embed_dim, self.kv_embed_dim)
        if self._qkv_same_embed_dim:
            qw, kw, _ = self.in_proj_weight.split(qkw_splits, dim=0)
        else:
            qw, kw = self.q_proj_weight, self.k_proj_weight
        qb, kb, _ = (None, None, None) if self.in_proj_bias is None else self.in_proj_bias.split(qkw_splits, dim=0)

        xq = F.linear(query, qw, qb)
        xk = F.linear(key, kw, kb)

        # Permutes (B, T, G * H * C) -> (B, G, H, T, C)
        xq = xq.unflatten(-1, (self.gqa_factor, self.kv_num_heads, self.head_dim)).permute(0, 2, 3, 1, 4)
        xk = xk.unflatten(-1, (1, self.kv_num_heads, self.head_dim)).permute(0, 2, 3, 1, 4)

        # Applies rotary embeddings.
        if rotary_q is not None:
            xq = apply_rotary_embeddings(xq.flatten(0, 2), rotary_q).view(xq.shape)
        if rotary_k is not None:
            xk = apply_rotary_embeddings(xk.flatten(0, 2), rotary_k).view(xk.shape)

        # Concatenates previous states
        if state is not None:
            prev_k, _ = state
            xk = torch.cat((prev_k, xk), dim=-2)
            if self.max_kv_cache_len is not None:
                xk = xk[:, -self.max_kv_cache_len :]

        # Computes the unnormalized attention scores.
        attn = torch.einsum("bghqc,bghkc->bghqk", xq, xk)

        # Applies a causal mask.
        if is_causal:
            causal_mask = get_causal_mask(query.shape[1], key.shape[1], query.device, query.dtype)
            causal_mask = causal_mask.expand(query.shape[0], *causal_mask.shape)
            attn = attn + causal_mask[:, None, None]

        # Applies the additional attention mask, if provided.
        if mask is not None:
            attn = attn + mask[:, None, None]

        # Normalizes.
        attn = F.softmax(attn, dim=-1)

        return attn


class TransformerEncoderLayer(nn.Module):
    """Defines a transformer encoder layer.

    This layer is a drop-in replacement for ``nn.TransformerEncoderLayer``
    except that it returns the attention state for causal attention, which can
    be used to implement streaming inference.

    Parameters:
        d_model: The input and output embedding dimension.
        nhead: The number of attention heads.
        dim_feedforward: The dimension of the feedforward network.
        dropout: The dropout probability, applied to the attention matrix.
        layer_norm_eps: The layer normalization epsilon value.
        norm_first: Whether to apply layer normalization before the attention
            layer.
        gqa_factor: The GQA factor to use, meaning the ratio of the number of
            queries to the number of keys. Higher values will result in more
            queries than keys, which can speed up inference.
        max_kv_cache_len: The maximum number of previous timesteps to cache
            for the key and value tensors. If ``None``, don't clip the maximum
            length.

    Inputs:
        src: The input tensor, of shape ``(B, T, C)``.
        state: The previous state tensor, if applicable.
        is_causal: Whether to apply a causal mask to the attention matrix.
            Note that the "mask" is only applied implicitly and isn't actually
            instantiated as a tensor.
        rotary_q: The rotary embeddings for the query tensor, of shape
            ``(G, H, C // H)``. If ``None``, don't apply rotary embeddings.
        rotary_k: The rotary embeddings for the key tensor, of shape
            ``(G, H, C // H)``. If ``None``, don't apply rotary embeddings.
        mask: The attention mask, of shape ``(B, Tq, Tk)``. If ``None``, don't
            apply an attention mask.

    Outputs:
        output: The output tensor, of shape ``(B, T, C)``.
        state: The next state tensor.
    """

    __constants__ = ["norm_first"]

    def __init__(
        self,
        d_model: int,
        nhead: int,
        dim_feedforward: int = 2048,
        dropout: float = 0.1,
        layer_norm_eps: float = 1e-5,
        norm_first: bool = False,
        gqa_factor: int = 1,
        max_kv_cache_len: int | None = None,
    ) -> None:
        super().__init__()

        # Self-attention layer.
        self.self_attn = MultiheadAttention(
            d_model,
            nhead,
            dropout=dropout,
            gqa_factor=gqa_factor,
            max_kv_cache_len=max_kv_cache_len,
        )

        # Feed-forward layers.
        self.linear1 = nn.Linear(d_model, dim_feedforward)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.ReLU()
        self.linear2 = nn.Linear(dim_feedforward, d_model)

        # Extras (norms and dropout).
        self.norm_first = norm_first
        self.norm1 = nn.LayerNorm(d_model, eps=layer_norm_eps)
        self.norm2 = nn.LayerNorm(d_model, eps=layer_norm_eps)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(
        self,
        src: Tensor,
        state: Tensor | None = None,
        is_causal: bool = False,
        rotary_q: Tensor | None = None,
        rotary_k: Tensor | None = None,
        mask: Tensor | None = None,
    ) -> tuple[Tensor, Tensor]:
        x = src
        if self.norm_first:
            xi, state = self._sa_block(self.norm1(x), state, is_causal, rotary_q, rotary_k, mask)
            x = x + xi
            x = x + self._ff_block(self.norm2(x))
        else:
            xi, state = self._sa_block(x, state, is_causal, rotary_q, rotary_k, mask)
            x = self.norm1(x + xi)
            x = self.norm2(x + self._ff_block(x))
        return x, state

    def _sa_block(
        self,
        x: Tensor,
        state: Tensor | None,
        is_causal: bool,
        rotary_q: Tensor | None = None,
        rotary_k: Tensor | None = None,
        mask: Tensor | None = None,
    ) -> tuple[Tensor, Tensor]:
        x, state = self.self_attn.forward(x, x, x, state, is_causal, rotary_q, rotary_k, mask)
        return self.dropout1(x), state

    def _sa_block_attn_matrix(
        self,
        x: Tensor,
        state: Tensor | None,
        is_causal: bool,
        rotary_q: Tensor | None = None,
        rotary_k: Tensor | None = None,
        mask: Tensor | None = None,
    ) -> Tensor:
        return self.self_attn.get_attn_matrix(x, x, state, is_causal, rotary_q, rotary_k, mask)

    def _ff_block(self, x: Tensor) -> Tensor:
        x = self.linear2(self.dropout(self.activation(self.linear1(x))))
        return self.dropout2(x)

    def get_attn_matrix(
        self,
        src: Tensor,
        state: Tensor | None = None,
        is_causal: bool = False,
        rotary_q: Tensor | None = None,
        rotary_k: Tensor | None = None,
        mask: Tensor | None = None,
    ) -> Tensor:
        """Computes the attention matrix for a given query and key.

        This function can be used for visualization purposes.

        Args:
            src: The input tensor, of shape ``(B, T, C)``.
            state: The previous state tensor, if applicable.
            is_causal: Whether to apply a causal mask to the attention matrix.
                In this function, unlike in the forward pass, the mask is
                explicitly created if not provided.
            rotary_q: The rotary embeddings for the query tensor, of shape
                ``(G, H, C // H)``. If ``None``, don't apply rotary embeddings.
            rotary_k: The rotary embeddings for the key tensor, of shape
                ``(G, H, C // H)``. If ``None``, don't apply rotary embeddings.
            mask: The attention mask, of shape ``(B, Tq, Tk)``. If ``None``,
                don't apply an attention mask.

        Returns:
            The attention matrix, of shape ``(B, G, H, Tq, Tk)``.
        """
        if self.norm_first:
            return self._sa_block_attn_matrix(self.norm1(src), state, is_causal, rotary_q, rotary_k, mask)
        return self._sa_block_attn_matrix(src, state, is_causal, rotary_q, rotary_k, mask)


class TransformerEncoder(nn.Module):
    """Defines a transformer encoder.

    This is a drop-in replacement for ``nn.TransformerEncoder`` except that it
    returns the attention state for causal attention, which can be used to
    implement streaming inference.

    This additionally supports using rotary embeddings for the key-query
    matrix multiplications. The rotary embedding tensors are computed at
    runtime and cached.

    Parameters:
        encoder_layer: The encoder layer to use.
        num_layers: The number of encoder layers.
        norm: The normalization layer to use. Defaults to ``None``.
        is_causal: Default value for ``is_causal`` in the ``forward`` method
            if not supplied. Controls causal verses bidirectional attention.
        use_rotary: Default value for ``use_rotary`` in the ``forward`` method
            if not supplied. Controls the use of rotary embeddings in the
            key-query matrix multiplication.
        rotary_base: The base value for rotary embeddings.

    Inputs:
        src: The input tensor, of shape ``(B, T, C)``.
        state: The previous state tensor, if applicable.
        is_causal: Whether to apply a causal mask to the attention matrix.
            Note that the "mask" is only applied implicitly and isn't actually
            instantiated as a tensor.
        use_rotary: If set, use rotary embeddings in the key-query matrix
            multiplication.
        mask: The attention mask, of shape ``(B, Tq, Tk)``. If ``None``, don't
            apply an attention mask.

    Outputs:
        output: The output tensor, of shape ``(B, T, C)``.
        state: The previous state tensor, if applicable.
    """

    __constants__ = ["num_heads", "head_dim", "kdim", "vdim", "embed_dim", "is_causal", "use_rotary", "rotary_base"]

    def __init__(
        self,
        encoder_layer: TransformerEncoderLayer,
        num_layers: int,
        norm: nn.LayerNorm | None = None,
        is_causal: bool | None = None,
        use_rotary: bool = False,
        rotary_base: int = 10_000,
    ) -> None:
        super().__init__()

        # Keeps some constant values in the top-level layer.
        self.num_heads = encoder_layer.self_attn.num_heads
        self.head_dim = encoder_layer.self_attn.head_dim
        self.kdim = encoder_layer.self_attn.kdim
        self.vdim = encoder_layer.self_attn.vdim
        self.embed_dim = encoder_layer.self_attn.embed_dim
        self.is_causal = is_causal
        self.use_rotary = use_rotary
        self.rotary_base = rotary_base

        self.layers = _get_clones(encoder_layer, num_layers)
        self.num_layers = num_layers
        self.norm = nn.Identity() if norm is None else norm
        self.rotary_q: Tensor | None = None
        self.rotary_k: Tensor | None = None

    def _get_rotary_embeddings(
        self,
        tsz: int,
        state: Tensor | None,
        device: torch.device,
        dtype: torch.dtype,
    ) -> tuple[Tensor, Tensor]:
        if state is None:
            if self.rotary_q is None or self.rotary_q.shape[-2] < tsz:
                self.rotary_q = get_rotary_embeddings(tsz, self.head_dim, device, dtype, 0, self.rotary_base)
            if self.rotary_k is None or self.rotary_k.shape[-2] < tsz:
                self.rotary_k = get_rotary_embeddings(tsz, self.head_dim, device, dtype, 0, self.rotary_base)
            return self.rotary_q[..., :tsz, :], self.rotary_k[..., :tsz, :]

        else:
            offset = state.shape[-2]
            rotary_q = get_rotary_embeddings(tsz, self.head_dim, device, dtype, offset, self.rotary_base)
            rotary_k = get_rotary_embeddings(tsz, self.head_dim, device, dtype, offset, self.rotary_base)
            return rotary_q, rotary_k

    def _default(self, *values: bool | None) -> bool:
        for value in values:
            if value is not None:
                return value
        return False  # Arbitrary.

    def forward(
        self,
        src: Tensor,
        state: Tensor | None = None,
        is_causal: bool | None = None,
        use_rotary: bool | None = None,
        mask: Tensor | None = None,
    ) -> tuple[Tensor, Tensor]:
        is_causal = self._default(is_causal, self.is_causal, state is None)
        use_rotary = self._default(use_rotary, self.use_rotary)

        output = src
        state_out = []
        _, tsz, _ = src.shape
        rotary_q, rotary_k = (
            self._get_rotary_embeddings(
                tsz=tsz,
                state=state,
                device=src.device,
                dtype=src.dtype,
            )
            if use_rotary
            else (None, None)
        )
        for i, layer in enumerate(self.layers):
            state_i = None if state is None else state[i]
            output, state_out_i = layer.forward(output, state_i, is_causal, rotary_q, rotary_k, mask)
            state_out.append(state_out_i)
        return self.norm(output), torch.stack(state_out, dim=0)

    def get_attn_matrices(
        self,
        src: Tensor,
        state: Tensor | None = None,
        is_causal: bool | None = None,
        use_rotary: bool | None = None,
        mask: Tensor | None = None,
    ) -> Tensor:
        """Computes the attention matrices for a given query and key.

        This function can be used for visualization purposes.

        Args:
            src: The input tensor, of shape ``(B, T, C)``.
            state: The previous key and value tensors, of shape
                ``(B * H, T', C // H)``, where ``T'`` is the number of previous
                timesteps and ``H`` is the number of attention heads. This is
                only supported if ``is_causal=True``.
            is_causal: Whether to apply a causal mask to the attention matrix.
                In this function, unlike in the forward pass, the mask is
                explicitly created if not provided.
            use_rotary: If set, use rotary embeddings in the key-query matrix
                multiplication.
            mask: The attention mask, of shape ``(B, Tq, Tk)``. If ``None``,
                don't apply an attention mask.

        Returns:
            The attention matrices, of shape ``(B, L, G, H, Tq, Tk)``, where
            ``L`` is the number of encoder layers.
        """
        is_causal = self._default(is_causal, self.is_causal, state is None)
        use_rotary = self._default(use_rotary, self.use_rotary)

        output = src
        _, tsz, _ = src.shape
        rotary_q, rotary_k = (
            self._get_rotary_embeddings(
                tsz=tsz,
                state=state,
                device=src.device,
                dtype=src.dtype,
            )
            if use_rotary
            else (None, None)
        )
        matrices = []
        for i, layer in enumerate(self.layers):
            state_i = None if state is None else state[i]
            matrices.append(layer.get_attn_matrix(output, state_i, is_causal, rotary_q, rotary_k, mask))
            if i < len(self.layers) - 1:
                output, _ = layer.forward(output, state_i, is_causal, rotary_q, rotary_k, mask)
        return torch.stack(matrices, dim=1)


@torch.no_grad()
def nucleus_sampling(logits: Tensor, p: float, temperature: float = 1.0, dim: int = -1) -> Tensor:
    """Samples from a distribution using nucleus sampling.

    This is a modified version of ``torch.multinomial`` that uses nucleus
    sampling instead of top-k sampling. The difference is that top-k sampling
    sets the probability of all values outside the top-k to zero, whereas
    nucleus sampling sets the probability of all values outside the top-p
    to zero.

    Parameters:
        logits: The input tensor, of shape ``(B, T, C)``.
        p: The probability threshold.
        temperature: The temperature to apply to the logits.
        dim: The dimension to sample from. Defaults to ``-1``.

    Returns:
        The sampled indices, of shape ``(B, T)``.
    """
    assert 0.0 <= p <= 1.0, f"`{p=}` must be between 0 and 1"
    if dim != -1:
        logits = logits.transpose(dim, -1)
    orig_shape = logits.shape[:-1]
    logits = logits.flatten(0, -2)
    probs = F.softmax(logits / temperature, dim=-1)
    sorted_probs, indices = torch.sort(probs, descending=True, dim=-1)
    cum_sum_probs = torch.cumsum(sorted_probs, dim=-1)
    nucleus = cum_sum_probs < p
    nucleus[:, 1:] = nucleus[:, :-1].clone()
    nucleus[:, 0] = 1
    sorted_probs[~nucleus] = 0.0
    sampled_sorted_indexes = torch.multinomial(sorted_probs, 1)
    sample = torch.gather(indices, -1, sampled_sorted_indexes)
    sample = sample.view(*orig_shape, 1)
    if dim != -1:
        sample = sample.transpose(dim, -1)
    return sample.squeeze(dim)


T = TypeVar("T", bound=nn.Module)


def _get_clones(module: T, num_layers: int) -> list[T]:
    return cast(list[T], nn.ModuleList([copy.deepcopy(module) for _ in range(num_layers)]))
