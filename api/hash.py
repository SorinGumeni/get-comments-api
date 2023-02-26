#!/usr/bin/env python3
import base64
import hashlib
import json
import sys

"""
Recreation of the Terraform filebase64sha256 in Python

We cannot reproduce the hashing with available command line tools,
so we defer to this python implementation

Taken from here: https://gist.github.com/LouisAmon/ea395d39d80b28eb78181831fa523456
"""


def sha256sum(filename):
    """
    Helper function that calculates the hash of a file
    using the SHA256 algorithm
    Inspiration:
    https://stackoverflow.com/a/44873382
    NB: we're deliberately using `digest` instead of `hexdigest` in order to
    mimic Terraform.
    """
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.digest()


def filebase64sha256(filename):
    """
    Computes the Base64-encoded SHA256 hash of a file
    This function mimics its Terraform counterpart, therefore being compatible
    with Pulumi's provisioning engine.
    """
    h = sha256sum(filename)
    b = base64.b64encode(h)
    return b.decode()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print(f"Usage: {sys.argv[0]} <file>")
        quit(1)

    try:
        hash = filebase64sha256(sys.argv[1])
    except:
        print(f"Could not hash file: {sys.argv[1]}")
        quit(1)

    print(json.dumps({"hash": hash}))
