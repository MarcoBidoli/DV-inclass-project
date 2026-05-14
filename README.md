# ⛽ Italy Fuel Price Dashboard

An interactive Dash/Plotly dashboard to visualize and analyze fuel price trends across Italy (2018-2023). This dashboard processes station-level daily data to provide regional insights via heatmaps, regional rankings (bar race), and price distributions.

## 🌟 Features

- **Price Heatmap**: A choropleth map of Italy showing average monthly prices per region.
- **Regional Ranking (Bar Race)**: An animated bar chart that sorts regions from most to least expensive.
- **Price Distribution**: A histogram showing the frequency of prices for the selected fuel type and period.
- **Interactive Controls**:
  - **Play/Pause**: Animate the dashboard over time.
  - **Filters**: Filter by Fuel Type (Benzina, Gasolio, GPL, etc.), Region, and Year.
  - **Time Slider**: Manually scrub through months from 2018 to 2023.

## 📋 Requirements

- Python 3.8 or higher
- `pandas`
- `dash`
- `plotly`
- `numpy`

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd DV-inclass-project
```

### 2. Create a Virtual Environment

#### macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Data Processing (One-time)
The raw data is large (194M rows). Run the aggregation script to generate the summarized files used by the dashboard:
```bash
python aggregate_data.py
```
*Note: This may take several minutes depending on your hardware.*

### 5. Run the Dashboard
```bash
python app.py
```
Once running, open your browser and navigate to: `http://127.0.0.1:8050/`

## 📂 Project Structure

- `app.py`: The main Dash application.
- `aggregate_data.py`: Script to process raw CSV files into optimized summaries.
- `limits_IT_regions.geojson`: GeoJSON file for Italian regional boundaries.
- `prezzi_daily_by_year/`: Folder containing raw yearly CSV data.
- `summary_data.csv`: Generated regional monthly averages.
- `distribution_data.csv`: Generated representative price samples.

---
*Created for the Data Visualization Course.*
