import json
import os
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

_DATA_PATH = Path(__file__).resolve().parent / "data.json"


def _load_travel_catalog():
    with open(_DATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    by_lower = {name.lower(): (name, payload) for name, payload in raw.items()}
    return raw, by_lower


TRAVEL_DATA, _TRAVEL_BY_LOWER = _load_travel_catalog()

GENERIC = {
    "tagline": "Explore local highlights at your own pace.",
    "food": ["Local Food"],
    "hotel": ["Standard Hotel"],
    "places": ["City Attractions"],
}


def _template_base(**extra):
    base = {"destinations": sorted(TRAVEL_DATA.keys())}
    base.update(extra)
    return base


def _resolve_destination(user_text):
    """Return (display_name, catalog_entry_or_generic)."""
    key = user_text.strip()
    if not key:
        return "", GENERIC
    hit = _TRAVEL_BY_LOWER.get(key.lower())
    if hit:
        return hit[0], {**hit[1]}
    return key, {**GENERIC}


def _tips_for(destination, trip_type, days, budget, tagline):
    tips = [tagline]
    per_day = budget // days if days else 0
    if days >= 7:
        tips.append("Week-long trip: add one light day mid-trip to avoid burnout.")
    elif days <= 2:
        tips.append("Short break: pick one anchor sight per day and keep travel windows wide.")
    if trip_type == "Budget Trip":
        tips.append("Budget: compare stays on maps; slightly away from hotspots often saves a lot.")
    elif trip_type == "Luxury Trip":
        tips.append("Luxury: book airport/station transfers in advance for a smoother arrival.")
    else:
        tips.append("Comfort: mix one splurge meal or stay with simpler options nearby.")
    if per_day < 2000:
        tips.append(f"About ₹{per_day}/day after dividing budget by days — prioritize free walks and public parks.")
    return tips


@app.route("/")
def home():
    return render_template("index.html", **_template_base())


@app.route("/plan", methods=["POST"])
def plan():
    destination_raw = (request.form.get("destination") or "").strip()
    if not destination_raw:
        return render_template(
            "index.html",
            **_template_base(error="Please enter a destination."),
        )

    try:
        budget = int(request.form.get("budget", ""))
        days = int(request.form.get("days", ""))
    except (TypeError, ValueError):
        return render_template(
            "index.html",
            **_template_base(error="Budget and days must be whole numbers."),
        )

    if budget < 0:
        return render_template(
            "index.html",
            **_template_base(error="Budget cannot be negative."),
        )

    if days < 1:
        return render_template(
            "index.html",
            **_template_base(error="Number of days must be at least 1."),
        )

    destination, data = _resolve_destination(destination_raw)

    if budget < 5000:
        trip_type = "Budget Trip"
    elif budget < 15000:
        trip_type = "Comfort Trip"
    else:
        trip_type = "Luxury Trip"

    estimated_cost = budget // days
    tagline = data.get("tagline") or GENERIC["tagline"]
    tips = _tips_for(destination, trip_type, days, budget, tagline)

    return render_template(
        "index.html",
        **_template_base(
            result=True,
            destination=destination,
            budget=budget,
            days=days,
            trip_type=trip_type,
            estimated_cost=estimated_cost,
            food=data["food"],
            hotels=data["hotel"],
            places=data["places"],
            tips=tips,
        ),
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(debug=True, port=port)
