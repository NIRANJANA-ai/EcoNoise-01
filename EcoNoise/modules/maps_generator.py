import os
import json
import folium
from statistics import mean

# Map coordinates for locations (update with your real coords)
LOCATION_COORDS = {
    "Central_Park": (12.9716, 77.5946),
    # Add your real locations here: "CityMarket": (lat, lon)
}

def load_all_location_records(output_base="output"):
    all_data = {}
    if not os.path.exists(output_base):
        return all_data
    for name in os.listdir(output_base):
        loc_path = os.path.join(output_base, name)
        if not os.path.isdir(loc_path):
            continue
        rec_file = os.path.join(loc_path, "records.json")
        if os.path.exists(rec_file):
            try:
                with open(rec_file, "r") as f:
                    arr = json.load(f)
                all_data[name] = arr
            except:
                all_data[name] = []
        else:
            latest = os.path.join(loc_path, "latest.json")
            if os.path.exists(latest):
                try:
                    with open(latest, "r") as f:
                        r = json.load(f)
                    all_data[name] = [r]
                except:
                    all_data[name] = []
    return all_data

def compute_location_avg_harm(all_data):
    out = []
    for loc, recs in all_data.items():
        harms = []
        for r in recs:
            h = r.get("Harm Rate") or r.get("harm_rate") or r.get("HarmRate") or 0
            try:
                harms.append(float(h))
            except:
                pass
        avg = float(mean(harms)) if harms else 0.0
        out.append({"location": loc, "avg_harm": avg, "count": len(harms)})
    out.sort(key=lambda x: x["avg_harm"], reverse=True)
    return out

def generate_rankings_file(output_base="output", filename="rankings.json"):
    all_data = load_all_location_records(output_base)
    rankings = compute_location_avg_harm(all_data)
    out_path = os.path.join(output_base, filename)
    os.makedirs(output_base, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(rankings, f, indent=2)
    return out_path

def _color_by_harm(h):
    if h >= 80: return "red"
    if h >= 40: return "orange"
    return "green"

def generate_combined_map(output_base="output", map_filename="map.html"):
    all_data = load_all_location_records(output_base)
    rankings = compute_location_avg_harm(all_data)
    # default center fallback
    center = (12.9716, 77.5946)
    m = folium.Map(location=center, zoom_start=13, tiles="OpenStreetMap")
    for r in rankings:
        loc = r["location"]
        avg = r["avg_harm"]
        coords = LOCATION_COORDS.get(loc, center)
        color = _color_by_harm(avg)
        radius = 6 + (avg / 10.0)
        folium.CircleMarker(location=coords, radius=radius, color=color, fill=True,
                            fill_opacity=0.7, popup=f"{loc} (avg harm: {avg:.2f})").add_to(m)
    out_path = os.path.join(output_base, map_filename)
    os.makedirs(output_base, exist_ok=True)
    m.save(out_path)
    return out_path



