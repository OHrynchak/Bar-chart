## CSV Data Visualization Application (CSV Bar Chart App)

This Django application is designed to read structured CSV files, group data by regions, and generate Bar Charts using the Pandas and Matplotlib libraries. The charts are dynamically generated and served to the user as PNG images.

### Key Technologies
* **Backend:** Python, Django

* **Data Processing:** Pandas

* **Visualization:** Matplotlib (Agg backend)

### Installation and Setup

**1.Requirements**

Ensure you have Python and Git installed.

**2.Clone and Change Directory**

```bash
git clone https://github.com/OHrynchak/Bar-chart.git
cd <project_folder_name>
```

**3.Create and Activate Virtual Environment**

To isolate dependencies, create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# For Windows PowerShell:
.\venv\Scripts\Activate.ps1

# For macOS/Linux or Git Bash:
source venv/bin/activate
```

**4.Install Dependencies**

After activation, install the necessary libraries (ensure that the `requirements.txt` file contains `django`, `pandas`, `matplotlib`):

```bash
pip install -r requirements.txt
```

(*If the `requirements.txt` file is missing, install manually: `pip install django pandas matplotlib`*)

**5.Data Structure (CSV)**

The application expects a data file to be present:

* File Path: `app/static/chartapp/data/input_data.csv`

* Required Columns:

    + `Область` (Region) - for top-level grouping

    + `Місто/Район` (City/District) - for detailed breakdown

    + `Значення` (Value) - the numeric value for visualization

**6.Run Django Server**

Execute the server startup command in the root directory:

```bash
python manage.py runserver
```

### Usage
pen the following address in your browser: `http://127.0.0.1:8000/`.

2. **Main Page:** Displays a general chart summarizing the `Значення` (Value) across all regions. It also provides links to detailed regional charts.

3. **Detailed Chart:** Clicking the link for a specific region will display a chart where the `Значення` (Value) is summarized and detailed by `Місто/Район`(City/District).