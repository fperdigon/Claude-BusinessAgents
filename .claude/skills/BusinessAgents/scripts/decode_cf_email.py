"""Decode Cloudflare email obfuscation hex strings.

Usage:
    python decode_cf_email.py <hex_string>
    python decode_cf_email.py d1bcbbff...

The hex string is found after /cdn-cgi/l/email-protection# in page markdown.
"""

import sys


def decode_cf_email(hex_str: str) -> str:
    key = int(hex_str[:2], 16)
    return "".join(
        chr(int(hex_str[i : i + 2], 16) ^ key) for i in range(2, len(hex_str), 2)
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_cf_email.py <hex_string>", file=sys.stderr)
        sys.exit(1)
    print(decode_cf_email(sys.argv[1]))
