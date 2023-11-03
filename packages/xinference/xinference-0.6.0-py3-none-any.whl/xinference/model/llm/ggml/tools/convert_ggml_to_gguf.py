#!/usr/bin/env python3
# Copied from llama.cpp to convert ggml file to gguf
from __future__ import annotations

import argparse
import struct
from enum import IntEnum
from pathlib import Path
from typing import Optional

import numpy as np

from . import gguf

# Note: Does not support GGML_QKK_64
QK_K = 256
# Items here are (block size, type size)
GGML_QUANT_SIZES = {
    gguf.GGMLQuantizationType.F32: (1, 4),
    gguf.GGMLQuantizationType.F16: (1, 2),
    gguf.GGMLQuantizationType.Q4_0: (32, 2 + 16),
    gguf.GGMLQuantizationType.Q4_1: (32, 2 + 2 + 16),
    gguf.GGMLQuantizationType.Q5_0: (32, 2 + 4 + 16),
    gguf.GGMLQuantizationType.Q5_1: (32, 2 + 2 + 4 + 16),
    gguf.GGMLQuantizationType.Q8_0: (32, 2 + 32),
    gguf.GGMLQuantizationType.Q8_1: (32, 4 + 4 + 32),
    gguf.GGMLQuantizationType.Q2_K: (256, 2 + 2 + QK_K // 16 + QK_K // 4),
    gguf.GGMLQuantizationType.Q3_K: (256, 2 + QK_K // 4 + QK_K // 8 + 12),
    gguf.GGMLQuantizationType.Q4_K: (256, 2 + 2 + QK_K // 2 + 12),
    gguf.GGMLQuantizationType.Q5_K: (256, 2 + 2 + QK_K // 2 + QK_K // 8 + 12),
    gguf.GGMLQuantizationType.Q6_K: (256, 2 + QK_K // 2 + QK_K // 4 + QK_K // 16),
    gguf.GGMLQuantizationType.Q8_K: (256, 4 + QK_K + QK_K // 8),
}


class GGMLFormat(IntEnum):
    GGML = 0
    GGMF = 1
    GGJT = 2


class GGMLFType(IntEnum):
    ALL_F32 = 0
    MOSTLY_F16 = 1
    MOSTLY_Q4_0 = 2
    MOSTLY_Q4_1 = 3
    MOSTLY_Q4_1_SOME_F16 = 4
    MOSTLY_Q8_0 = 7
    MOSTLY_Q5_0 = 8
    MOSTLY_Q5_1 = 9
    MOSTLY_Q2_K = 10
    MOSTLY_Q3_K_S = 11
    MOSTLY_Q3_K_M = 12
    MOSTLY_Q3_K_L = 13
    MOSTLY_Q4_K_S = 14
    MOSTLY_Q4_K_M = 15
    MOSTLY_Q5_K_S = 16
    MOSTLY_Q5_K_M = 17
    MOSTLY_Q6_K = 18


class Hyperparameters:
    def __init__(self):
        self.n_vocab = self.n_embd = self.n_mult = self.n_head = 0
        self.n_layer = self.n_rot = self.n_ff = 0
        self.ftype = GGMLFType.ALL_F32

    def set_n_ff(self, model):
        ff_tensor_idx = model.tensor_map.get(b"layers.0.feed_forward.w1.weight")
        assert ff_tensor_idx is not None, "Missing layer 0 FF tensor"
        ff_tensor = model.tensors[ff_tensor_idx]
        self.n_ff = ff_tensor.dims[1]

    def load(self, data, offset):
        (
            self.n_vocab,
            self.n_embd,
            self.n_mult,
            self.n_head,
            self.n_layer,
            self.n_rot,
            ftype,
        ) = struct.unpack("<7I", data[offset : offset + (4 * 7)])
        try:
            self.ftype = GGMLFType(ftype)
        except ValueError:
            raise ValueError(f"Invalid ftype {ftype}")
        return 4 * 7

    def __str__(self):
        return f"<Hyperparameters: n_vocab={self.n_vocab}, n_embd={self.n_embd}, n_mult={self.n_mult}, n_head={self.n_head}, n_layer={self.n_layer}, n_rot={self.n_rot}, n_ff={self.n_ff}, ftype={self.ftype.name}>"


class Vocab:
    def __init__(self, load_scores=True):
        self.items = []
        self.load_scores = load_scores

    def load(self, data, offset, n_vocab):
        orig_offset = offset
        for _ in range(n_vocab):
            itemlen = struct.unpack("<I", data[offset : offset + 4])[0]
            assert itemlen < 4096, "Absurd vocab item length"
            offset += 4
            item_text = bytes(data[offset : offset + itemlen])
            offset += itemlen
            if self.load_scores:
                item_score = struct.unpack("<f", data[offset : offset + 4])[0]
                offset += 4
            else:
                item_score = 0.0
            self.items.append((item_text, item_score))
        return offset - orig_offset


class Tensor:
    def __init__(self, use_padding=True):
        self.name = None
        self.dims: tuple[int, ...] = ()
        self.dtype = None
        self.start_offset = 0
        self.len_bytes = np.int64(0)
        self.use_padding = use_padding

    def load(self, data, offset):
        orig_offset = offset
        (n_dims, name_len, dtype) = struct.unpack("<3I", data[offset : offset + 12])
        assert n_dims >= 0 and n_dims <= 4, f"Invalid tensor dimensions {n_dims}"
        assert name_len < 4096, "Absurd tensor name length"
        quant = GGML_QUANT_SIZES.get(dtype)
        assert quant is not None, "Unknown tensor type"
        (blksize, tysize) = quant
        offset += 12
        self.dtype = dtype
        self.dims = struct.unpack(f"<{n_dims}I", data[offset : offset + (4 * n_dims)])
        offset += 4 * n_dims
        self.name = bytes(data[offset : offset + name_len])
        offset += name_len
        pad = ((offset + 31) & ~31) - offset if self.use_padding else 0
        offset += pad
        n_elems = np.prod(self.dims)
        n_bytes = np.int64(np.int64(n_elems) * np.int64(tysize)) // np.int64(blksize)
        self.start_offset = offset
        self.len_bytes = n_bytes
        offset += n_bytes
        # print(n_dims, name_len, dtype, self.dims, self.name, pad)
        return offset - orig_offset


class GGMLModel:
    def __init__(self):
        self.hyperparameters = None
        self.vocab = None
        self.tensor_map = {}
        self.tensors = []

    def validate_header(self, data, offset):
        magic = bytes(data[offset : offset + 4])
        if magic == b"GGUF":
            raise ValueError("File is already in GGUF format.")
        if magic == b"lmgg":
            self.file_format = GGMLFormat.GGML
            self.format_version = 1
            return 4
        version = struct.unpack("<I", data[offset + 4 : offset + 8])[0]
        if magic == b"fmgg":
            if version != 1:
                raise ValueError(
                    f"Cannot handle unexpected GGMF file version {version}"
                )
            self.file_format = GGMLFormat.GGMF
            self.format_version = version
            return 8
        if magic == b"tjgg":
            if version < 1 or version > 3:
                raise ValueError(
                    f"Cannot handle unexpected GGJT file version {version}"
                )
            self.file_format = GGMLFormat.GGJT
            self.format_version = version
            return 8
        raise ValueError(
            f"Unexpected file magic {magic!r}! This doesn't look like a GGML format file."
        )

    def validate_conversion(self, ftype):
        err = ""
        if self.file_format < GGMLFormat.GGJT or self.format_version < 2:
            if ftype not in (GGMLFType.ALL_F32, GGMLFType.MOSTLY_F16):
                err = "Quantizations changed in GGJTv2. Can only convert unquantized GGML files older than GGJTv2."
        elif self.file_format == GGMLFormat.GGJT and self.format_version == 2:
            if ftype in (
                GGMLFType.MOSTLY_Q4_0,
                GGMLFType.MOSTLY_Q4_1,
                GGMLFType.MOSTLY_Q4_1_SOME_F16,
                GGMLFType.MOSTLY_Q8_0,
            ):
                err = "Q4 and Q8 quantizations changed in GGJTv3."
        if len(err) > 0:
            raise ValueError(
                f"{err} Sorry, your {self.file_format.name}v{self.format_version} file of type {ftype.name} is not eligible for conversion."
            )

    def load(self, data, offset):
        offset += self.validate_header(data, offset)
        hp = Hyperparameters()
        offset += hp.load(data, offset)
        print(
            f"* File format: {self.file_format.name}v{self.format_version} with ftype {hp.ftype.name}"
        )
        self.validate_conversion(hp.ftype)
        vocab = Vocab(load_scores=self.file_format > GGMLFormat.GGML)
        offset += vocab.load(data, offset, hp.n_vocab)
        tensors: list[Tensor] = []
        tensor_map = {}
        while offset < len(data):
            tensor = Tensor(use_padding=self.file_format > GGMLFormat.GGMF)
            offset += tensor.load(data, offset)
            tensor_map[tensor.name] = len(tensors)
            tensors.append(tensor)
        self.hyperparameters = hp
        self.vocab = vocab
        self.tensors = tensors
        self.tensor_map = tensor_map
        hp.set_n_ff(self)
        return offset


class GGMLToGGUF:
    def __init__(
        self,
        ggml_model,
        data,
        cfg,
        params_override=None,
        vocab_override=None,
        special_vocab=None,
    ):
        hp = ggml_model.hyperparameters
        self.model = ggml_model
        self.data = data
        self.cfg = cfg
        self.params_override = params_override
        self.vocab_override = vocab_override
        self.special_vocab = special_vocab
        if params_override is not None:
            n_kv_head = params_override.n_head_kv
        else:
            if cfg.gqa == 1:
                n_kv_head = hp.n_head
            else:
                gqa = float(cfg.gqa)
                n_kv_head = None
                for x in range(1, 256):
                    if float(hp.n_head) / float(x) == gqa:
                        n_kv_head = x
                assert (
                    n_kv_head is not None
                ), "Couldn't determine n_kv_head from GQA param"
                print(f"- Guessed n_kv_head = {n_kv_head} based on GQA {cfg.gqa}")
        self.n_kv_head = n_kv_head
        self.name_map = gguf.get_tensor_name_map(
            gguf.MODEL_ARCH.LLAMA, ggml_model.hyperparameters.n_layer
        )

    def save(self):
        print("* Preparing to save GGUF file")
        gguf_writer = gguf.GGUFWriter(
            self.cfg.output,
            gguf.MODEL_ARCH_NAMES[gguf.MODEL_ARCH.LLAMA],
            use_temp_file=False,
        )
        self.add_params(gguf_writer)
        self.add_vocab(gguf_writer)
        if self.special_vocab is not None:
            self.special_vocab.add_to_gguf(gguf_writer)
        self.add_tensors(gguf_writer)
        print("    gguf: write header")
        gguf_writer.write_header_to_file()
        print("    gguf: write metadata")
        gguf_writer.write_kv_data_to_file()
        print("    gguf: write tensors")
        gguf_writer.write_tensors_to_file()
        gguf_writer.close()

    def add_params(self, gguf_writer):
        hp = self.model.hyperparameters
        cfg = self.cfg
        if cfg.desc is not None:
            desc = cfg.desc
        else:
            desc = f"converted from legacy {self.model.file_format.name}v{self.model.format_version} {hp.ftype.name} format"
        try:
            # Filenames aren't necessarily valid UTF8.
            name = cfg.name if cfg.name is not None else cfg.input.name
        except UnicodeDecodeError:
            name = None
        print("* Adding model parameters and KV items")
        if name is not None:
            gguf_writer.add_name(name)
        gguf_writer.add_description(desc)
        gguf_writer.add_file_type(int(hp.ftype))
        if self.params_override is not None:
            po = self.params_override
            assert po.n_embd == hp.n_embd, "Model hyperparams mismatch"
            assert po.n_layer == hp.n_layer, "Model hyperparams mismatch"
            assert po.n_head == hp.n_head, "Model hyperparams mismatch"
            gguf_writer.add_context_length(po.n_ctx)
            gguf_writer.add_embedding_length(po.n_embd)
            gguf_writer.add_block_count(po.n_layer)
            gguf_writer.add_feed_forward_length(po.n_ff)
            gguf_writer.add_rope_dimension_count(po.n_embd // po.n_head)
            gguf_writer.add_head_count(po.n_head)
            gguf_writer.add_head_count_kv(po.n_head_kv)
            gguf_writer.add_layer_norm_rms_eps(po.f_norm_eps)
            return
        gguf_writer.add_context_length(cfg.context_length)
        gguf_writer.add_embedding_length(hp.n_embd)
        gguf_writer.add_block_count(hp.n_layer)
        gguf_writer.add_feed_forward_length(hp.n_ff)
        gguf_writer.add_rope_dimension_count(hp.n_embd // hp.n_head)
        gguf_writer.add_head_count(hp.n_head)
        gguf_writer.add_head_count_kv(self.n_kv_head)
        gguf_writer.add_layer_norm_rms_eps(float(cfg.eps))

    def add_vocab(self, gguf_writer):
        hp = self.model.hyperparameters
        gguf_writer.add_tokenizer_model("llama")
        tokens = []
        scores = []
        toktypes = []
        if self.vocab_override is not None:
            vo = self.vocab_override
            print("* Adding vocab item(s)")
            for idx, (vbytes, score, ttype) in enumerate(vo.all_tokens()):
                tokens.append(vbytes)
                scores.append(score)
                toktypes.append(ttype)
            assert (
                len(tokens) == hp.n_vocab
            ), f"Override vocab has a different number of items than hyperparameters - override = {len(tokens)} but n_vocab={hp.n_vocab}"
            gguf_writer.add_token_list(tokens)
            gguf_writer.add_token_scores(scores)
            if len(toktypes) > 0:
                gguf_writer.add_token_types(toktypes)
            return
        print(f"* Adding {hp.n_vocab} vocab item(s)")
        assert (
            len(self.model.vocab.items) >= 3
        ), "Cannot handle unexpectedly short model vocab"
        for tokid, (vbytes, vscore) in enumerate(self.model.vocab.items):
            tt = 1  # Normal
            # Special handling for UNK, BOS, EOS tokens.
            if tokid <= 2:
                if tokid == 0:
                    vbytes = b"<unk>"
                    tt = 2
                elif tokid == 1:
                    vbytes = b"<s>"
                    tt = 3
                else:
                    vbytes = b"</s>"
                    tt = 3
            elif len(vbytes) == 0:
                tt = 3  # Control
            elif tokid >= 3 and tokid <= 258 and len(vbytes) == 1:
                vbytes = bytes(f"<0x{vbytes[0]:02X}>", encoding="UTF-8")
                tt = 6  # Byte
            else:
                vbytes = vbytes.replace(b" ", b"\xe2\x96\x81")
            toktypes.append(tt)
            tokens.append(vbytes)
            scores.append(vscore)
        gguf_writer.add_token_list(tokens)
        gguf_writer.add_token_scores(scores)
        gguf_writer.add_token_types(toktypes)
        gguf_writer.add_unk_token_id(0)
        gguf_writer.add_bos_token_id(1)
        gguf_writer.add_eos_token_id(2)

    def add_tensors(self, gguf_writer):
        tensor_map = self.name_map
        data = self.data
        print(f"* Adding {len(self.model.tensors)} tensor(s)")
        for tensor in self.model.tensors:
            name = str(tensor.name, "UTF-8")
            mapped_name = tensor_map.get_name(name, try_suffixes=(".weight", ".bias"))
            assert mapped_name is not None, f"Bad name {name}"
            tempdims = list(tensor.dims[:])
            if len(tempdims) > 1:
                temp = tempdims[1]
                tempdims[1] = tempdims[0]
                tempdims[0] = temp
            # print(f'+ {tensor.name} | {mapped_name} {tensor.dims} :: {tempdims}')
            gguf_writer.add_tensor(
                mapped_name,
                data[tensor.start_offset : tensor.start_offset + tensor.len_bytes],
                raw_shape=tempdims,
                raw_dtype=tensor.dtype,
            )


def handle_args():
    parser = argparse.ArgumentParser(description="Convert GGML models to GGUF")
    parser.add_argument(
        "--input", "-i", type=Path, required=True, help="Input GGMLv3 filename"
    )
    parser.add_argument(
        "--output", "-o", type=Path, required=True, help="Output GGUF filename"
    )
    parser.add_argument("--name", help="Set model name")
    parser.add_argument("--desc", help="Set model description")
    parser.add_argument(
        "--gqa",
        type=int,
        default=1,
        help="grouped-query attention factor (use 8 for LLaMA2 70B)",
    )
    parser.add_argument(
        "--eps",
        default="5.0e-06",
        help="RMS norm eps: Use 1e-6 for LLaMA1 and OpenLLaMA, use 1e-5 for LLaMA2",
    )
    parser.add_argument(
        "--context-length",
        "-c",
        type=int,
        default=2048,
        help="Default max context length: LLaMA1 is typically 2048, LLaMA2 is typically 4096",
    )
    return parser.parse_args()


from dataclasses import dataclass


@dataclass
class Config:
    input: Path
    output: Path
    name: Optional[str]
    desc: Optional[str]
    gqa: int
    eps: float
    context_length: int


def convert(
    source_path: str,
    dest_path: str,
    model_name: Optional[str] = None,
    model_desc: Optional[str] = None,
    gqa: int = 1,
    eps: float = 5.0e-06,
    context_length: int = 2048,
):
    cfg = Config(
        input=Path(source_path),
        output=Path(dest_path),
        name=model_name,
        desc=model_desc,
        gqa=gqa,
        eps=eps,
        context_length=context_length,
    )
    print(f"* Using config: {cfg}")
    print(
        "\n=== WARNING === Be aware that this conversion script is best-effort. Use a native GGUF model if possible. === WARNING ===\n"
    )
    if cfg.gqa == 1 or cfg.eps == "5.0e-06":
        print(
            '- Note: If converting LLaMA2, specifying "--eps 1e-5" is required. 70B models also need "--gqa 8".'
        )
    data = np.memmap(cfg.input, mode="r")
    model = GGMLModel()
    print("* Scanning GGML input file")
    model.load(data, 0)
    print(f"* GGML model hyperparameters: {model.hyperparameters}")
    vocab_override = None
    params_override = None
    special_vocab = None
    print(
        "\n=== WARNING === Special tokens may not be converted correctly. Use --model-metadata-dir if possible === WARNING ===\n"
    )
    if model.file_format == GGMLFormat.GGML:
        print(
            "! This is a very old GGML file that does not contain vocab scores. Strongly recommend using model metadata!"
        )
    converter = GGMLToGGUF(
        model,
        data,
        cfg,
        params_override=params_override,
        vocab_override=vocab_override,
        special_vocab=special_vocab,
    )
    converter.save()
    print(f"* Successful completion. Output saved to: {cfg.output}")
