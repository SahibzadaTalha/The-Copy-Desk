"""
app.py
Flask backend for The Copy Desk web UI.
Serves templates/index.html + static/style.css + static/script.js, and
exposes /api/generate which the frontend calls via fetch().
"""

import asyncio

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from config import PLATFORM_PROFILES, TONE_PARAMETERS, resolve_generation_params
from engine import generate_many

load_dotenv()

app = Flask(__name__)

TEMP_LEVELS = [
    ("Conservative", 0.2),
    ("Balanced", 0.6),
    ("Creative", 0.95),
]


@app.route("/")
def index():
    return render_template("index.html", platforms=PLATFORM_PROFILES, tones=TONE_PARAMETERS)


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True, silent=True) or {}

    product = (data.get("product") or "").strip()
    description = (data.get("description") or "").strip()
    tone = (data.get("tone") or "").strip().lower()
    platforms = [p.strip().lower() for p in data.get("platforms") or []]
    compare_mode = bool(data.get("compare_mode"))

    if not product or not description or not tone or not platforms:
        return jsonify({"error": "Product, description, tone, and at least one platform are required."}), 400

    unknown = [p for p in platforms if p not in PLATFORM_PROFILES]
    if unknown:
        return jsonify({"error": f"Unknown platform(s): {', '.join(unknown)}"}), 400

    try:
        if compare_mode:
            platform = platforms[0]
            limit = PLATFORM_PROFILES[platform].max_characters
            requests_payload = [
                {
                    "product_name": product, "product_description": description,
                    "platform": platform, "tone": tone, "temperature_override": t,
                }
                for _, t in TEMP_LEVELS
            ]
            results = asyncio.run(generate_many(requests_payload))
            gen_params = resolve_generation_params(platform, tone)

            output = [
                {
                    "platform": r.platform,
                    "label": label,
                    "temperature": temp,
                    "top_p": gen_params["top_p"],
                    "text": r.full_text,
                    "char_count": r.character_count,
                    "limit": limit,
                    "compliant": r.compliance_check(limit),
                }
                for (label, temp), r in zip(TEMP_LEVELS, results)
            ]
            return jsonify({"mode": "compare", "results": output})

        requests_payload = [
            {"product_name": product, "product_description": description, "platform": p, "tone": tone}
            for p in platforms
        ]
        results = asyncio.run(generate_many(requests_payload))

        output = []
        for r in results:
            gen_params = resolve_generation_params(r.platform, tone)
            limit = PLATFORM_PROFILES[r.platform].max_characters
            output.append({
                "platform": r.platform,
                "label": None,
                "temperature": gen_params["temperature"],
                "top_p": gen_params["top_p"],
                "text": r.full_text,
                "char_count": r.character_count,
                "limit": limit,
                "compliant": r.compliance_check(limit),
            })
        return jsonify({"mode": "normal", "results": output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)