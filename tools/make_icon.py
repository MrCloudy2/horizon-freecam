import pathlib
import struct
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCALE = 16
ART = [
    "................",
    "................",
    "...KKKK.........",
    "..KLLLLK....KKK.",
    ".KKKKKKKKKKKKRKK",
    ".KLLLLLLLLLLLLLK",
    ".KDDDDKKKKKKDDDK",
    ".KDDDKBBBBBBKDDK",
    ".KDDKBCCCCCCBKDK",
    ".KDDKBCWWCCCBKDK",
    ".KDDKBCWCCCCBKDK",
    ".KDDKBCCCCCSBKDK",
    ".KDDDKBBBBBBKDDK",
    ".KSSSSKKKKKKSSSK",
    ".KKKKKKKKKKKKKKK",
    "................",
]
COLORS = {
    "K": (30, 30, 36, 255),
    "L": (138, 138, 150, 255),
    "D": (74, 74, 85, 255),
    "S": (52, 52, 61, 255),
    "B": (44, 92, 138, 255),
    "C": (63, 169, 245, 255),
    "W": (232, 246, 255, 255),
    "R": (229, 57, 53, 255),
    ".": (0, 0, 0, 0),
}


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def png(art, scale):
    size = len(art) * scale
    rows = bytearray()
    for line in art:
        assert len(line) == len(art), line
        row = b"".join(bytes(COLORS[c]) * scale for c in line)
        rows += (b"\x00" + row) * scale
    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b"")


def main():
    target = ROOT / "icon.png"
    target.write_bytes(png(ART, SCALE))
    print(target, target.stat().st_size, "bytes")


if __name__ == "__main__":
    sys.exit(main())
