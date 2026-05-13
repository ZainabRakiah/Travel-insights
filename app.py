"""Run TravelEx Insights from the project root: `python app.py`"""
import os
from pathlib import Path
import sys

_app_dir = Path(__file__).resolve().parent / "travelex-insights"
sys.path.insert(0, str(_app_dir))

from app import app  # noqa: E402

if __name__ == "__main__":
    # Default 5001: macOS often reserves 5000 for AirPlay Receiver.
    port = int(os.environ.get("PORT", "5001"))
    app.run(debug=True, port=port)
