# GenBitcoinWallet
🚀 Here is a simple and lightweight python script that generates Bitcoin wallet offline. 

# Ultimate Bitcoin Wallet Generator (Legacy + SegWit + Taproot)
Generate **all major Bitcoin address types** from a single **12-word BIP-39 mnemonic**:

| Type | Prefix | Path | Standard |
|------|--------|------|----------|
| Legacy | `1...` | `m/44'/0'/0'/0/0` | [BIP-44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) |
| Nested SegWit | `3...` | `m/49'/0'/0'/0/0` | [BIP-49](https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki) |
| Native SegWit | `bc1q...` | `m/84'/0'/0'/0/0` | [BIP-84](https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki) |
| Taproot | `bc1p...` | `m/86'/0'/0'/0/0` | [BIP-86](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki) |

All addresses are derived from the **same seed** — perfect for learning, testing, or creating **multi-format paper wallets**.

## Features

- 100% **offline-capable** (air-gapped safe)
- BIP-32 hierarchical deterministic derivation
- Full BIP-39 mnemonic → seed → key path support
- Outputs:
  - 12-word recovery phrase
  - Private key (hex)
  - **WIF** (Wallet Import Format)
  - **All 4 address types**
- No external dependencies beyond standard libraries

---

## Requirements

```bash
pip install mnemonic ecdsa bech32 base58
```

## Usage
```bash
python bitcoin_wallet.py
```
RUN THIS SCRIPT & BACKUP **OFFLINE**!

---


## Example Output
```text
=================================================================
ULTIMATE Bitcoin Wallet Generator (Legacy + SegWit + Taproot)
=================================================================


*** RUN THIS SCRIPT & BACKUP OFFLINE! ***


12-Word Mnemonic:
   current vital panel blame inspire orchard cheese legal daring burst trick plug

Controls ALL addresses below.

First receiving address (index 0) for each type:

Legacy (P2PKH)
   Path  : m/44'/0'/0'/0/0
   Address: 1DERHi4...
   WIF   : KyWSh263...

Nested SegWit (P2SH)
   Path  : m/49'/0'/0'/0/0
   Address: 3Fo56vGLvr...
   WIF   : Kz55BrC...

Native SegWit (P2WPKH)
   Path  : m/84'/0'/0'/0/0
   Address: bc1quman...
   WIF   : KzHV2zmey...

Taproot (P2TR)
   Path  : m/86'/0'/0'/0/0
   Address: bc1ptfw7c...
   WIF   : L3yyimzN8v...
```
---
## Security Warning
This tool generates real Bitcoin keys.

Never run it on an online machine with funds.

Use only on air-gapped or trusted offline systems.

The mnemonic controls all generated addresses. 

Store it securely.

