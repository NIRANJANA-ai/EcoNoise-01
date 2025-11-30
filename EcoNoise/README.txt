EcoNoise is a real-time environmental noise monitoring system that tracks noise levels across multiple locations. It provides interactive dashboards, monthly reports, and harm rate rankings to help users understand and manage noise pollution. The system supports data export, multi-location monitoring, and generates insights that can assist in decision-making for noise management and environmental planning.

FEATURES:
Real-Time Noise Monitoring: Continuously track noise levels from multiple locations.
Harm Rate Ranking: Evaluate and rank areas based on noise impact.
Monthly Analytics Reports: Generate CSV and visual reports summarizing noise patterns.
Multi-Location Support: Monitor noise from multiple sensors or locations simultaneously.
Interactive Dashboard: Visualize data, trends, and reports in a user-friendly interface.
Data Export: Save reports in C:/PythonReports for future analysis.

TECH STACK:
Backend: Python, Flask
Data Analysis: Pandas, NumPy
Machine Learning / AI: TensorFlow (optional, for advanced noise classification)
Frontend: HTML, CSS, JavaScript (Dashboard)
Reporting: CSV generation, real-time charts

INSTALLATION:
Create a virtual environment to activate it:
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the application:
python app.py

Usage:
Open your browser and navigate to http://localhost:5000 to access the dashboard.
View real-time noise levels for all connected locations.
Generate monthly reports from the Reports section.
Use the Harm Rate Ranking to identify high-noise areas.

FOLDER STRUCTURE:
EcoNoise/
│
├── main_continuous.py                  # Main Flask application
├── modules/                # Python modules (e.g., noise analysis, report generation)
├── templates/              # HTML templates for dashboard
├── static/                 # CSS, JS, and images
├── C:/PythonReports/       # Generated reports folder
└── requirements.txt        # Python dependencies

CONTRIBUTING:
Contributions are welcome! Please fork the repository and submit a pull request with improvements or new features.

