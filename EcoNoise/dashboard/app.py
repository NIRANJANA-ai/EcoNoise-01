import os
import sys
import json
from flask import Flask, render_template, send_from_directory, jsonify, abort
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)
from modules import maps_generator

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT = os.path.join(BASE, "output")
REPORTS = "C:/PythonReports"

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map_page():
    return render_template("map_view.html")

@app.route("/rankings")
def rankings_page():
    return render_template("rankings.html")

@app.route("/reports")
def reports_page():
    return render_template("reports.html")

@app.route("/monthly")
def monthly_page():
    return render_template("monthly.html")

# Combined latest snapshot (most recent across locations)
@app.route("/api/snapshot")
def api_snapshot():
    all_data = maps_generator.load_all_location_records(OUTPUT)
    latest = None
    for loc, recs in all_data.items():
        for r in recs:
            ts = r.get("Timestamp") or r.get("timestamp")
            if not ts:
                continue
            if latest is None or ts > latest.get("Timestamp", ""):
                latest = r
    if latest is None:
        return jsonify({"error": "no snapshot yet"})
    resp = {
        "location": latest.get("Location"),
        "sound_class": latest.get("Predicted Class"),
        "confidence": latest.get("Confidence"),
        "harm_rate": latest.get("Harm Rate"),
        "timestamp": latest.get("Timestamp"),
        "total_cycles": sum(len(v) for v in all_data.values())
    }
    return jsonify(resp)

# Per-location list
@app.route("/api/locations")
def api_locations():
    out = []
    all_data = maps_generator.load_all_location_records(OUTPUT)
    for loc, recs in all_data.items():
        latest = recs[-1] if recs else {}
        out.append({
            "location": loc,
            "latest": {
                "timestamp": latest.get("Timestamp"),
                "predicted_class": latest.get("Predicted Class"),
                "confidence": latest.get("Confidence"),
                "harm_rate": latest.get("Harm Rate")
            },
            "count": len(recs)
        })
    return jsonify({"locations": out})

# rankings
@app.route("/api/rankings")
def api_rankings():
    path = os.path.join(OUTPUT, "rankings.json")
    if not os.path.exists(path):
        maps_generator.generate_rankings_file(OUTPUT)
    try:
        with open(path, "r") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"rankings": []})

# monthly analytics aggregated for dashboard
@app.route("/api/monthly")
def api_monthly():
    all_data = maps_generator.load_all_location_records(OUTPUT)
    flat = []
    for loc, recs in all_data.items():
        for r in recs:
            rr = r.copy()
            rr["Location"] = loc
            flat.append(rr)
    from collections import defaultdict
    daily = defaultdict(list)
    for r in flat:
        ts = r.get("Timestamp")
        if not ts:
            continue
        date = ts.split(" ")[0]
        try:
            daily[date].append(float(r.get("Harm Rate", 0)))
        except:
            daily[date].append(0.0)
    dates = sorted(daily.keys())
    series = [{"date": d, "avg_harm": (sum(daily[d]) / len(daily[d])) if daily[d] else 0.0, "count": len(daily[d])} for d in dates]
    sound_counts = {}
    for r in flat:
        cls = r.get("Predicted Class") or r.get("predicted_class") or "unknown"
        sound_counts[cls] = sound_counts.get(cls, 0) + 1
    return jsonify({"daily": series, "sound_counts": sound_counts, "locations_count": len(all_data)})

# downloads
@app.route("/download/csv")
def download_csv():
    file_path = os.path.join(REPORTS, "eco_report.csv")
    if not os.path.exists(file_path):
        abort(404, "CSV report not found")
    return send_from_directory(REPORTS, "eco_report.csv", as_attachment=True)

@app.route("/download/pdf")
def download_pdf():
    file_path = os.path.join(REPORTS, "eco_report.pdf")
    if not os.path.exists(file_path):
        abort(404, "PDF report not found")
    return send_from_directory(REPORTS, "eco_report.pdf", as_attachment=True)

@app.route("/map_content")
def map_content():
    path = os.path.join(OUTPUT, "map.html")
    if not os.path.exists(path):
        try:
            maps_generator.generate_combined_map(OUTPUT, map_filename="map.html")
        except Exception:
            return "<h2>No map generated yet.</h2>"
    return send_from_directory(OUTPUT, "map.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)




