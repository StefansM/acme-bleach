import codecs


def lookup(coding_name: str) -> codecs.CodecInfo | None:
    """Function registered with the codecs module to find the bleach codec."""

    if coding_name != "bleach":
        return None

    return codecs.CodecInfo(
        encode=encode_bleach,  # type: ignore
        decode=decode_bleach,  # type: ignore
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )


def encode_bleach(input_chars: str, errors: str = "strict") -> tuple[bytes, int]:
    """Bleach a file, replacing everything with spaces and tabs.

    Converts the file into a set of UTF-8 encoded bytes, then generates a
    string representation of the bytes using spaces for 1s and tabs for zeros.
    This encoding also writes a newline every 40 characters, to avoid
    extremely long line lengths. The newlines could be removed without affecting
    the encoded document.
    """

    bleached_lines = []
    byte_encoding = input_chars.encode("UTF-8")
    as_bits = "".join([f"{x:08b}" for x in byte_encoding])
    bleached = as_bits.replace("1", " ").replace("0", "\t")
    for i in range(0, len(bleached), 40):
        bleached_lines.append(bleached[i : i + 40])

    # Terminate with blank line.
    bleached_lines.append("")

    # We're only using tabs and spaces, we know ascii is sufficient.
    return "\n".join(bleached_lines).encode("ascii"), len(input_chars)


def decode_bleach(input_bytes: bytes, errors: str = "strict") -> tuple[str, int]:
    """Unbleach a file by decoding tabs and spaces into bytes.

    Replaces all spaces with 1s and tabs with 0s, and interprets each chunk of
    8 characters as a byte. The resulting document is a series of UTF-8
    encoded bytes representing the original document. Newlines are ignored.
    """
    input_lines = bytearray(input_bytes).decode("ascii").split("\n")
    output_bytes = bytearray()

    for line in input_lines:
        if line.startswith("#"):
            continue

        binary_str = line.replace(" ", "1").replace("\t", "0")
        for i in range(0, len(binary_str), 8):
            b = int(binary_str[i : i + 8], 2)
            output_bytes.append(b)

    return output_bytes.decode("UTF-8"), len(input_bytes)


class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: str, final: bool = False) -> bytes:
        return encode_bleach(input, self.errors)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):
    def __init__(self, errors: str = "strict") -> None:
        super().__init__(errors)
        self.buffer = bytearray()
        self.i = 0

    def decode(self, input: bytes, final: bool = False) -> str:  # type: ignore
        if not final:
            self.buffer.extend(input)
            return ""

        result = bytes(self.buffer)
        # Needs to make sure this returns "" if called again with final=True.
        # If it returns output, this will get called again and again.
        self.buffer.clear()
        if result:
            # The interpreter chomps the first line from the decoded text, so
            # we add a comment here.
            return "# coding=utf-8\n" + decode_bleach(result)[0]

        return ""


class StreamWriter(codecs.StreamWriter):
    encode = encode_bleach  # type: ignore


class StreamReader(codecs.StreamReader):
    decode = decode_bleach  # type: ignore


# Register codec when this file is imported.
codecs.register(lookup)
