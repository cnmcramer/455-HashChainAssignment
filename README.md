# Merkle Hash Tree - CIS455 01 Project

By: [Your Name]

The file **merkle.py** contains Python code that will utilize the Merkle Hash Tree model to compute the Top Hash. Hashing is done using SHA-1.

## Usage

To run the built-in demo:

```
python merkle.py --demo
```

To run on your own files:

```
python merkle.py file1.txt file2.txt file3.txt ...
```

The program creates temporary files, computes the Top Hash for the original files, then tampers with one file and recomputes the Top Hash. The before and after hashes are compared — if they don't match, tampering is detected. Below is an example of the demo output:

```
*** DEMO MODE ***

Files created:
  C:\Users\User\AppData\Local\Temp\tmph7qt5ht7\L1.txt
  C:\Users\User\AppData\Local\Temp\tmph7qt5ht7\L2.txt
  C:\Users\User\AppData\Local\Temp\tmph7qt5ht7\L3.txt
  C:\Users\User\AppData\Local\Temp\tmph7qt5ht7\L4.txt

--- BEFORE MODIFICATION ---

============================================================
  MERKLE TREE  (bottom → top)
============================================================

  Level 0 (Leaves — 4 file(s))
    f0cb65ef276d63571366dd5a7c88f09160b076b2  ←  L1.txt
    7f186c2a6434572bc5b1026b5fe28ba76c06e6bb  ←  L2.txt
    5b3a1a9b8037ffd5e7f0670b1d22724c037a9bec  ←  L3.txt
    0241b0a1cdf753a70f7eeec626b06fa906008364  ←  L4.txt

  Level 1
    5e7334e49f9def0c7252181f0e1f0df08c31b493
    e488c65099de8135d8b315d9fa5b2fa5f6f788b5

  Level 2  ← TOP HASH
    388324e5114930ec528b5d8ea745f002c2aab196

============================================================
  TOP HASH: 388324e5114930ec528b5d8ea745f002c2aab196
============================================================

>>> Tampering with: L1.txt

--- AFTER MODIFICATION ---

============================================================
  MERKLE TREE  (bottom → top)
============================================================

  Level 0 (Leaves — 4 file(s))
    70d378c1121b5cd136227a80efa91ff401265a39  ←  L1.txt
    7f186c2a6434572bc5b1026b5fe28ba76c06e6bb  ←  L2.txt
    5b3a1a9b8037ffd5e7f0670b1d22724c037a9bec  ←  L3.txt
    0241b0a1cdf753a70f7eeec626b06fa906008364  ←  L4.txt

  Level 1
    0eab85a7aa107ae417d7302030435a724da3bf48
    e488c65099de8135d8b315d9fa5b2fa5f6f788b5

  Level 2  ← TOP HASH
    44e129458e28a9b55b55694ca1a8fe82712eaf9a

============================================================
  TOP HASH: 44e129458e28a9b55b55694ca1a8fe82712eaf9a
============================================================

INTEGRITY CHECK RESULT:
  ✗  Top hashes DO NOT MATCH — tampering detected!
     Before: 388324e5114930ec528b5d8ea745f002c2aab196
     After:  44e129458e28a9b55b55694ca1a8fe82712eaf9a
```

## Disclaimer

*This code was created with the assistance of Claude, an AI assistant made by Anthropic. All code has been reviewed and tested for correctness. The author takes full responsibility for the final implementation and any modifications made thereafter.*

Read more on Merkle Trees here: https://www.geeksforgeeks.org/dsa/introduction-to-merkle-tree/