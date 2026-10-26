"""Run each standard works extraction script in sequence."""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
EXTRACTION_SCRIPTS = (
    "extract_bofm.py",
    "extract_ot.py",
    "extract_nt.py",
    "extract_dc.py",
    "extract_pgp.py",
)


def main() -> None:
    for script_name in EXTRACTION_SCRIPTS:
        script_path = SCRIPT_DIR / script_name
        print(f"\n=== Running {script_name} ===", flush=True)
        # check=True stops the pipeline immediately if an extraction fails.
        subprocess.run([sys.executable, str(script_path)], check=True)

    print("\nAll standard works extractions completed.")


if __name__ == "__main__":
    main()
