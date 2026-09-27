"""Generate a minimal homogeneous Gadget-2 particle template for gevolution.

Qualification infrastructure only. The binary contains one CDM template
particle at the center of a unit box. gevolution tiles the template according
to the prospectively frozen tiling factor.
"""

from __future__ import annotations

import argparse
import pathlib
import struct


HEADER_BYTES = 256


def build_header() -> bytes:
    npart = [0, 1, 0, 0, 0, 0]
    mass = [0.0] * 6
    time = 1.0
    redshift = 0.0
    flag_sfr = 0
    flag_feedback = 0
    npart_total = npart.copy()
    flag_cooling = 0
    num_files = 1
    box_size = 1.0
    omega0 = 1.0
    omega_lambda = 0.0
    hubble_param = 1.0
    flag_age = 0
    flag_metals = 0
    npart_total_hw = [0] * 6
    fill = bytes(64)

    header = struct.pack(
        "<6I6d2d2i6I2i4d2i6I64s",
        *npart,
        *mass,
        time,
        redshift,
        flag_sfr,
        flag_feedback,
        *npart_total,
        flag_cooling,
        num_files,
        box_size,
        omega0,
        omega_lambda,
        hubble_param,
        flag_age,
        flag_metals,
        *npart_total_hw,
        fill,
    )
    if len(header) != HEADER_BYTES:
        raise RuntimeError(f"unexpected Gadget-2 header size: {len(header)}")
    return header


def write_template(path: pathlib.Path) -> None:
    header = build_header()
    positions = struct.pack("<3f", 0.5, 0.5, 0.5)

    with path.open("wb") as handle:
        handle.write(struct.pack("<i", HEADER_BYTES))
        handle.write(header)
        handle.write(struct.pack("<i", HEADER_BYTES))
        handle.write(struct.pack("<i", len(positions)))
        handle.write(positions)
        handle.write(struct.pack("<i", len(positions)))


def validate_template(path: pathlib.Path) -> None:
    data = path.read_bytes()
    if len(data) != 4 + HEADER_BYTES + 4 + 4 + 12 + 4:
        raise RuntimeError(f"unexpected template byte length: {len(data)}")

    offset = 0
    (head_open,) = struct.unpack_from("<i", data, offset)
    offset += 4
    if head_open != HEADER_BYTES:
        raise RuntimeError("invalid Gadget-2 header opening marker")

    header = data[offset : offset + HEADER_BYTES]
    offset += HEADER_BYTES
    (head_close,) = struct.unpack_from("<i", data, offset)
    offset += 4
    if head_close != HEADER_BYTES:
        raise RuntimeError("invalid Gadget-2 header closing marker")

    npart = list(struct.unpack_from("<6I", header, 0))
    if npart[1] != 1 or sum(npart) != 1:
        raise RuntimeError(f"unexpected particle counts: {npart}")

    # num_files sits after 6I + 6d + 2d + 2i + 6I + 1i.
    num_files_offset = 6 * 4 + 6 * 8 + 2 * 8 + 2 * 4 + 6 * 4 + 4
    (num_files,) = struct.unpack_from("<i", header, num_files_offset)
    if num_files != 1:
        raise RuntimeError(f"unexpected num_files: {num_files}")

    # BoxSize immediately follows num_files.
    (box_size,) = struct.unpack_from("<d", header, num_files_offset + 4)
    if box_size <= 0.0:
        raise RuntimeError(f"invalid BoxSize: {box_size}")

    (pos_open,) = struct.unpack_from("<i", data, offset)
    offset += 4
    if pos_open != 12:
        raise RuntimeError(f"unexpected positions block size: {pos_open}")

    xyz = struct.unpack_from("<3f", data, offset)
    offset += 12
    (pos_close,) = struct.unpack_from("<i", data, offset)
    if pos_close != 12:
        raise RuntimeError("positions closing marker mismatch")
    if any(value < 0.0 or value > box_size for value in xyz):
        raise RuntimeError(f"particle position out of bounds: {xyz}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_template(output)
    validate_template(output)
    print(f"wrote validated Gadget-2 template: {output}")


if __name__ == "__main__":
    main()
