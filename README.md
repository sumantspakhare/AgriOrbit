# AgriOrbit

### NASA-Powered Climate Intelligence for Climate-Resilient Agriculture

**AgriOrbit** is a farm-adaptation decision-support prototype developed
by **Helios Analytics** for the **NASA Space Apps Challenge 2026**
challenge, **"Field Shift: Adapting Farms with NASA Data."**

AgriOrbit brings together NASA environmental data, farmer-entered soil
information, and experimental crop-rotation screening to help users
explore agricultural adaptation strategies for a selected farm location.

> **Important:** AgriOrbit is an experimental decision-support
> prototype. Its crop-rotation scores, climate-scenario results, and
> alerts are illustrative screening outputs---not validated agronomic
> predictions, official climate forecasts, or a substitute for field
> measurements and expert advice.

------------------------------------------------------------------------

## Table of Contents

-   [Project Objectives](#project-objectives)
-   [Key Features](#key-features)
-   [NASA Data Sources](#nasa-data-sources)
-   [How AgriOrbit Works](#how-agriorbit-works)
-   [Technology Stack](#technology-stack)
-   [Installation](#installation)
-   [Run the Application](#run-the-application)
-   [Using the Dashboard](#using-the-dashboard)
-   [Data Interpretation and
    Limitations](#data-interpretation-and-limitations)
-   [Project Team](#project-team)

------------------------------------------------------------------------

## Project Objectives

Agriculture is exposed to changing rainfall patterns, temperature
variability, water stress, and soil degradation. Farmers need accessible
environmental information and practical tools to explore possible
adaptation strategies.

AgriOrbit aims to:

-   Make location-specific environmental indicators easier to explore.
-   Combine NASA data with farmer-provided soil information.
-   Compare alternative crop-rotation strategies.
-   Explore hypothetical climate stress scenarios.
-   Present results through dashboards, insights, and downloadable
    reports.

## Key Features

### 1. Global Farm Explorer

-   Select a farm location using an interactive map or geographical
    coordinates.
-   Use the selected latitude and longitude as the location context for
    data retrieval and planning.

### 2. NASA Climate Intelligence

-   Retrieve historical daily air-temperature and precipitation
    indicators from NASA POWER.
-   View climate summaries, data completeness, observation coverage, and
    trends.

### 3. Soil Intelligence

-   Enter soil laboratory or farmer-provided values:
    -   Soil pH
    -   Organic carbon
    -   Available nitrogen
    -   Soil texture
-   Review a preliminary soil-profile assessment.
-   Save the soil profile for use in the planning workflow.

### 4. NASA Soil-Wetness Monitoring

-   Retrieve NASA POWER modeled soil-wetness indicators.
-   Explore surface, root-zone, and soil-profile wetness values.
-   Review historical observations, trends, and data-quality
    information.

### 5. Vegetation Monitoring with MODIS NDVI

-   Retrieve MODIS MOD13Q1 vegetation-index observations when the
    external data service is available.
-   Explore NDVI observations and vegetation-greenness trends.
-   Review observation coverage and data availability.

### 6. Crop Rotation Intelligence

-   Compare four experimental crop-rotation strategies.
-   Review three-year crop sequences and comparative screening scores.
-   Consider farmer priorities and entered soil information during
    planning.

### 7. Climate What-If Simulator

-   Explore hypothetical changes in rainfall and temperature.
-   Compare baseline and scenario screening scores for crop-rotation
    strategies.
-   These are stress-test scenarios, not official NASA climate
    projections.

### 8. Smart Farm Insights and Alerts

-   Compare recent environmental observations with earlier observations.
-   Highlight changes that may deserve further investigation.
-   Display the highest-ranked crop-rotation strategy when results are
    available.

### 9. Dashboards and Reports

-   Project overview and executive dashboard.
-   Advanced environmental analytics.
-   Data reliability and farm adaptation scorecards.
-   Farmer adaptation action plan.
-   Downloadable Farm Adaptation Report in text and PDF formats.

------------------------------------------------------------------------

## NASA Data Sources

  Data source   Variables / product   Use in AgriOrbit
  ------------- --------------------- ------------------------------------------
  NASA POWER    `T2M`                 Daily mean air temperature
  NASA POWER    `PRECTOTCORR`         Corrected daily precipitation
  NASA POWER    `GWETTOP`             Modeled surface soil-wetness indicator
  NASA POWER    `GWETROOT`            Modeled root-zone soil-wetness indicator
  NASA POWER    `GWETPROF`            Modeled soil-profile wetness indicator
  NASA MODIS    `MOD13Q1`             Vegetation indices, including NDVI

Official references:

-   [NASA POWER](https://power.larc.nasa.gov/)
-   [NASA POWER Documentation](https://power.larc.nasa.gov/docs/)
-   [NASA LAADS DAAC -- MOD13Q1 Product
    Information](https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MOD13Q1/)

### Understanding the data

-   NASA POWER climate values are gridded satellite/model-based
    estimates, not measurements from an on-site weather station.
-   NASA POWER soil-wetness variables are modeled indicators. They are
    not direct field soil-moisture measurements, soil laboratory
    results, or direct SMAP Level-4 measurements.
-   MODIS NDVI represents vegetation greenness. It is not a direct
    measurement of crop yield, profitability, or a definitive
    crop-health diagnosis.
-   MODIS MOD13Q1 is a 16-day vegetation-index composite product with a
    nominal spatial resolution of 250 metres.

------------------------------------------------------------------------

## How AgriOrbit Works

1.  **Select a farm location** using the interactive map or coordinates.
2.  **Retrieve environmental data** from NASA POWER and attempt MODIS
    NDVI retrieval.
3.  **Enter soil information** such as pH, organic carbon, nitrogen, and
    texture.
4.  **Set a farmer priority**: water conservation, soil health
    improvement, climate resilience, or balanced sustainability.
5.  **Compare crop rotations** using the prototype's screening approach.
6.  **Explore climate scenarios** and review the resulting comparisons.
7.  **Generate planning outputs**, including the Farm Adaptation Report
    and Farmer Action Plan.

------------------------------------------------------------------------

## Technology Stack

The application is built with Python and Streamlit. The project uses the
following libraries and services in its current setup:

-   **Python** -- application logic and data processing
-   **Streamlit** -- interactive web application
-   **Pandas** -- tabular data handling
-   **NumPy** -- numerical operations
-   **Requests** -- API requests
-   **Plotly** -- interactive charts
-   **Folium** and **streamlit-folium** -- interactive map
-   **Matplotlib** -- report charts
-   **ReportLab** -- PDF report generation
-   **NASA POWER API** -- climate and modeled soil-wetness data
-   **NASA MODIS MOD13Q1 data service** -- vegetation-index observations

The exact installed package versions are defined by the project's
`requirements.txt` file.

------------------------------------------------------------------------

## Installation

### Prerequisites

-   Python 3.10 or later is recommended.
-   Git (optional, if cloning the repository).
-   A Windows, macOS, or Linux environment.

### 1. Get the project

If you have the project repository:

``` bash
git clone <repository-url>
cd AgriOrbit
```

Alternatively, open the project folder containing `app.py` and
`requirements.txt`.

### 2. Create a virtual environment

**Windows PowerShell:**

``` powershell
py -m venv .venv
```

**macOS / Linux:**

``` bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

``` bat
.venv\Scripts\activate.bat
```

**macOS / Linux:**

``` bash
source .venv/bin/activate
```

### 4. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Run the Application

From the project directory, with the virtual environment activated:

``` bash
streamlit run app.py
```

Streamlit will print a local address in the terminal. Open that address
in your browser. The default local address is usually:

``` text
http://localhost:8501
```

To stop the application, press **Ctrl + C** in the terminal.

------------------------------------------------------------------------

## Using the Dashboard

For a typical workflow:

1.  Open the application and review the AgriOrbit project overview.
2.  Select the farm location in **Global Farm Explorer**.
3.  Retrieve climate data and soil-wetness indicators for that location.
4.  Retrieve MODIS NDVI observations when available.
5.  Enter and save the farm's soil profile.
6.  Choose the farmer's main priority.
7.  Generate and compare crop-rotation strategies.
8.  Adjust rainfall and temperature assumptions in the climate
    simulator.
9.  Review dashboards, insights, data reliability, and the action plan.
10. Generate and download the Farm Adaptation Report.

**Location awareness:** Environmental data and planning outputs are
associated with the selected farm coordinates. After changing the
location, retrieve the relevant data and regenerate planning outputs
before interpreting them for the new location.

------------------------------------------------------------------------

## Data Interpretation and Limitations

AgriOrbit is a prototype intended to support exploration and discussion.
Users should consider the following limitations:

-   Environmental data availability and coverage can vary by location,
    date range, and external service availability.
-   NASA POWER data are gridded or modeled estimates and may differ from
    local field conditions.
-   Soil-profile values are user-entered; AgriOrbit does not
    independently verify laboratory results.
-   Soil-wetness indicators are modeled estimates and should not be
    treated as direct volumetric soil-water measurements.
-   NDVI indicates vegetation greenness and should not be interpreted as
    crop yield or a definitive diagnosis.
-   Crop-rotation scores are experimental, rule-based screening results.
    They are not validated yield, profitability, or soil-health
    predictions.
-   Climate-simulator outputs are hypothetical sensitivity scenarios,
    not official climate forecasts.
-   Smart alerts use simple comparisons of available observations. They
    are not validated drought warnings, crop-health diagnoses, or
    agronomic recommendations.
-   Local field measurements and advice from qualified agronomists are
    recommended before making farm-management decisions.

## Project Team

**Team:** Helios Analytics\
**Project:** AgriOrbit\
**Challenge:** Field Shift: Adapting Farms with NASA Data\
**Competition:** NASA Space Apps Challenge 2026

------------------------------------------------------------------------

*AgriOrbit --- Exploring environmental intelligence for
climate-resilient agriculture.*