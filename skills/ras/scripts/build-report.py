"""Convenience wrapper for hosts that invoke skill scripts directly."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from ras_engine.cli import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
