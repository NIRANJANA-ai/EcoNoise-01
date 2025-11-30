import time
import json
import os
from datetime import datetime
from modules import recorder, classifier, harm_rate, report_generator

# === CONFIG ===
# Set per device: either edit LOCATION or set env var ECO_LOCATION
LOCATION = os.environ.get("ECO_LOCATION", "Central_Park")
RECORD_SECONDS = 3
CYCLE_INTERVAL = 5      # seconds between cycles
OUTPUT_BASE = "output"  # shared folder; ensure dashboard server can read this

# Derived paths
LOC_FOLDER = os.path.join(OUTPUT_BASE, LOCATION.replace(" ", "_"))
LATEST_FILE = os.path.join(LOC_FOLDER, "latest.json")
RECORDS_FILE = os.path.join(LOC_FOLDER, "records.json")

os.makedirs(LOC_FOLDER, exist_ok=True)

def append_record(record):
    if not os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "w") as f:
            json.dump([record], f, indent=2)
        return
    try:
        with open(RECORDS_FILE, "r") as f:
            arr = json.load(f)
    except:
        arr = []
    arr.append(record)
    with open(RECORDS_FILE, "w") as f:
        json.dump(arr, f, indent=2)

def write_latest(record):
    with open(LATEST_FILE, "w") as f:
        json.dump(record, f, indent=2)

if __name__ == "__main__":
    print(f"[main] Starting monitoring (location={LOCATION}). Press Ctrl+C to stop.")

    interpreter = classifier.load_model("models/sound_classifier.tflite")
    cycle_no = 0
    all_records_local = []

    try:
        while True:
            cycle_no += 1
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Capture (memory-only)
            samples, sr, _ = recorder.capture_audio(RECORD_SECONDS)

            # Classify
            predicted, conf = classifier.classify_audio(interpreter, samples, sr)

            # Harm
            harm = harm_rate.compute_harm_rate(predicted)

            record = {
                "Location": LOCATION,
                "Timestamp": ts,
                "Predicted Class": predicted,
                "Confidence": float(conf),
                "Harm Rate": float(harm),
                "cycle": cycle_no
            }

            all_records_local.append(record)
            append_record(record)
            # include total_cycles in latest snapshot
            record["total_cycles"] = len(all_records_local)
            write_latest(record)

            print(f"[main] {ts} -> {predicted} (conf={conf}) at {LOCATION}")

            time.sleep(CYCLE_INTERVAL)

    except KeyboardInterrupt:
        print("[main] Stopped by user. Generating local reports...")

    # Generate final per-device reports (optional)
    try:
        report_generator.generate_csv_report(all_records_local, filename=f"{LOCATION.replace(' ','_')}_eco_report.csv")
        report_generator.generate_pdf_report(all_records_local, filename=f"{LOCATION.replace(' ','_')}_eco_report.pdf")
        print("[main] Local reports created.")
    except Exception as e:
        print("[main] Report generation error:", e)
