#!/usr/bin/env python3
"""
ULTIMATE Offline Bitcoin Wallet Generator with 12-word seed mnemonic phrases that supports Legacy, Nested SegWit, Native SegWit and Taproot

* RUN THIS SCRIPT & BACKUP OFFLINE! *

Supports: 
Legacy (1...), 
Nested SegWit (3...), 
Native SegWit (bc1q...), 
Taproot (bc1p...)

Install dependencies:
    pip install mnemonic ecdsa bech32 base58

Run:
    python bitcoin_wallet.py

"""

import os
import hashlib
import hmac
from mnemonic import Mnemonic
import ecdsa
from ecdsa import SECP256k1
import bech32
import base58

# === CONFIG ===
COIN_TYPE = 0
ACCOUNT = 0
CHANGE = 0
INDEX = 0
# ==============

mnemo = Mnemonic("english")

# ----------------------------
# Crypto Helpers
# ----------------------------
def generate_mnemonic(strength=128):
    return mnemo.to_mnemonic(os.urandom(strength // 8))

def mnemonic_to_seed(mnemonic, passphrase=""):
    return mnemo.to_seed(mnemonic, passphrase)

def hmac_sha512(key, data):
    return hmac.new(key, data, hashlib.sha512).digest()

def derive_master_key(seed):
    h = hmac_sha512(b"Bitcoin seed", seed)
    return h[:32], h[32:]

def private_to_public_key(privkey):
    sk = ecdsa.SigningKey.from_string(privkey, curve=SECP256k1)
    vk = sk.verifying_key
    x = vk.pubkey.point.x()
    prefix = b'\x02' if vk.pubkey.point.y() % 2 == 0 else b'\x03'
    return prefix + x.to_bytes(32, 'big')

def hash160(data):
    return hashlib.new('ripemd160', hashlib.sha256(data).digest()).digest()

# ----------------------------
# BIP-32 CKD (Child Key Derivation)
# ----------------------------
def CKDpriv(parent_key, parent_chain_code, index):
    if index >= 2**31:  # Hardened
        data = b'\x00' + parent_key
    else:
        data = private_to_public_key(parent_key)
    data += index.to_bytes(4, 'big')
    h = hmac_sha512(parent_chain_code, data)
    child_key = (int.from_bytes(h[:32], 'big') + int.from_bytes(parent_key, 'big')) % SECP256k1.order
    child_chain_code = h[32:]
    return child_key.to_bytes(32, 'big'), child_chain_code

def derive_path(seed, path="m/86'/0'/0'/0/0"):
    if not path.startswith("m/"):
        raise ValueError("Path must start with 'm/'")
    segments = path.split('/')[1:]
    key, chain = derive_master_key(seed)
    for seg in segments:
        hardened = seg.endswith("'")
        idx = int(seg.rstrip("'"))
        if hardened:
            idx += 2**31
        key, chain = CKDpriv(key, chain, idx)
    return key

# ----------------------------
# Address Types
# ----------------------------
def p2pkh_address(pubkey):
    payload = hash160(pubkey)
    return base58.b58encode_check(b'\x00' + payload).decode()

def p2sh_p2wpkh_address(pubkey):
    witness_script = b'\x00\x14' + hash160(pubkey)
    script_hash = hash160(witness_script)
    return base58.b58encode_check(b'\x05' + script_hash).decode()

def p2wpkh_address(pubkey):
    program = hash160(pubkey)
    return bech32.encode('bc', 0, program)

def p2tr_address(pubkey):
    """Taproot: bc1p... (BIP-86) - uses x-only pubkey (32 bytes)"""
    # Remove parity byte → x-only (32 bytes)
    x_only = pubkey[1:]  # pubkey is 33 bytes → take 32-byte x
    return bech32.encode('bc', 1, x_only)  # witness version 1

def private_key_to_wif(privkey, compressed=True):
    extended = b'\x80' + privkey
    if compressed:
        extended += b'\x01'
    return base58.b58encode_check(extended).decode()

# ----------------------------
# MAIN
# ----------------------------
def main():
    print("\n")
    print("=" * 65)
    print("ULTIMATE Bitcoin Wallet Generator (Legacy + SegWit + Taproot)")
    print("=" * 65)
    print("\n")
    print("*** RUN THIS SCRIPT & BACKUP OFFLINE! ***\n")
    mnemonic = generate_mnemonic(128)
    print(f"\n12-Word Mnemonic:\n   {mnemonic}\n")
    print("Controls ALL addresses below.\n")

    seed = mnemonic_to_seed(mnemonic)

    paths = {
        "Legacy (P2PKH)":           "m/44'/0'/0'/0/0",
        "Nested SegWit (P2SH)":     "m/49'/0'/0'/0/0",
        "Native SegWit (P2WPKH)":   "m/84'/0'/0'/0/0",
        "Taproot (P2TR)":           "m/86'/0'/0'/0/0"   # BIP-86
    }

    print("First receiving address (index 0) for each type:\n")

    for name, path in paths.items():
        privkey = derive_path(seed, path)
        pubkey = private_to_public_key(privkey)
        wif = private_key_to_wif(privkey)

        print(f"{name}")
        print(f"   Path  : {path}")
        print(f"   Address: ", end="")

        if "Legacy" in name:
            print(p2pkh_address(pubkey))
        elif "Nested" in name:
            print(p2sh_p2wpkh_address(pubkey))
        elif "Native" in name:
            print(p2wpkh_address(pubkey))
        elif "Taproot" in name:
            print(p2tr_address(pubkey))

        print(f"   WIF   : {wif}")
        print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")