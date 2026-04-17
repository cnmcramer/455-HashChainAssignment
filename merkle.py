"""
Merkle Hash Tree for File Integrity Checking
============================================
Usage:
    python merkle.py file1 file2 file3 ...
    python merkle.py --demo        (runs a built-in demo)
"""

import hashlib
import sys
import os


# ── Hash Utilities ────────────────────────────────────────────────────────────

def hash_data(data: bytes) -> str:
    """Return the SHA-1 hex digest of raw bytes."""
    return hashlib.sha1(data).hexdigest()


def hash_file(filepath: str) -> str:
    """Read a file in binary mode and return its SHA-1 hash."""
    with open(filepath, 'rb') as f:
        return hash_data(f.read())


# ── Merkle Tree ───────────────────────────────────────────────────────────────

def build_merkle_tree(file_paths: list) -> tuple:
    """
    Build a Merkle tree from a list of file paths.

    Returns:
        (top_hash, tree_levels)
        top_hash    – the single root hash string
        tree_levels – list of levels (each level is a list of hashes),
                      from leaves to root, useful for printing the tree.
    """
    if not file_paths:
        raise ValueError("No file paths provided.")

    # Level 0: leaf hashes (one per file)
    leaves = []
    for fp in file_paths:
        if not os.path.isfile(fp):
            raise FileNotFoundError(f"File not found: {fp}")
        leaves.append(hash_file(fp))

    tree_levels = [leaves]
    nodes = leaves[:]

    # Build upward until only one node remains
    while len(nodes) > 1:
        if len(nodes) % 2 != 0:
            nodes.append(nodes[-1])          # duplicate last node if odd count

        next_level = []
        for i in range(0, len(nodes), 2):
            combined = (nodes[i] + nodes[i + 1]).encode()
            next_level.append(hash_data(combined))

        tree_levels.append(next_level)
        nodes = next_level

    return nodes[0], tree_levels


# ── Display Helpers ───────────────────────────────────────────────────────────

def print_tree(file_paths: list, tree_levels: list):
    """Print the full Merkle tree level by level."""
    print("\n" + "=" * 60)
    print("  MERKLE TREE  (bottom → top)")
    print("=" * 60)

    labels = [f"  Level 0 (Leaves — {len(file_paths)} file(s))"]
    for i in range(1, len(tree_levels)):
        labels.append(f"  Level {i}")
    labels[-1] += "  ← TOP HASH"

    for level_idx, (level, label) in enumerate(zip(tree_levels, labels)):
        print(f"\n{label}")
        if level_idx == 0:
            for fp, h in zip(file_paths, level):
                print(f"    {h}  ←  {os.path.basename(fp)}")
            # If a node was duplicated, note it
            if len(level) < len(tree_levels[1]) * 2 - 1:
                pass  # nothing to show for internal duplication
        else:
            for h in level:
                print(f"    {h}")

    print("\n" + "=" * 60)
    print(f"  TOP HASH: {tree_levels[-1][0]}")
    print("=" * 60 + "\n")


# ── Demo Mode ─────────────────────────────────────────────────────────────────

def run_demo():
    """Create temporary files, compute Top Hash, tamper one, recompute."""
    import tempfile

    print("\n*** DEMO MODE ***\n")
    tmp_dir = tempfile.mkdtemp()

    # Create 4 sample files
    file_contents = {
        "L1.txt": b"This is file L1.",
        "L2.txt": b"This is file L2.",
        "L3.txt": b"This is file L3.",
        "L4.txt": b"This is file L4.",
    }

    file_paths = []
    for name, content in file_contents.items():
        path = os.path.join(tmp_dir, name)
        with open(path, 'wb') as f:
            f.write(content)
        file_paths.append(path)

    print("Files created:")
    for fp in file_paths:
        print(f"  {fp}")

    # ── Before tampering ──
    print("\n--- BEFORE MODIFICATION ---")
    top_hash_before, tree_before = build_merkle_tree(file_paths)
    print_tree(file_paths, tree_before)

    # ── Tamper with L1.txt ──
    tampered_file = file_paths[0]
    print(f">>> Tampering with: {os.path.basename(tampered_file)}")
    with open(tampered_file, 'ab') as f:
        f.write(b" [TAMPERED DATA]")

    # ── After tampering ──
    print("\n--- AFTER MODIFICATION ---")
    top_hash_after, tree_after = build_merkle_tree(file_paths)
    print_tree(file_paths, tree_after)

    # ── Result ──
    print("INTEGRITY CHECK RESULT:")
    if top_hash_before == top_hash_after:
        print("  ✓  Top hashes MATCH — files are unchanged.")
    else:
        print("  ✗  Top hashes DO NOT MATCH — tampering detected!")
        print(f"     Before: {top_hash_before}")
        print(f"     After:  {top_hash_after}")

    # Cleanup
    for fp in file_paths:
        os.remove(fp)
    os.rmdir(tmp_dir)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--demo":
        run_demo()
        return

    file_paths = sys.argv[1:]

    try:
        top_hash, tree_levels = build_merkle_tree(file_paths)
        print_tree(file_paths, tree_levels)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
