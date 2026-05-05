"""
Builds the smarteval/ dataset folder from the 6 batch outputs.

Structure produced:
  smarteval/
  ├── requirement_fsm_code.jsonl  (copied from applications/)
  ├── smarteval_contracts.jsonl   (all contract_NNN.json files combined)
  └── contracts/
      ├── 0001/
      │   ├── contract.sol
      │   └── quality_evaluation.json
      ├── 0002/
      │   ...
"""

import glob
import json
import os
import shutil

BASE = r"c:\Users\abhin\OneDrive\Desktop\Research\Agentics-Research"
BATCHES_ROOT = os.path.join(BASE, "applications", "contract-translator", "output")
OUTPUT_DIR = os.path.join(BASE, "smarteval")
CONTRACTS_DIR = os.path.join(OUTPUT_DIR, "contracts")

BATCHES = [
    "batch_20260202_234733",
    "batch_20260202_234738",
    "batch_20260202_234742",
    "batch_20260202_234746",
    "batch_20260202_234751",
    "batch_20260202_234755",
]


def main():
    os.makedirs(CONTRACTS_DIR, exist_ok=True)

    # ── 1. Copy requirement_fsm_code.jsonl ──────────────────────────────────
    src_fsm = os.path.join(BASE, "applications", "requirement_fsm_code.jsonl")
    dst_fsm = os.path.join(OUTPUT_DIR, "requirement_fsm_code.jsonl")
    shutil.copy2(src_fsm, dst_fsm)
    print(f"Copied requirement_fsm_code.jsonl")

    # ── 2. Build smarteval_contracts.jsonl from all contract_NNN.json files ─
    jsonl_path = os.path.join(OUTPUT_DIR, "smarteval_contracts.jsonl")
    total_contracts_json = 0
    with open(jsonl_path, "w", encoding="utf-8") as out_f:
        for batch in BATCHES:
            batch_path = os.path.join(BATCHES_ROOT, batch)
            # Glob only the top-level contract_*.json files (not inside subdirs)
            pattern = os.path.join(batch_path, "contract_*.json")
            files = sorted(glob.glob(pattern))
            for fpath in files:
                with open(fpath, "r", encoding="utf-8") as in_f:
                    data = json.load(in_f)
                out_f.write(json.dumps(data, ensure_ascii=False) + "\n")
                total_contracts_json += 1
            print(f"  {batch}: added {len(files)} JSON records")
    print(f"smarteval_contracts.jsonl written — {total_contracts_json} total records")

    # ── 3. Copy contract folders into contracts/XXXX/ ───────────────────────
    counter = 1
    for batch in BATCHES:
        batch_path = os.path.join(BATCHES_ROOT, batch)
        # Only include subdirectories that contain at least a .sol or quality_evaluation.json
        subdirs = sorted(
            d for d in os.listdir(batch_path)
            if os.path.isdir(os.path.join(batch_path, d))
        )
        batch_copied = 0
        for subdir in subdirs:
            subdir_path = os.path.join(batch_path, subdir)

            sol_files = glob.glob(os.path.join(subdir_path, "*.sol"))
            quality_eval = os.path.join(subdir_path, "quality_evaluation.json")

            # Skip folders that have neither (shouldn't happen, but be safe)
            if not sol_files and not os.path.exists(quality_eval):
                print(f"  SKIP {subdir} (no .sol or quality_evaluation.json)")
                continue

            folder_name = f"{counter:04d}"
            dest_path = os.path.join(CONTRACTS_DIR, folder_name)
            os.makedirs(dest_path, exist_ok=True)

            if sol_files:
                shutil.copy2(sol_files[0], os.path.join(dest_path, "contract.sol"))

            if os.path.exists(quality_eval):
                shutil.copy2(quality_eval, os.path.join(dest_path, "quality_evaluation.json"))

            counter += 1
            batch_copied += 1

        print(f"  {batch}: copied {batch_copied} contract folders")

    total_folders = counter - 1
    print(f"\nDone. contracts/ contains {total_folders} folders (0001 – {total_folders:04d})")


if __name__ == "__main__":
    main()
