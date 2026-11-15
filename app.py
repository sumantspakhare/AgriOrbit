import time
import io
import matplotlib.pyplot as plt
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)

import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

# ==========================================
# 1. APPLICATION CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AgriOrbit | Siddhi Services",
    page_icon="🌱",
    layout="wide"
)

st.title("🌍 AgriOrbit")
st.subheader("NASA-Powered Climate Intelligence")

st.markdown(
    "Understanding environmental conditions to "
    "support climate-resilient agriculture."
)


# ==========================================
# AGRIORBIT PROJECT OVERVIEW DASHBOARD
# ==========================================

st.header("🚀 Discover AgriOrbit")

st.markdown(
    """
    **AgriOrbit** is a farm adaptation decision-support
    prototype developed by **Siddhi Services** for the
    NASA Space Apps Challenge 2026.

    It brings together environmental data, farmer-provided
    soil information and crop rotation screening to help
    explore agricultural adaptation strategies.
    """
)

# Project highlights

overview_col1, overview_col2, overview_col3 = st.columns(3)

with overview_col1:
    st.subheader("🛰️ NASA Data")
    st.write(
        "Explore historical climate indicators, "
        "modeled soil-wetness indicators and "
        "MODIS vegetation observations when available."
    )

with overview_col2:
    st.subheader("🌱 Farm Intelligence")
    st.write(
        "Combine farmer-entered soil information "
        "and farming priorities to compare "
        "alternative crop rotation strategies."
    )

with overview_col3:
    st.subheader("🌦️ Climate Adaptation")
    st.write(
        "Explore hypothetical climate scenarios "
        "and generate farm adaptation reports "
        "and practical planning checklists."
    )

st.divider()

# The agricultural challenge

st.subheader("🌍 The Problem We Address")

st.write(
    """
    Agriculture is exposed to changing rainfall patterns,
    temperature variability, water stress and soil
    degradation.

    Farmers need accessible environmental information
    and practical planning tools to explore possible
    adaptation strategies.
    """
)

# How AgriOrbit works

st.subheader("⚙️ How AgriOrbit Works")

workflow_col1, workflow_col2 = st.columns(2)

with workflow_col1:
    st.markdown(
        """
        **1. Select a Farm Location**

        Choose a location using the interactive global map
        or enter geographical coordinates.

        **2. Explore Environmental Data**

        Retrieve NASA POWER climate and soil-wetness
        indicators, and attempt MODIS NDVI retrieval.

        **3. Enter Soil Information**

        Add soil pH, organic carbon, available nitrogen
        and soil texture.
        """
    )

with workflow_col2:
    st.markdown(
        """
        **4. Set Farmer Priorities**

        Select water conservation, soil health,
        climate resilience or balanced sustainability.

        **5. Compare Crop Rotations**

        Generate and compare experimental
        three-year crop rotation strategies.

        **6. Plan and Download**

        Explore climate scenarios and download
        the Farm Adaptation Report and Action Plan.
        """
    )

st.divider()

# NASA data sources

st.subheader("🛰️ NASA Earth Observation and Data Sources")

st.markdown(
    """
    | Data source | AgriOrbit application |
    |---|---|
    | NASA POWER – T2M | Daily mean air temperature |
    | NASA POWER – PRECTOTCORR | Corrected daily precipitation |
    | NASA POWER – GWETTOP | Surface soil-wetness indicator |
    | NASA POWER – GWETROOT | Root-zone soil-wetness indicator |
    | NASA POWER – GWETPROF | Soil-profile wetness indicator |
    | NASA MODIS MOD13Q1 | Vegetation NDVI observations |
    """
)

st.caption(
    "NASA POWER climate and soil-wetness values are "
    "gridded or modeled estimates. MODIS NDVI represents "
    "vegetation greenness. These data do not directly "
    "measure crop yield or soil laboratory properties."
)

st.divider()

# Project identity

st.subheader("👥 Project Team")

st.markdown(
    """
    **Team:** Siddhi Services

    **Project:** AgriOrbit

    **Challenge:** Field Shift: Adapting Farms with NASA Data

    **Competition:** NASA Space Apps Challenge 2026
    """
)

st.info(
    "AgriOrbit is an experimental decision-support prototype. "
    "Its crop rotation scores and climate scenarios are "
    "illustrative screening tools and require local "
    "agronomic validation."
)

st.divider()

# ==========================================
# END OF PROJECT OVERVIEW
# ==========================================

st.divider()

# ==========================================
# GLOBAL FARM LOCATION
# ==========================================

st.sidebar.header("🌍 Farm Location")

# Initialize default coordinates

if "farm_lat" not in st.session_state:
    st.session_state["farm_lat"] = 19.0760

if "farm_lon" not in st.session_state:
    st.session_state["farm_lon"] = 72.8777

# Apply map selections BEFORE creating widgets

if "pending_lat" in st.session_state:

    st.session_state["farm_lat"] = (
        st.session_state.pop("pending_lat")
    )

    st.session_state["farm_lon"] = (
        st.session_state.pop("pending_lon")
    )

# Create coordinate widgets

latitude = st.sidebar.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    key="farm_lat",
    format="%.4f"
)

longitude = st.sidebar.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    key="farm_lon",
    format="%.4f"
)

st.sidebar.caption(
    "Select a location using the map or coordinates."
)

# ==========================================
# INTERACTIVE GLOBAL FARM MAP
# ==========================================

st.header("🗺️ Global Farm Explorer")

st.write(
    "Click anywhere on the map to select "
    "your farm location."
)

farm_map = folium.Map(
    location=[latitude, longitude],
    zoom_start=5,
    control_scale=True
)

folium.Marker(
    [latitude, longitude],
    popup="Selected Farm",
    tooltip="Your Farm",
    icon=folium.Icon(color="green")
).add_to(farm_map)

map_result = st_folium(
    farm_map,
    width=None,
    height=450,
    key="global_farm_map",
    returned_objects=["last_clicked"]
)

if map_result and map_result.get("last_clicked"):

    clicked = map_result["last_clicked"]

    new_lat = round(clicked["lat"], 4)
    new_lon = round(clicked["lng"], 4)

    if new_lat != latitude or new_lon != longitude:

        st.session_state["pending_lat"] = new_lat
        st.session_state["pending_lon"] = new_lon

        st.rerun()

        st.session_state["pending_lat"] = new_lat
        st.session_state["pending_lon"] = new_lon

        st.rerun()

st.info(
    f"Selected farm coordinates: "
    f"{latitude:.4f}, {longitude:.4f}"
)

# ==========================================
# AGRIORBIT EXECUTIVE DASHBOARD
# ==========================================

st.divider()

st.header("📊 AgriOrbit Executive Dashboard")

st.write(
    "A consolidated overview of farm location, "
    "environmental observations and adaptation "
    "planning progress."
)

# ------------------------------------------
# CURRENT LOCATION AND DATA AVAILABILITY
# ------------------------------------------

dashboard_location = (
    round(latitude, 4),
    round(longitude, 4)
)

dashboard_climate_df = st.session_state.get("climate_data")
dashboard_wetness_df = st.session_state.get("smap_data")
dashboard_ndvi_df = st.session_state.get("ndvi_data")

dashboard_climate_ready = (
    isinstance(dashboard_climate_df, pd.DataFrame)
    and not dashboard_climate_df.empty
    and st.session_state.get("climate_data_location")
    == dashboard_location
)

dashboard_wetness_ready = (
    isinstance(dashboard_wetness_df, pd.DataFrame)
    and not dashboard_wetness_df.empty
    and st.session_state.get("wetness_data_location")
    == dashboard_location
)

dashboard_ndvi_ready = (
    isinstance(dashboard_ndvi_df, pd.DataFrame)
    and not dashboard_ndvi_df.empty
    and st.session_state.get("ndvi_data_location")
    == dashboard_location
)

dashboard_rotation_ready = (
    bool(st.session_state.get("rotation_results"))
    and st.session_state.get("rotation_location")
    == dashboard_location
)

dashboard_simulation_ready = (
    bool(st.session_state.get("simulated_results"))
    and st.session_state.get("simulation_location")
    == dashboard_location
)

dashboard_soil_ready = (
    "soil_profile" in st.session_state
)

dashboard_available_streams = sum([
    dashboard_climate_ready,
    dashboard_wetness_ready,
    dashboard_ndvi_ready
])

dashboard_planning_steps = sum([
    dashboard_soil_ready,
    dashboard_rotation_ready,
    dashboard_simulation_ready
])

# ------------------------------------------
# TOP KPI CARDS
# ------------------------------------------

st.subheader("🌍 Farm Overview")

overview_col1, overview_col2, overview_col3 = st.columns(3)

with overview_col1:
    st.metric(
        "Selected Farm Location",
        f"{latitude:.4f}, {longitude:.4f}"
    )

with overview_col2:
    st.metric(
        "Environmental Data Streams",
        f"{dashboard_available_streams}/3"
    )

with overview_col3:
    st.metric(
        "Farm Planning Progress",
        f"{dashboard_planning_steps}/3"
    )

st.divider()

# ------------------------------------------
# ENVIRONMENTAL INTELLIGENCE SNAPSHOT
# ------------------------------------------

st.subheader("🛰️ Environmental Intelligence Snapshot")

climate_col, wetness_col, vegetation_col = st.columns(3)

# Climate snapshot

with climate_col:

    st.markdown("**🌡️ Climate Conditions**")

    if dashboard_climate_ready:

        st.metric(
            "Average Temperature",
            f"{dashboard_climate_df['Temperature'].mean():.1f} °C"
        )

        st.metric(
            "Total Precipitation",
            f"{dashboard_climate_df['Rainfall'].sum():.1f} mm"
        )

        st.caption(
            f"Latest available date: "
            f"{dashboard_climate_df['Date'].max().date()}"
        )

    else:

        st.info(
            "Climate data has not been retrieved "
            "for this farm location."
        )

# Soil wetness snapshot

with wetness_col:

    st.markdown("**💧 Soil Wetness**")

    if dashboard_wetness_ready:

        latest_wetness = dashboard_wetness_df.iloc[-1]

        st.metric(
            "Surface Wetness",
            f"{latest_wetness['Surface Moisture']:.3f}"
        )

        st.metric(
            "Root-Zone Wetness",
            f"{latest_wetness['Root Zone Moisture']:.3f}"
        )

        st.metric(
            "Profile Wetness",
            f"{latest_wetness['Profile Moisture']:.3f}"
        )

    else:

        st.info(
            "Soil-wetness data has not been retrieved "
            "for this farm location."
        )

# Vegetation snapshot

with vegetation_col:

    st.markdown("**🌿 Vegetation Monitoring**")

    if dashboard_ndvi_ready:

        latest_ndvi = dashboard_ndvi_df.iloc[-1]

        st.metric(
            "Latest NDVI",
            f"{latest_ndvi['NDVI']:.3f}"
        )

        st.metric(
            "Valid Observations",
            len(dashboard_ndvi_df)
        )

        st.caption(
            f"Observation date: {latest_ndvi['Date'].date()}"
        )

    else:

        st.info(
            "MODIS NDVI has not been retrieved "
            "for this farm location."
        )

st.divider()

# ------------------------------------------
# FARM ADAPTATION PROGRESS
# ------------------------------------------

st.subheader("🌱 Farm Adaptation Progress")

progress_col1, progress_col2, progress_col3 = st.columns(3)

with progress_col1:

    st.markdown("**Soil Profile**")

    if dashboard_soil_ready:
        st.success("Saved")
    else:
        st.warning("Not saved")

with progress_col2:

    st.markdown("**Crop Rotation**")

    if dashboard_rotation_ready:

        best_dashboard_rotation = (
            st.session_state["rotation_results"][0]
        )

        st.success("Generated")

        st.caption(
            f"Top strategy: "
            f"{best_dashboard_rotation['Rotation']}"
        )

    else:

        st.warning("Not generated")

with progress_col3:

    st.markdown("**Climate Simulation**")

    if dashboard_simulation_ready:
        st.success("Generated")
    else:
        st.warning("Not generated")

# ------------------------------------------
# QUICK NAVIGATION
# ------------------------------------------

st.divider()

st.subheader("🧭 Quick Navigation")

st.markdown("""
Use these shortcuts to explore the main AgriOrbit modules:

- [🌍 Global Farm Explorer](#global-farm-explorer)
- [🛰️ Climate Dashboard](#earth-observation-intelligence)
- [🌱 Soil Intelligence](#soil-intelligence)
- [💧 Soil Wetness Monitoring](#nasa-soil-wetness-monitoring)
- [🌾 Crop Rotation Intelligence](#crop-rotation-intelligence)
- [🌦️ Climate What-If Simulator](#climate-what-if-simulator)
- [📄 Farm Adaptation Report](#agriorbit-farm-adaptation-report)
- [🧑‍🌾 Farmer Action Plan](#farmer-adaptation-action-plan)
""")

st.caption(
    "Dashboard values are shown only when retrieved "
    "data belongs to the currently selected farm location. "
    "Missing data is not treated as zero."
)

st.divider()

# ==========================================
# AGRIORBIT ADVANCED ANALYTICS DASHBOARD
# ==========================================

st.divider()

st.header("📈 AgriOrbit Advanced Analytics")

st.write(
    "Explore interactive environmental trends "
    "and compare farm adaptation strategies."
)

# ------------------------------------------
# 1. CLIMATE ANALYTICS
# ------------------------------------------

st.subheader("🌦️ 1. Climate Trend Analysis")

if dashboard_climate_ready:

    analytics_col1, analytics_col2 = st.columns(2)

    with analytics_col1:

        temperature_fig = px.line(
            dashboard_climate_df,
            x="Date",
            y="Temperature",
            title="Daily Temperature Trend",
            labels={
                "Temperature": "Temperature (°C)",
                "Date": "Date"
            }
        )

        st.plotly_chart(
            temperature_fig,
            use_container_width=True
        )

    with analytics_col2:

        monthly_rainfall_analytics = (
            dashboard_climate_df
            .set_index("Date")["Rainfall"]
            .resample("MS")
            .sum()
            .reset_index()
        )

        rainfall_fig = px.bar(
            monthly_rainfall_analytics,
            x="Date",
            y="Rainfall",
            title="Monthly Rainfall Distribution",
            labels={
                "Rainfall": "Precipitation (mm)",
                "Date": "Month"
            }
        )

        st.plotly_chart(
            rainfall_fig,
            use_container_width=True
        )

else:

    st.info(
        "Retrieve NASA POWER climate data for the "
        "selected farm location to view climate analytics."
    )

st.divider()

# ------------------------------------------
# 2. SOIL WETNESS ANALYTICS
# ------------------------------------------

st.subheader("💧 2. Soil Wetness Analysis")

if dashboard_wetness_ready:

    wetness_fig = px.line(
        dashboard_wetness_df,
        x="Date",
        y=[
            "Surface Moisture",
            "Root Zone Moisture",
            "Profile Moisture"
        ],
        markers=True,
        title="Soil Wetness Across Different Layers",
        labels={
            "value": "Wetness (fraction)",
            "Date": "Date",
            "variable": "Soil Layer"
        }
    )

    st.plotly_chart(
        wetness_fig,
        use_container_width=True
    )

    st.caption(
        "NASA POWER modeled soil-wetness indicators. "
        "These are not direct field measurements."
    )

else:

    st.info(
        "Retrieve NASA POWER soil-wetness indicators "
        "to view this analysis."
    )

st.divider()

# ------------------------------------------
# 3. VEGETATION ANALYTICS
# ------------------------------------------

st.subheader("🌿 3. Vegetation Trend Analysis")

if dashboard_ndvi_ready:

    vegetation_fig = px.line(
        dashboard_ndvi_df,
        x="Date",
        y="NDVI",
        markers=True,
        title="MODIS NDVI Time Series",
        labels={
            "NDVI": "Vegetation Greenness (NDVI)",
            "Date": "Observation Date"
        }
    )

    st.plotly_chart(
        vegetation_fig,
        use_container_width=True
    )

    st.caption(
        "NDVI represents vegetation greenness. "
        "It is not a direct crop-yield measurement."
    )

else:

    st.info(
        "Retrieve MODIS NDVI data when the external "
        "service is available to view vegetation trends."
    )

st.divider()

# ------------------------------------------
# 4. CROP ROTATION ANALYTICS
# ------------------------------------------

st.subheader("🌾 4. Crop Rotation Performance Comparison")

if dashboard_rotation_ready:

    analytics_rotation_df = pd.DataFrame([
        {
            "Rotation": item["Rotation"],
            "Score": item["Score"]
        }
        for item in st.session_state["rotation_results"]
    ])

    rotation_fig = px.bar(
        analytics_rotation_df,
        x="Rotation",
        y="Score",
        color="Score",
        text="Score",
        title="Comparative Crop Rotation Scores",
        labels={
            "Rotation": "Crop Rotation Strategy",
            "Score": "Screening Score (/100)"
        }
    )

    rotation_fig.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        rotation_fig,
        use_container_width=True
    )

    st.dataframe(
        analytics_rotation_df,
        use_container_width=True
    )

else:

    st.info(
        "Save your soil profile and generate a crop "
        "rotation plan to compare strategy scores."
    )

# ------------------------------------------
# ANALYTICS LIMITATIONS
# ------------------------------------------

st.caption(
    "Analytics are based on data retrieved for the "
    "currently selected farm location. Crop rotation "
    "scores are experimental rule-based screening "
    "results, not validated agronomic predictions."
)

st.divider()

# ==========================================
# AGRIORBIT SMART FARM INSIGHTS & ALERTS
# ==========================================

st.divider()

st.header("🧠 Smart Farm Insights & Alerts")

st.write(
    "AgriOrbit compares recent environmental observations "
    "with earlier observations and highlights changes "
    "that may deserve further investigation."
)

smart_insights = []
comparisons_available = 0

# ------------------------------------------
# 1. CLIMATE INSIGHTS
# ------------------------------------------

st.subheader("🌦️ Climate Insights")

if dashboard_climate_ready:

    climate_insight_df = dashboard_climate_df.copy()

    climate_insight_df["Date"] = pd.to_datetime(
        climate_insight_df["Date"],
        errors="coerce"
    )

    climate_insight_df["Rainfall"] = pd.to_numeric(
        climate_insight_df["Rainfall"],
        errors="coerce"
    )

    climate_insight_df["Temperature"] = pd.to_numeric(
        climate_insight_df["Temperature"],
        errors="coerce"
    )

    climate_insight_df = (
        climate_insight_df
        .dropna(subset=["Date", "Rainfall", "Temperature"])
        .sort_values("Date")
    )

    if len(climate_insight_df) >= 60:

        recent_climate = climate_insight_df.tail(30)
        previous_climate = climate_insight_df.iloc[-60:-30]

        recent_rainfall = recent_climate["Rainfall"].sum()
        previous_rainfall = previous_climate["Rainfall"].sum()

        recent_temperature = recent_climate["Temperature"].mean()
        previous_temperature = previous_climate["Temperature"].mean()

        comparisons_available += 1

        # Rainfall comparison

        if previous_rainfall > 0:

            rainfall_change = (
                (recent_rainfall - previous_rainfall)
                / previous_rainfall
            ) * 100

            if rainfall_change <= -20:

                smart_insights.append((
                    "warning",
                    "Rainfall Decline",
                    f"Rainfall in the latest 30 observations "
                    f"is {abs(rainfall_change):.1f}% lower "
                    "than in the preceding 30 observations."
                ))

            elif rainfall_change >= 20:

                smart_insights.append((
                    "info",
                    "Rainfall Increase",
                    f"Rainfall in the latest 30 observations "
                    f"is {rainfall_change:.1f}% higher "
                    "than in the preceding 30 observations."
                ))

            else:

                smart_insights.append((
                    "success",
                    "Rainfall Trend",
                    "No rainfall change greater than 20% "
                    "was detected between the two periods."
                ))

        else:

            smart_insights.append((
                "info",
                "Rainfall Comparison",
                "The earlier comparison period had zero "
                "recorded rainfall, so percentage change "
                "cannot be calculated."
            ))

        # Temperature comparison

        temperature_change = (
            recent_temperature - previous_temperature
        )

        if temperature_change >= 2:

            smart_insights.append((
                "warning",
                "Temperature Increase",
                f"Average temperature is {temperature_change:.1f}°C "
                "higher in the latest 30 observations."
            ))

        elif temperature_change <= -2:

            smart_insights.append((
                "info",
                "Temperature Decrease",
                f"Average temperature is {abs(temperature_change):.1f}°C "
                "lower in the latest 30 observations."
            ))

        else:

            smart_insights.append((
                "success",
                "Temperature Trend",
                "Average temperature has not changed by "
                "2°C or more between the comparison periods."
            ))

    else:

        st.info(
            "At least 60 valid climate observations are "
            "required for a 30-observation comparison."
        )

else:

    st.info(
        "Retrieve NASA POWER climate data to generate "
        "climate insights."
    )

# ------------------------------------------
# 2. SOIL WETNESS INSIGHTS
# ------------------------------------------

st.subheader("💧 Soil Wetness Insights")

if dashboard_wetness_ready:

    wetness_insight_df = dashboard_wetness_df.copy()

    wetness_insight_df["Date"] = pd.to_datetime(
        wetness_insight_df["Date"],
        errors="coerce"
    )

    wetness_columns = [
        "Surface Moisture",
        "Root Zone Moisture",
        "Profile Moisture"
    ]

    for column in wetness_columns:

        wetness_insight_df[column] = pd.to_numeric(
            wetness_insight_df[column],
            errors="coerce"
        )

    wetness_insight_df = (
        wetness_insight_df
        .dropna(subset=["Date"])
        .sort_values("Date")
    )

    if len(wetness_insight_df) >= 14:

        recent_wetness = wetness_insight_df.tail(7)
        previous_wetness = wetness_insight_df.iloc[-14:-7]

        comparisons_available += 1

        for column in wetness_columns:

            recent_value = recent_wetness[column].mean()
            previous_value = previous_wetness[column].mean()

            if pd.isna(recent_value) or pd.isna(previous_value):
                continue

            if previous_value <= 0:
                continue

            change = (
                (recent_value - previous_value)
                / previous_value
            ) * 100

            if change <= -15:

                smart_insights.append((
                    "warning",
                    f"{column} Decline",
                    f"The latest seven-observation average "
                    f"is {abs(change):.1f}% lower than the "
                    "preceding seven-observation average."
                ))

            elif change >= 15:

                smart_insights.append((
                    "info",
                    f"{column} Increase",
                    f"The latest seven-observation average "
                    f"is {change:.1f}% higher than the "
                    "preceding seven-observation average."
                ))

            else:

                smart_insights.append((
                    "success",
                    f"{column} Trend",
                    "No change greater than 15% was detected "
                    "between the comparison periods."
                ))

    else:

        st.info(
            "At least 14 valid observations are required "
            "to compare soil-wetness trends."
        )

else:

    st.info(
        "Retrieve NASA POWER soil-wetness indicators "
        "to generate soil insights."
    )

# ------------------------------------------
# 3. VEGETATION INSIGHTS
# ------------------------------------------

st.subheader("🌿 Vegetation Insights")

if dashboard_ndvi_ready:

    ndvi_insight_df = dashboard_ndvi_df.copy()

    ndvi_insight_df["Date"] = pd.to_datetime(
        ndvi_insight_df["Date"],
        errors="coerce"
    )

    ndvi_insight_df["NDVI"] = pd.to_numeric(
        ndvi_insight_df["NDVI"],
        errors="coerce"
    )

    ndvi_insight_df = (
        ndvi_insight_df
        .dropna(subset=["Date", "NDVI"])
        .sort_values("Date")
    )

    if len(ndvi_insight_df) >= 2:

        previous_ndvi = ndvi_insight_df["NDVI"].iloc[-2]
        latest_ndvi = ndvi_insight_df["NDVI"].iloc[-1]

        ndvi_change = latest_ndvi - previous_ndvi

        comparisons_available += 1

        if ndvi_change <= -0.05:

            smart_insights.append((
                "warning",
                "NDVI Decline",
                f"NDVI decreased by {abs(ndvi_change):.3f} "
                "compared with the previous observation. "
                "Consider checking field conditions."
            ))

        elif ndvi_change >= 0.05:

            smart_insights.append((
                "success",
                "NDVI Increase",
                f"NDVI increased by {ndvi_change:.3f} "
                "compared with the previous observation."
            ))

        else:

            smart_insights.append((
                "info",
                "NDVI Trend",
                "No NDVI change of 0.05 or more was detected "
                "between the two latest observations."
            ))

    else:

        st.info(
            "At least two valid MODIS observations are "
            "required to compare NDVI."
        )

else:

    st.info(
        "MODIS NDVI observations are not available "
        "for this location. Vegetation insights cannot "
        "currently be generated."
    )

# ------------------------------------------
# 4. CROP ROTATION INSIGHT
# ------------------------------------------

st.subheader("🌾 Crop Rotation Insight")

if dashboard_rotation_ready:

    best_rotation = st.session_state["rotation_results"][0]

    smart_insights.append((
        "success",
        "Top-Ranked Crop Rotation",
        f"{best_rotation['Rotation']} currently has the "
        f"highest comparative screening score of "
        f"{best_rotation['Score']}/100."
    ))

    st.write(
        f"**Selected farmer priority:** "
        f"{st.session_state.get('farmer_priority', 'Not selected yet')}"
    )

else:

    st.info(
        "Generate a crop rotation plan to receive "
        "crop strategy insights."
    )

# ------------------------------------------
# 5. SMART ALERT SUMMARY
# ------------------------------------------

st.divider()

st.subheader("🚨 Smart Alert Summary")

if comparisons_available == 0 and not dashboard_rotation_ready:

    st.info(
        "No current-location data comparisons or crop "
        "rotation results are available yet. Retrieve "
        "environmental data and generate a rotation plan."
    )

elif smart_insights:

    warning_count = sum(
        1 for item in smart_insights
        if item[0] == "warning"
    )

    st.metric(
        "Potential Changes Requiring Attention",
        warning_count
    )

    for severity, title, message in smart_insights:

        if severity == "warning":

            st.warning(f"⚠️ **{title}** — {message}")

        elif severity == "success":

            st.success(f"✅ **{title}** — {message}")

        else:

            st.info(f"ℹ️ **{title}** — {message}")

else:

    st.info(
        "No insights could be generated from the available "
        "observations."
    )

# ------------------------------------------
# IMPORTANT INTERPRETATION NOTES
# ------------------------------------------

st.caption(
    "These alerts use simple comparisons of available "
    "observations. They are not validated drought warnings, "
    "crop-health diagnoses or agronomic recommendations. "
    "NASA POWER soil-wetness indicators are modeled estimates, "
    "and MODIS NDVI represents vegetation greenness."
)

st.divider()

# ==========================================
# NASA POWER CLIMATE DATA
# ==========================================

@st.cache_data(ttl=3600)
def get_nasa_data(lat, lon):

    end_date = date.today() - timedelta(days=2)
    end_date = date.today() - timedelta(days=2)
    start_date = end_date - timedelta(days=365)

    url = (
        "https://power.larc.nasa.gov/api/"
        "temporal/daily/point"
    )

    params = {
        "parameters": "T2M,PRECTOTCORR",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON"
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    climate = result["properties"]["parameter"]

    temperature = climate["T2M"]
    rainfall = climate["PRECTOTCORR"]

    df = pd.DataFrame({
        "Date": pd.to_datetime(
            list(temperature.keys()),
            format="%Y%m%d"
        ),
        "Temperature": list(temperature.values()),
        "Rainfall": list(rainfall.values())
    })

    df = df.replace(-999, float("nan")).dropna()

    if df.empty:
        raise ValueError("No valid climate observations.")

    return df

# ==========================================
# NASA SMAP SOIL MOISTURE DATA
# ==========================================


@st.cache_data(ttl=3600)
def get_smap_data(lat, lon):

    end_date = date.today() - timedelta(days=5)
    start_date = end_date - timedelta(days=89)

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": "GWETTOP,GWETROOT,GWETPROF",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON",
        "time-standard": "UTC"
    }

    response = requests.get(url, params=params, timeout=60)

    if not response.ok:
        raise ValueError(
            f"NASA POWER Error {response.status_code}: "
            f"{response.text}"
        )

    result = response.json()

    parameters = result["properties"]["parameter"]

    df = pd.DataFrame({
        "Date": pd.to_datetime(
            list(parameters["GWETTOP"].keys()),
            format="%Y%m%d"
        ),
        "Surface Moisture": list(parameters["GWETTOP"].values()),
        "Root Zone Moisture": list(parameters["GWETROOT"].values()),
        "Profile Moisture": list(parameters["GWETPROF"].values())
    })

    df = df.replace(-999, float("nan")).dropna()

    if df.empty:
        raise ValueError("No valid soil moisture observations returned.")

    return df


# ==========================================
# NASA MODIS NDVI DATA RETRIEVAL
# ==========================================

@st.cache_data(ttl=3600)
def get_modis_ndvi(lat, lon):

    base_url = "https://modis.ornl.gov/rst/api/v1/MOD13Q1"

    # Retrieve MODIS observation dates
    dates_response = None

    for attempt in range(3):

        try:
            dates_response = requests.get(
                f"{base_url}/dates",
                params={
                    "latitude": lat,
                    "longitude": lon
                },
                timeout=(15, 120)
            )

            if dates_response.status_code in [502, 503, 504]:
                if attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue

            dates_response.raise_for_status()
            break

        except requests.exceptions.Timeout:

            if attempt == 2:
                raise ValueError(
                    "MODIS dates service timed out after 3 attempts."
                )

            time.sleep(5 * (attempt + 1))

    dates_data = dates_response.json()

    available_dates = sorted(
        item["modis_date"]
        for item in dates_data["dates"]
    )

    if not available_dates:
        raise ValueError("No MODIS dates available.")

    selected_dates = available_dates[-10:]

    # Prepare subset request
    subset_params = {
        "latitude": lat,
        "longitude": lon,
        "startDate": selected_dates[0],
        "endDate": selected_dates[-1],
        "kmAboveBelow": 1,
        "kmLeftRight": 1
    }

    headers = {"Accept": "application/json"}

    subset_response = None

    # Retry subset request
    for attempt in range(3):

        try:
            subset_response = requests.get(
                f"{base_url}/subset",
                params=subset_params,
                headers=headers,
                timeout=120
            )

            if subset_response.status_code in [502, 503, 504]:

                if attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue

                break

            subset_response.raise_for_status()
            break

        except requests.exceptions.Timeout:

            if attempt == 2:
                break

            time.sleep(5 * (attempt + 1))

    # Fallback to latest observation
    if (
        subset_response is None
        or subset_response.status_code in [502, 503, 504]
    ):

        latest_date = selected_dates[-1]

        subset_params["startDate"] = latest_date
        subset_params["endDate"] = latest_date

        subset_response = requests.get(
            f"{base_url}/subset",
            params=subset_params,
            headers=headers,
            timeout=120
        )

    subset_response.raise_for_status()

    subset_data = subset_response.json()

    # Extract central pixel
    nrows = subset_data["nrows"]
    ncols = subset_data["ncols"]

    center_index = (
        (nrows // 2) * ncols + (ncols // 2)
    )

    observations = {}

    for item in subset_data["subset"]:

        modis_date = item["modis_date"]
        band = item["band"]
        values = item["data"]

        if modis_date not in observations:
            observations[modis_date] = {}

        observations[modis_date][band] = values

    # Process NDVI observations
    records = []

    for modis_date, bands in observations.items():

        ndvi_band = "250m_16_days_NDVI"
        quality_band = "250m_16_days_pixel_reliability"

        if ndvi_band not in bands:
            continue

        raw_ndvi = bands[ndvi_band][center_index]

        if raw_ndvi < -2000 or raw_ndvi > 10000:
            continue

        quality_values = bands.get(quality_band)

        quality = (
            quality_values[center_index]
            if quality_values is not None
            else None
        )

        if quality is not None and quality > 1:
            continue

        observation_date = pd.to_datetime(
            modis_date[1:],
            format="%Y%j"
        )

        records.append({
            "Date": observation_date,
            "NDVI": raw_ndvi * 0.0001,
            "Quality": quality
        })

    df = pd.DataFrame(records)

    if df.empty:
        raise ValueError(
            "No valid MODIS NDVI observations found."
        )

    return df.sort_values("Date").reset_index(drop=True)

# ==========================================
# MODIS VEGETATION HEALTH DASHBOARD
# ==========================================

st.divider()

st.header("🌿 MODIS Vegetation Health Monitoring")

st.header("🛰️ NASA MODIS NDVI Monitoring")

if st.button("🛰️ Retrieve MODIS NDVI"):

    with st.spinner("Retrieving MODIS NDVI data..."):

        try:
            ndvi_df = get_modis_ndvi(latitude, longitude)

            st.session_state["ndvi_data"] = ndvi_df

            st.session_state["ndvi_data_location"] = (
                round(latitude, 4),
                round(longitude, 4)
            )

            st.session_state["ndvi_retrieved_at"] = pd.Timestamp.now()

            st.success("MODIS NDVI data retrieved successfully!")

        except Exception as error:
            st.error(f"MODIS retrieval failed: {error}")
if "ndvi_data" in st.session_state:

    ndvi_df = st.session_state["ndvi_data"]

    latest_ndvi = ndvi_df["NDVI"].iloc[-1]

    st.subheader("📊 Latest Vegetation Indicator")

    col1, col2 = st.columns(2)

    col1.metric(
        "Latest NDVI",
        f"{latest_ndvi:.3f}"
    )

    col2.metric(
        "Observations Retrieved",
        len(ndvi_df)
    )

    st.caption(
        f"Latest observation: {ndvi_df['Date'].iloc[-1].date()}"
    )

    st.subheader("🌱 Vegetation Greenness Trend")

    ndvi_chart = px.line(
        ndvi_df,
        x="Date",
        y="NDVI",
        markers=True,
        title="MODIS NDVI Time Series",
        labels={
            "NDVI": "Normalized Difference Vegetation Index",
            "Date": "Observation Date"
        }
    )

    st.plotly_chart(
        ndvi_chart,
        use_container_width=True
    )

    st.subheader("📋 Historical NDVI Observations")

    st.dataframe(
        ndvi_df,
        use_container_width=True
    )

    st.download_button(
        "Download MODIS NDVI CSV",
        data=ndvi_df.to_csv(index=False),
        file_name="agriorbit_modis_ndvi.csv",
        mime="text/csv"
    )

    st.caption(
        "Source: NASA MODIS/Terra MOD13Q1 Version 6.1, "
        "accessed through ORNL DAAC TESViS. "
        "NDVI is dimensionless and uses a 0.0001 scale factor. "
        "Observations are 16-day composites at 250 m resolution. "
        "NDVI indicates vegetation greenness, not crop yield "
        "or a definitive diagnosis of crop health."
    )

# ==========================================
# 4. NASA CLIMATE DASHBOARD
# ==========================================

st.header("🛰️ Earth Observation Intelligence")

st.write(
    "Retrieve historical climate information "
    "for your selected farm location."
)

if st.button(
    "🔄 Analyze Farm with NASA Data",
    type="primary"
):

    with st.spinner(
        "Connecting to NASA POWER API..."
    ):

        try:

            df = get_nasa_data(
                latitude,
                longitude
            )

            st.session_state["climate_data"] = df

            st.session_state["analyzed_location"] = (
                latitude,
                longitude
            )
            st.session_state["climate_data_location"] = (
            round(latitude, 4),
            round(longitude, 4)
            )
            climate_end_date = date.today() - timedelta(days=2)
            climate_start_date = climate_end_date - timedelta(days=365)

            st.session_state["climate_requested_start"] = climate_start_date
            st.session_state["climate_requested_end"] = climate_end_date
            st.session_state["climate_retrieved_at"] = pd.Timestamp.now()
            st.success(
                "NASA climate data retrieved successfully!"
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"NASA API connection failed: {error}"
            )

        except (KeyError, ValueError) as error:

            st.error(
                f"Unable to process NASA data: {error}"
            )

        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )

# ==========================================
# 5. DISPLAY CLIMATE RESULTS
# ==========================================


if "climate_data" in st.session_state:

    df = st.session_state["climate_data"]

    current_location = (
        round(latitude, 4),
        round(longitude, 4)
    )

    climate_location = st.session_state.get("climate_data_location")

    if climate_location != current_location:
        st.warning(
            "Climate data belongs to a different farm location. "
            "Please retrieve NASA climate data again for the selected location."
        )

    st.subheader("📊 Climate Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Temperature",
        f"{df['Temperature'].mean():.2f} °C"
    )

    col2.metric(
        "Total Precipitation",
        f"{df['Rainfall'].sum():.1f} mm"
    )

    col3.metric(
        "Valid Observation Days",
        len(df)
    )

    st.caption(
        f"Location: {st.session_state['analyzed_location']} "
        f"| Period: {df['Date'].min().date()} to "
        f"{df['Date'].max().date()}"
    )

    st.caption(
        "Data source: NASA POWER Daily Point API "
        "(Agroclimatology community). "
        "Variables: T2M (daily mean air temperature, °C) "
        "and PRECTOTCORR (corrected daily precipitation, mm/day). "
        "Daily timestamps use Local Solar Time, "
        "the NASA POWER default. "
        "These are gridded satellite/model-based estimates, "
        "not measurements from an on-site weather station."
    )
    st.subheader("🧾 Climate Data Quality")

    expected_days = (
        st.session_state["climate_requested_end"]
        - st.session_state["climate_requested_start"]
    ).days + 1

    valid_days = df["Date"].nunique()
    completeness = (valid_days / expected_days) * 100

    quality_col1, quality_col2, quality_col3 = st.columns(3)

    quality_col1.metric(
        "Valid daily records",
        f"{valid_days} / {expected_days}"
    )

    quality_col2.metric(
        "Data completeness",
        f"{completeness:.1f}%"
    )

    quality_col3.metric(
        "Retrieved in app",
        st.session_state["climate_retrieved_at"].strftime(
            "%d %b %Y, %H:%M"
        )
    )

    st.caption(
        "Completeness is calculated against the requested daily date range. "
        "A valid record contains both temperature and precipitation values."
    )
    # Temperature chart

    st.subheader("🌡️ Temperature Trends")

    temperature_chart = px.line(
        df,
        x="Date",
        y="Temperature",
        title="Daily Average Temperature",
        labels={
            "Temperature": "Temperature (°C)",
            "Date": "Date"
        }
    )

    st.plotly_chart(
        temperature_chart,
        use_container_width=True
    )

    # Monthly rainfall chart

    st.subheader("🌧️ Monthly Precipitation")

    monthly_rainfall = (
        df.set_index("Date")["Rainfall"]
        .resample("MS")
        .sum()
        .reset_index()
    )

    rainfall_chart = px.bar(
        monthly_rainfall,
        x="Date",
        y="Rainfall",
        title="Monthly Total Precipitation",
        labels={
            "Rainfall": "Precipitation (mm)",
            "Date": "Month"
        }
    )

    st.plotly_chart(
        rainfall_chart,
        use_container_width=True
    )

    # Monthly temperature

    monthly_temperature = (
        df.set_index("Date")["Temperature"]
        .resample("MS")
        .mean()
        .reset_index()
    )

    st.subheader("📈 Monthly Temperature Average")

    st.line_chart(
        monthly_temperature,
        x="Date",
        y="Temperature"
    )

    # Raw data

    with st.expander("View NASA climate observations"):

        st.dataframe(
            df,
            use_container_width=True
        )

        st.download_button(
            "Download climate data CSV",
            data=df.to_csv(index=False),
            file_name="agriorbit_nasa_climate.csv",
            mime="text/csv"
        )

# ==========================================
# SOIL INTELLIGENCE MODULE
# ==========================================

st.divider()

st.header("🌱 Soil Intelligence")

st.write(
    "Enter your soil laboratory results to assess "
    "soil conditions and support crop rotation planning."
)

st.info(
    "These values are farmer-entered inputs. "
    "They are not automatically retrieved from satellite data."
)

# Soil parameters

col1, col2 = st.columns(2)

with col1:

    soil_ph = st.number_input(
        "Soil pH",
        min_value=3.0,
        max_value=10.0,
        value=6.5,
        step=0.1,
        key="soil_ph"
    )

    organic_carbon = st.number_input(
        "Organic Carbon (%)",
        min_value=0.0,
        max_value=20.0,
        value=1.0,
        step=0.1,
        key="organic_carbon"
    )

with col2:

    nitrogen = st.number_input(
        "Available Nitrogen (mg/kg)",
        min_value=0.0,
        max_value=5000.0,
        value=100.0,
        step=5.0,
        key="soil_nitrogen"
    )

    soil_texture = st.selectbox(
        "Soil Texture",
        [
            "Loamy",
            "Sandy",
            "Clay",
            "Silty",
            "Sandy Loam",
            "Clay Loam"
        ],
        key="soil_texture"
    )

# Soil assessment

st.subheader("📊 Soil Profile Assessment")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Soil pH",
        f"{soil_ph:.1f}"
    )

    if soil_ph < 5.5:
        st.warning("Acidic soil")

    elif soil_ph > 7.5:
        st.warning("Alkaline soil")

    else:
        st.success("Broadly near-neutral pH")

with col2:

    st.metric(
        "Organic Carbon",
        f"{organic_carbon:.1f}%"
    )

with col3:

    st.metric(
        "Available Nitrogen",
        f"{nitrogen:.0f} mg/kg"
    )

# Texture information

st.subheader("Soil Characteristics")

texture_information = {
    "Loamy": "Generally balanced water retention and drainage.",
    "Sandy": "Generally drains quickly and may require careful water management.",
    "Clay": "Generally retains more water but may have drainage limitations.",
    "Silty": "Can retain water and nutrients but may be vulnerable to erosion.",
    "Sandy Loam": "Often has good drainage with moderate water retention.",
    "Clay Loam": "Can retain moisture and nutrients; compaction should be considered."
}

st.info(
    f"Selected texture: {soil_texture}. "
    + texture_information[soil_texture]
)

# Data provenance

st.caption(
    "Source: Farmer-entered soil information. "
    "Interpretations are preliminary screening indicators, "
    "not laboratory diagnoses or crop-specific suitability assessments."
)

# Save soil profile

if st.button("Save Soil Profile"):

    st.session_state["soil_profile"] = {
        "pH": soil_ph,
        "organic_carbon": organic_carbon,
        "nitrogen": nitrogen,
        "texture": soil_texture
    }

    st.success(
        "Soil profile saved for this session!"
    )

# ==========================================
# FARMER PRIORITIES
# ==========================================

st.divider()

st.header("🎯 Farmer Priorities")


priority = st.selectbox(
    "What matters most to your farm?",
    [
        "Water Conservation",
        "Soil Health Improvement",
        "Climate Resilience",
        "Balanced Sustainability"
    ],
    key="farmer_priority"
)


st.write(
    "AgriOrbit will use this preference "
    "to rank alternative crop rotations."
)

# ==========================================
# SMAP SOIL MOISTURE DASHBOARD
# ==========================================

st.divider()

st.header("💧 NASA Soil Wetness Monitoring")

st.write(
    "Monitor modeled surface, root-zone and "
    "full-profile soil wetness indicators "
    "at your selected farm location."
)

if st.button("Retrieve NASA Soil Moisture"):

    with st.spinner(
        "Retrieving soil moisture observations..."
    ):

        try:

            smap_df = get_smap_data(
                latitude,
                longitude
            )

            st.session_state["smap_data"] = smap_df
            st.session_state["wetness_data_location"] = (
            round(latitude, 4),
            round(longitude, 4)
            )
            wetness_end_date = date.today() - timedelta(days=5)
            wetness_start_date = wetness_end_date - timedelta(days=89)

            st.session_state["wetness_requested_start"] = wetness_start_date
            st.session_state["wetness_requested_end"] = wetness_end_date
            st.session_state["wetness_retrieved_at"] = pd.Timestamp.now()
            st.success(
                "Soil moisture data retrieved successfully!"
            )

        except Exception as error:

            st.error(
                f"Soil moisture retrieval failed: {error}"
            )

if "smap_data" in st.session_state:

    smap_df = st.session_state["smap_data"]

    current_location = (
        round(latitude, 4),
        round(longitude, 4)
    )

    wetness_location = st.session_state.get("wetness_data_location")

    if wetness_location != current_location:
        st.warning(
            "Soil-wetness data belongs to a different farm location. "
            "Please retrieve NASA soil-wetness data again for the selected location."
        )

    # Initialize metadata for previously retrieved data
    st.session_state.setdefault(
        "wetness_requested_start",
        smap_df["Date"].min().date()
    )

    st.session_state.setdefault(
        "wetness_requested_end",
        smap_df["Date"].max().date()
    )

    st.session_state.setdefault(
        "wetness_retrieved_at",
        None
    )

    # Soil wetness data quality
    st.subheader("🧾 Soil Wetness Data Quality")

    expected_wetness_days = (
        st.session_state["wetness_requested_end"]
        - st.session_state["wetness_requested_start"]
    ).days + 1

    valid_wetness_days = smap_df["Date"].nunique()

    wetness_completeness = (
        valid_wetness_days / expected_wetness_days
    ) * 100

    quality_col1, quality_col2, quality_col3 = st.columns(3)

    quality_col1.metric(
        "Valid daily records",
        f"{valid_wetness_days} / {expected_wetness_days}"
    )

    quality_col2.metric(
        "Data completeness",
        f"{wetness_completeness:.1f}%"
    )

    retrieval_time = st.session_state["wetness_retrieved_at"]

    quality_col3.metric(
        "Retrieved in app",
        (
            retrieval_time.strftime("%d %b %Y, %H:%M")
            if retrieval_time is not None
            else "Not recorded"
        )
    )

    st.caption(
        "Completeness is calculated against the requested date range. "
        "A valid record contains all three soil-wetness indicators: "
        "GWETTOP, GWETROOT and GWETPROF."
    )

    # Latest soil wetness indicators
    st.subheader("📊 Latest Soil Wetness Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Surface Wetness (GWETTOP)",
        f"{smap_df['Surface Moisture'].iloc[-1]:.3f}"
    )

    col2.metric(
        "Root Zone Wetness (GWETROOT)",
        f"{smap_df['Root Zone Moisture'].iloc[-1]:.3f}"
    )

    col3.metric(
        "Profile Wetness (GWETPROF)",
        f"{smap_df['Profile Moisture'].iloc[-1]:.3f}"
    )

    # Soil wetness trends
    st.subheader("💧 Soil Wetness Trends")

    moisture_chart = px.line(
        smap_df,
        x="Date",
        y=[
            "Surface Moisture",
            "Root Zone Moisture",
            "Profile Moisture"
        ],
        title="NASA POWER Soil Wetness Indicators",
        labels={
            "value": "Wetness (fraction)",
            "Date": "Date",
            "variable": "Soil Layer"
        }
    )

    st.plotly_chart(
        moisture_chart,
        use_container_width=True
    )

    # Historical data
    st.subheader("📋 Historical Soil Wetness Data")

    st.dataframe(
        smap_df.tail(15),
        use_container_width=True
    )

    st.download_button(
        "Download Soil Wetness Data",
        data=smap_df.to_csv(index=False),
        file_name="agriorbit_soil_wetness.csv",
        mime="text/csv"
    )

    st.caption(
        "Source: NASA POWER. GWETTOP, GWETROOT and GWETPROF "
        "are modeled soil-wetness indicators for different soil "
        "depths. They are not direct SMAP Level-4 measurements "
        "or field soil laboratory measurements."
    )

    st.caption(
        f"Observation period: "
        f"{smap_df['Date'].min().date()} to "
        f"{smap_df['Date'].max().date()}."
    )

    st.caption(
        "Units: dimensionless relative saturation (0–1). "
        "A value of 0 represents completely dry conditions; "
        "a value of 1 represents saturated conditions. "
        "These modeled indicators are not volumetric "
        "soil-water content measurements."
    )

# ==========================================
# CROP ROTATION INTELLIGENCE ENGINE
# ==========================================

st.divider()

st.header("🌾 Crop Rotation Intelligence")

st.write(
    "Compare alternative three-year crop rotation "
    "strategies using soil information, climate "
    "indicators and farmer priorities."
)

# ------------------------------------------
# CANDIDATE ROTATION DATABASE
# ------------------------------------------

rotations = [
    {
        "name": "Water-Smart Rotation",
        "crops": ["Millet", "Chickpea", "Sesame"],
        "water": 5,
        "heat": 5,
        "cover": 3,
        "legumes": 1,
        "diversity": 5
    },
    {
        "name": "Legume-Based Rotation",
        "crops": ["Sorghum", "Pigeon Pea", "Wheat"],
        "water": 3,
        "heat": 4,
        "cover": 4,
        "legumes": 1,
        "diversity": 5
    },
    {
        "name": "Conventional Diversification",
        "crops": ["Maize", "Soybean", "Wheat"],
        "water": 2,
        "heat": 3,
        "cover": 3,
        "legumes": 1,
        "diversity": 5
    },
    {
        "name": "Drought-Resilient Rotation",
        "crops": ["Sorghum", "Cowpea", "Millet"],
        "water": 5,
        "heat": 5,
        "cover": 4,
        "legumes": 1,
        "diversity": 5
    }
]

# Higher values mean better performance
# on the corresponding screening dimension.

# ------------------------------------------
# FARMER PRIORITY WEIGHTS
# ------------------------------------------

weights = {
    "Water Conservation": {
        "water": 0.40,
        "soil": 0.20,
        "nitrogen": 0.10,
        "climate": 0.20,
        "diversity": 0.10
    },

    "Soil Health Improvement": {
        "water": 0.10,
        "soil": 0.40,
        "nitrogen": 0.25,
        "climate": 0.10,
        "diversity": 0.15
    },

    "Climate Resilience": {
        "water": 0.25,
        "soil": 0.15,
        "nitrogen": 0.10,
        "climate": 0.35,
        "diversity": 0.15
    },

    "Balanced Sustainability": {
        "water": 0.20,
        "soil": 0.20,
        "nitrogen": 0.20,
        "climate": 0.20,
        "diversity": 0.20
    }
}

# ------------------------------------------
# SOIL AND CLIMATE INPUTS
# ------------------------------------------

soil_values = st.session_state.get(
    "soil_profile",
    {
        "pH": soil_ph,
        "organic_carbon": organic_carbon,
        "nitrogen": nitrogen,
        "texture": soil_texture
    }
)


current_location = (
    round(latitude, 4),
    round(longitude, 4)
)

rainfall = None

if (
    "climate_data" in st.session_state
    and st.session_state.get("climate_data_location") == current_location
):

    climate_df = st.session_state["climate_data"]

    rainfall = climate_df["Rainfall"].sum()


# ------------------------------------------
# RECENT NASA SOIL WETNESS SUMMARY
# ------------------------------------------

moisture_summary = None

if (
    "smap_data" in st.session_state
    and st.session_state.get("wetness_data_location") == current_location
):

    moisture_df = st.session_state["smap_data"].copy()

    # Select observations from the latest 30 days
    cutoff_date = (
        pd.Timestamp.today().normalize()
        - pd.Timedelta(days=30)
    )

    recent_moisture = moisture_df[
        moisture_df["Date"] >= cutoff_date
    ]

    # Use the latest available observations if
    # the 30-day period contains no records.
    if recent_moisture.empty:
        recent_moisture = moisture_df.tail(30)

    moisture_summary = {
        "Surface": recent_moisture[
            "Surface Moisture"
        ].mean(),

        "Root Zone": recent_moisture[
            "Root Zone Moisture"
        ].mean(),

        "Profile": recent_moisture[
            "Profile Moisture"
        ].mean()
    }

# ==========================================
# AGRIORBIT DATA RELIABILITY DASHBOARD
# ==========================================

st.divider()

st.header("🛡️ AgriOrbit Data Reliability Dashboard")

st.write(
    "Monitor the availability of NASA data "
    "for your currently selected farm location."
)

# Check climate data availability

climate_ready = (
    "climate_data" in st.session_state
    and st.session_state.get("climate_data_location")
    == current_location
)

# Check soil wetness data availability
# Check MODIS NDVI data availability

ndvi_ready = (
    "ndvi_data" in st.session_state
    and st.session_state.get("ndvi_data_location")
    == current_location
)
wetness_ready = (
    "smap_data" in st.session_state
    and st.session_state.get("wetness_data_location")
    == current_location
)
# Retrieve last successful data retrieval times

climate_retrieved = st.session_state.get(
    "climate_retrieved_at"
)

wetness_retrieved = st.session_state.get(
    "wetness_retrieved_at"
)
# Display data status

status_col1, status_col2, status_col3 = st.columns(3)
with status_col1:

    st.metric(
        "NASA POWER Climate Data",
        "Available" if climate_ready else "Needs Retrieval"
    )

with status_col2:

    st.metric(
        "NASA POWER Soil Wetness Data",
        "Available" if wetness_ready else "Needs Retrieval"
    )

with status_col3:

    st.metric(
        "MODIS NDVI Data",
        "Available" if ndvi_ready else "Needs Retrieval"
    )

st.caption(
    "Data is marked available only when it belongs "
    "to the currently selected farm coordinates."
)
st.subheader("🕒 Last Successful Retrieval")
# ------------------------------------------
# DATA COMPLETENESS AND OBSERVATION PERIODS
# ------------------------------------------

st.divider()

st.subheader("📊 Observation Coverage")

coverage_col1, coverage_col2 = st.columns(2)

with coverage_col1:

    st.markdown("**NASA POWER Climate Data**")

    if climate_ready:

        climate_df = st.session_state["climate_data"]

        climate_start = st.session_state["climate_requested_start"]
        climate_end = st.session_state["climate_requested_end"]

        expected_climate_days = (
            climate_end - climate_start
        ).days + 1

        valid_climate_days = climate_df["Date"].nunique()

        climate_completeness = (
            valid_climate_days / expected_climate_days * 100
        )

        st.write(
            f"Observation period: {climate_start} to {climate_end}"
        )

        st.metric(
            "Climate Data Completeness",
            f"{climate_completeness:.1f}%"
        )

        st.write(
            f"Valid daily records: {valid_climate_days} "
            f"/ {expected_climate_days}"
        )

    else:
        st.info("Retrieve climate data to view coverage.")

with coverage_col2:

    st.markdown("**NASA POWER Soil Wetness Data**")

    if wetness_ready:

        wetness_df = st.session_state["smap_data"]

        wetness_start = st.session_state["wetness_requested_start"]
        wetness_end = st.session_state["wetness_requested_end"]

        expected_wetness_days = (
            wetness_end - wetness_start
        ).days + 1

        valid_wetness_days = wetness_df["Date"].nunique()

        wetness_completeness = (
            valid_wetness_days / expected_wetness_days * 100
        )

        st.write(
            f"Observation period: {wetness_start} to {wetness_end}"
        )

        st.metric(
            "Soil Wetness Data Completeness",
            f"{wetness_completeness:.1f}%"
        )

        st.write(
            f"Valid daily records: {valid_wetness_days} "
            f"/ {expected_wetness_days}"
        )

    else:
        st.info("Retrieve soil-wetness data to view coverage.")
# ------------------------------------------
# MODIS NDVI OBSERVATION COVERAGE
# ------------------------------------------

st.divider()

st.subheader("🛰️ MODIS NDVI Observation Coverage")

if ndvi_ready:

    ndvi_df = st.session_state["ndvi_data"]

    ndvi_col1, ndvi_col2, ndvi_col3 = st.columns(3)

    ndvi_col1.metric(
        "Valid NDVI Observations",
        len(ndvi_df)
    )

    ndvi_col2.metric(
        "First Observation",
        ndvi_df["Date"].min().strftime("%d %b %Y")
    )

    ndvi_col3.metric(
        "Latest Observation",
        ndvi_df["Date"].max().strftime("%d %b %Y")
    )

    st.caption(
        "MODIS observations are 16-day composites. "
        "Only observations passing the configured "
        "quality screening are included."
    )

else:

    st.info(
        "Successfully retrieve MODIS NDVI data for this "
        "farm location to view observation coverage."
    )
time_col1, time_col2, time_col3 = st.columns(3)
with time_col1:

    if climate_ready and climate_retrieved is not None:
        st.write(
            "Climate data:",
            climate_retrieved.strftime("%d %b %Y, %H:%M")
        )
    else:
        st.write("Climate data: Not retrieved for this location")

with time_col2:

    if wetness_ready and wetness_retrieved is not None:
        st.write(
            "Soil wetness data:",
            wetness_retrieved.strftime("%d %b %Y, %H:%M")
        )
    else:
        st.write("Soil wetness data: Not retrieved for this location")

with time_col3:

    if ndvi_ready and st.session_state.get("ndvi_retrieved_at") is not None:
        st.write(
            "MODIS NDVI data:",
            st.session_state["ndvi_retrieved_at"].strftime(
                "%d %b %Y, %H:%M"
            )
        )
    else:
        st.write("MODIS NDVI data: Not retrieved for this location")

# ==========================================
# SOIL TEXTURE INTERPRETATION
# ==========================================

texture_guidance = {
    "Sandy": (
        "Rapid drainage and lower water retention. "
        "Monitor irrigation and organic matter."
    ),

    "Loamy": (
        "Generally balanced drainage and water retention. "
        "Maintain organic matter and soil structure."
    ),

    "Clay": (
        "Higher water retention and possible drainage "
        "limitations. Monitor compaction and waterlogging."
    ),

    "Silty": (
        "Can retain water and nutrients but may be "
        "vulnerable to erosion and compaction."
    ),

    "Sandy Loam": (
        "Generally good drainage with moderate water "
        "retention. Monitor moisture during dry periods."
    ),

    "Clay Loam": (
        "Generally good moisture and nutrient retention. "
        "Monitor drainage and compaction."
    )
}

# ------------------------------------------
# SCORING FUNCTION
# ------------------------------------------

def calculate_rotation_score(rotation):

    # Water suitability
    water_score = rotation["water"] * 20

    # Use annual rainfall only as a coarse
    # water-stress screening indicator.
    if rainfall is not None:

        if rainfall < 500:
            water_score += (
                6 - rotation["water"]
            ) * 5

        elif rainfall > 1000:
            water_score += (
                rotation["water"] - 1
            ) * 2

    water_score = max(
        0,
        min(100, water_score)
    )

    # Soil improvement potential
    soil_score = 50 + rotation["cover"] * 10

    if soil_values["organic_carbon"] < 1.5:
        soil_score += 10

    if soil_values["pH"] < 5.5 or soil_values["pH"] > 7.5:
        soil_score -= 10

    soil_score = max(0, min(100, soil_score))

    # Nitrogen management potential
    nitrogen_score = (
        50 + rotation["legumes"] * 25
    )

    if soil_values["nitrogen"] < 100:
        nitrogen_score += 10

    nitrogen_score = max(
        0,
        min(100, nitrogen_score)
    )

    # Heat adaptation screening
    climate_score = rotation["heat"] * 20

    # Crop diversity
    diversity_score = rotation["diversity"] * 20

    components = {
        "water": water_score,
        "soil": soil_score,
        "nitrogen": nitrogen_score,
        "climate": climate_score,
        "diversity": diversity_score
    }

    selected_weights = weights[priority]

    final_score = sum(
        components[key] * selected_weights[key]
        for key in components
    )

    return round(final_score, 1), components

# ------------------------------------------
# GENERATE RECOMMENDATIONS
# ------------------------------------------

if "soil_profile" not in st.session_state:
    st.warning(
        "Please save your Farmer Soil Profile before "
        "generating crop rotation recommendations."
    )

if st.button(
    "🚀 Generate Crop Rotation Plan",
    type="primary",
    disabled=("soil_profile" not in st.session_state)
):

    results = []

    for rotation in rotations:

        score, components = calculate_rotation_score(
            rotation
        )

        results.append({
            "Rotation": rotation["name"],
            "Sequence": " → ".join(rotation["crops"]),
            "Score": score,
            "Components": components
        })

    results = sorted(
        results,
        key=lambda x: x["Score"],
        reverse=True
    )

    st.session_state["rotation_results"] = results
    st.session_state["rotation_location"] = current_location

# ------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------

if "rotation_results" in st.session_state:

    rotation_location = st.session_state.get("rotation_location")

    if rotation_location != current_location:

        st.warning(
            "Your crop rotation plan belongs to a different farm location. "
            "Please generate a new plan for the selected location."
        )

    else:

        results = st.session_state["rotation_results"]


        st.subheader("🏆 Recommended Rotation Strategies")

        best = results[0]

        st.success(
            f"Highest-scoring candidate: {best['Rotation']}"
        )

        st.metric(
            "Comparative Sustainability Score",
            f"{best['Score']}/100"
        )

        for index, result in enumerate(results):

            with st.expander(
                f"Strategy {index + 1}: {result['Rotation']} "
                f"– {result['Score']}/100",
                expanded=(index == 0)
            ):

                st.markdown(
                    f"**Three-year sequence:** "
                    f"{result['Sequence']}"
                )

                # Soil texture guidance
                st.info(
                    "🌱 Soil texture: "
                    + str(soil_values["texture"])
                    + "\n\n"
                    + texture_guidance[soil_values["texture"]]
                )

                # NASA soil wetness context
                st.markdown("**💧 NASA Soil Wetness Context**")

                if moisture_summary is not None:

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Surface",
                        f"{moisture_summary['Surface']:.3f}"
                    )

                    col2.metric(
                        "Root Zone",
                        f"{moisture_summary['Root Zone']:.3f}"
                    )

                    col3.metric(
                        "Soil Profile",
                        f"{moisture_summary['Profile']:.3f}"
                    )

                    st.caption(
                        "Recent average of available NASA POWER "
                        "soil-wetness observations. These indicators "
                        "provide environmental context and do not "
                        "directly determine the rotation score."
                    )

                else:

                    st.info(
                        "Retrieve NASA soil-wetness data to display "
                        "moisture context for this recommendation."
                    )

                # Scoring breakdown
                st.progress(int(result["Score"]))

                st.write("Scoring breakdown")

                for category, value in result["Components"].items():

                    st.write(
                        f"{category.title()}: {value:.0f}/100"
                    )

        # Comparison table
        comparison = pd.DataFrame([
            {
                "Rotation": item["Rotation"],
                "Crop Sequence": item["Sequence"],
                "Score": item["Score"]
            }
            for item in results
        ])

        st.subheader("📊 Rotation Comparison")

        st.dataframe(
            comparison,
            use_container_width=True
        )

        st.caption(
            "These scores are experimental, rule-based "
            "screening scores, not validated yield, "
            "profitability or soil-health predictions. "
            "Crop sequences require local agronomic validation."
        )

        st.download_button(
            "Download Rotation Comparison",
            data=comparison.to_csv(index=False),
            file_name="agriorbit_rotation_results.csv",
            mime="text/csv"
        )

# ==========================================
# CLIMATE WHAT-IF SIMULATOR
# ==========================================

st.divider()

st.header("🌦️ Climate What-If Simulator")

st.write(
    "Explore how hypothetical climate changes "
    "could affect the ranking of crop rotation strategies."
)

# Farmer scenario inputs

col1, col2 = st.columns(2)

with col1:

    rainfall_change = st.slider(
        "Change in rainfall (%)",
        min_value=-50,
        max_value=30,
        value=-20,
        step=5
    )

with col2:

    temperature_change = st.slider(
        "Temperature increase (°C)",
        min_value=0.0,
        max_value=5.0,
        value=2.0,
        step=0.5
    )

st.info(
    "These are hypothetical stress-test scenarios, "
    "not official NASA climate forecasts."
)

# Calculate scenario results

if st.button("🔮 Run Climate Simulation"):

    if (
        "rotation_results" not in st.session_state
        or st.session_state.get("rotation_location") != current_location
    ):

        st.warning(
            "Generate a fresh crop rotation plan for the selected farm location first."
        )

    else:

        baseline = st.session_state["rotation_results"]

        simulated_results = []

        for result in baseline:

            original_score = result["Score"]

            components = result["Components"]

            # Simplified scenario sensitivity.
            # These are prototype assumptions, not crop models.

            water_penalty = (
                abs(rainfall_change) / 50
            ) * (
                components["water"] / 100
            ) * 20

            heat_penalty = (
                temperature_change / 5
            ) * (
                100 - components["climate"]
            ) * 0.30

            simulated_score = max(
                0,
                min(
                    100,
                    original_score
                    - water_penalty
                    - heat_penalty
                )
            )

            simulated_results.append({

                "Rotation": result["Rotation"],

                "Baseline Score": original_score,

                "Scenario Score": round(
                    simulated_score, 1
                )

            })

        simulated_results = sorted(
            simulated_results,
            key=lambda x: x["Scenario Score"],
            reverse=True
        )

        st.session_state[
            "simulated_results"
        ] = simulated_results
        st.session_state["simulation_location"] = (
            round(latitude, 4),
            round(longitude, 4)
        )
        st.session_state[
            "scenario_settings"
        ] = {
            "rainfall_change": rainfall_change,
            "temperature_change": temperature_change
        }

# Display simulation

if (
    "simulated_results" in st.session_state
    and st.session_state.get("simulation_location")
    == (round(latitude, 4), round(longitude, 4))
):
    st.info(
        "Simulation results correspond to the currently selected farm location."
    )

    simulated = st.session_state[
        "simulated_results"
    ]

    st.subheader("📊 Simulation Results")

    best_strategy = simulated[0]

    st.success(
        "Highest-scoring strategy under this "
        f"scenario: {best_strategy['Rotation']}"
    )

    comparison_df = pd.DataFrame(simulated)

    fig = px.bar(

        comparison_df,

        x="Rotation",

        y=[
            "Baseline Score",
            "Scenario Score"
        ],

        barmode="group",

        title="Baseline vs Climate Scenario"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        comparison_df,
        use_container_width=True
    )

    st.download_button(

        "Download Climate Simulation",

        data=comparison_df.to_csv(
            index=False
        ),

        file_name="agriorbit_climate_simulation.csv",

        mime="text/csv"

    )

    st.caption(
        "Scenario scores are illustrative sensitivity "
        "scores derived from prototype assumptions. "
        "They do not represent validated future crop "
        "performance or climate projections."
    )

# ==========================================
# AGRIORBIT FARM ADAPTATION REPORT
# ==========================================

st.divider()

st.header("📄 AgriOrbit Farm Adaptation Report")

st.write(
    "Generate a consolidated report using the environmental "
    "and farm information available for your selected location."
)

if st.button("📄 Generate Farm Adaptation Report"):

    report_lines = []

    report_lines.append("AGRIORBIT FARM ADAPTATION REPORT")
    report_lines.append("=" * 45)
    report_lines.append(f"Report date: {date.today()}")
    report_lines.append(
        f"Farm coordinates: {current_location[0]}, "
        f"{current_location[1]}"
    )

    # EXECUTIVE SUMMARY
    report_lines.append("")
    report_lines.append("EXECUTIVE SUMMARY")
    report_lines.append("-" * 30)

    report_lines.append(
        "AgriOrbit is a farm adaptation decision-support "
        "prototype developed by Siddhi Services."
    )

    report_lines.append(
        f"Selected farmer priority: "
        f"{st.session_state.get('farmer_priority', 'Not selected')}"
    )

    report_lines.append(
        f"Environmental data streams available: "
        f"{sum([climate_ready, wetness_ready, ndvi_ready])}/3"
    )

    report_lines.append(
        "The assessment combines available climate, "
        "modeled soil-wetness and vegetation indicators "
        "with farmer-entered soil information."
    )

    report_lines.append(
        "The findings are intended to support preliminary "
        "farm planning and should be verified against "
        "actual field conditions."
    )

    # KEY FINDINGS
    report_lines.append("")
    report_lines.append("KEY FINDINGS")
    report_lines.append("-" * 30)

    key_findings = []

    if climate_ready:
        climate_summary_df = st.session_state["climate_data"]

        average_temperature = (
            climate_summary_df["Temperature"].mean()
        )

        total_rainfall = (
            climate_summary_df["Rainfall"].sum()
        )

        key_findings.append(
            f"Climate: Average temperature is "
            f"{average_temperature:.2f} °C, with "
            f"{total_rainfall:.1f} mm total precipitation "
            f"over the available observation period."
        )
    else:
        key_findings.append(
            "Climate: Data has not been retrieved for this location."
        )

    if wetness_ready:
        wetness_summary_df = st.session_state["smap_data"]

        key_findings.append(
            "Soil wetness: NASA POWER modeled surface, "
            "root-zone and profile wetness indicators are available."
        )
    else:
        key_findings.append(
            "Soil wetness: Data is not currently available."
        )

    if ndvi_ready:
        ndvi_summary_df = st.session_state["ndvi_data"]

        latest_ndvi = ndvi_summary_df["NDVI"].iloc[-1]

        key_findings.append(
            f"Vegetation: Latest available MODIS NDVI is "
            f"{latest_ndvi:.3f}."
        )
    else:
        key_findings.append(
            "Vegetation: MODIS NDVI data is not currently available."
        )

    if (
        "rotation_results" in st.session_state
        and st.session_state.get("rotation_location")
        == current_location
        and st.session_state["rotation_results"]
    ):
        summary_rotation = st.session_state["rotation_results"][0]

        key_findings.append(
            f"Crop rotation: Highest-ranked strategy is "
            f"{summary_rotation['Rotation']} with a "
            f"comparative score of {summary_rotation['Score']}/100."
        )
    else:
        key_findings.append(
            "Crop rotation: No current-location strategy "
            "has been generated."
        )

    for finding_number, finding in enumerate(
        key_findings, start=1
    ):
        report_lines.append(
            f"{finding_number}. {finding}"
        )

    report_lines.append("")

    report_lines.append("")
    report_lines.append("1. FARM SOIL PROFILE")
    report_lines.append("-" * 30)

    report_lines.append(f"Soil pH: {soil_values['pH']}")
    report_lines.append(
        f"Organic Carbon: {soil_values['organic_carbon']}%"
    )
    report_lines.append(
        f"Available Nitrogen: {soil_values['nitrogen']} mg/kg"
    )
    report_lines.append(
        f"Soil Texture: {soil_values['texture']}"
    )

    report_lines.append("")
    report_lines.append("2. NASA POWER CLIMATE ASSESSMENT")
    report_lines.append("-" * 30)

    if climate_ready:

        climate_df = st.session_state["climate_data"]

        report_lines.append(
            f"Average Temperature: "
            f"{climate_df['Temperature'].mean():.2f} °C"
        )

        report_lines.append(
            f"Total Precipitation: "
            f"{climate_df['Rainfall'].sum():.1f} mm"
        )

        report_lines.append(
            f"Observation Period: "
            f"{climate_df['Date'].min().date()} to "
            f"{climate_df['Date'].max().date()}"
        )

    else:
        report_lines.append(
            "Climate data: Not retrieved for this location."
        )

    report_lines.append("")
    report_lines.append("3. SOIL WETNESS ASSESSMENT")
    report_lines.append("-" * 30)

    if wetness_ready:

        wetness_df = st.session_state["smap_data"]

        report_lines.append(
            f"Average Surface Wetness: "
            f"{wetness_df['Surface Moisture'].mean():.3f}"
        )

        report_lines.append(
            f"Average Root Zone Wetness: "
            f"{wetness_df['Root Zone Moisture'].mean():.3f}"
        )

        report_lines.append(
            f"Average Profile Wetness: "
            f"{wetness_df['Profile Moisture'].mean():.3f}"
        )

    else:
        report_lines.append(
            "Soil wetness data: Not retrieved for this location."
        )

    report_lines.append("")
    report_lines.append("4. MODIS VEGETATION ASSESSMENT")
    report_lines.append("-" * 30)

    if ndvi_ready:

        ndvi_df = st.session_state["ndvi_data"]

        report_lines.append(
            f"Latest NDVI: {ndvi_df['NDVI'].iloc[-1]:.3f}"
        )

        report_lines.append(
            f"Latest Observation: "
            f"{ndvi_df['Date'].max().date()}"
        )

        report_lines.append(
            f"Valid Observations: {len(ndvi_df)}"
        )

    else:
        report_lines.append(
            "MODIS NDVI: Not retrieved for this location."
        )

    report_lines.append("")
    report_lines.append("5. CROP ROTATION STRATEGY")
    report_lines.append("-" * 30)

    if (
        "rotation_results" in st.session_state
        and st.session_state.get("rotation_location")
        == current_location
    ):

        best_rotation = st.session_state["rotation_results"][0]

        report_lines.append(
            f"Recommended Strategy: {best_rotation['Rotation']}"
        )

        report_lines.append(
            f"Crop Sequence: {best_rotation['Sequence']}"
        )

        report_lines.append(
            f"Comparative Score: {best_rotation['Score']}/100"
        )

    else:
        report_lines.append(
            "No current-location crop rotation plan available."
        )

    report_lines.append("")
    report_lines.append("6. CLIMATE WHAT-IF SIMULATION")
    report_lines.append("-" * 30)

    if (
        "simulated_results" in st.session_state
        and st.session_state.get("simulation_location")
        == current_location
    ):

        simulation = st.session_state["simulated_results"]

        report_lines.append(
            f"Top Strategy: {simulation[0]['Rotation']}"
        )

        report_lines.append(
            f"Scenario Score: "
            f"{simulation[0]['Scenario Score']}/100"
        )

    else:
        report_lines.append(
            "No current-location simulation available."
        )

    report_lines.append("")
    report_lines.append("7. DATA COMPLETENESS AND RETRIEVAL TIMES")
    report_lines.append("-" * 40)

    # Climate data completeness
    if climate_ready:
        climate_df = st.session_state["climate_data"]

        expected_days = (
            st.session_state["climate_requested_end"]
            - st.session_state["climate_requested_start"]
        ).days + 1

        valid_days = climate_df["Date"].nunique()

        if expected_days > 0:
            climate_completeness = (
                valid_days / expected_days
            ) * 100

            report_lines.append(
                f"Climate completeness: "
                f"{climate_completeness:.1f}% "
                f"({valid_days}/{expected_days} days)"
            )

        climate_time = st.session_state.get(
            "climate_retrieved_at"
        )

        report_lines.append(
            "Climate retrieval time: "
            + (
                climate_time.strftime("%d %b %Y, %H:%M")
                if climate_time is not None
                else "Not recorded"
            )
        )
    else:
        report_lines.append("Climate completeness: Not available")

    # Soil wetness data completeness
    if wetness_ready:
        wetness_df = st.session_state["smap_data"]

        expected_wetness_days = (
            st.session_state["wetness_requested_end"]
            - st.session_state["wetness_requested_start"]
        ).days + 1

        valid_wetness_days = wetness_df["Date"].nunique()

        if expected_wetness_days > 0:
            wetness_completeness = (
                valid_wetness_days / expected_wetness_days
            ) * 100

            report_lines.append(
                f"Soil wetness completeness: "
                f"{wetness_completeness:.1f}% "
                f"({valid_wetness_days}/{expected_wetness_days} days)"
            )

        wetness_time = st.session_state.get(
            "wetness_retrieved_at"
        )

        report_lines.append(
            "Soil wetness retrieval time: "
            + (
                wetness_time.strftime("%d %b %Y, %H:%M")
                if wetness_time is not None
                else "Not recorded"
            )
        )
    else:
        report_lines.append(
            "Soil wetness completeness: Not available"
        )

    # MODIS retrieval time
    if ndvi_ready:
        ndvi_time = st.session_state.get("ndvi_retrieved_at")

        report_lines.append(
            "MODIS valid observations: "
            f"{len(st.session_state['ndvi_data'])}"
        )

        report_lines.append(
            "MODIS retrieval time: "
            + (
                ndvi_time.strftime("%d %b %Y, %H:%M")
                if ndvi_time is not None
                else "Not recorded"
            )
        )
    else:
        report_lines.append("MODIS retrieval time: Not available")

    report_lines.append(
        "Note: MODIS uses 16-day composite observations; "
        "daily completeness percentage is not applicable."
    )

    # Smart Farm Insights and Alerts
    report_lines.append("")
    report_lines.append("8. SMART FARM INSIGHTS AND ALERTS")
    report_lines.append("-" * 40)

    if smart_insights:

        for severity, title, message in smart_insights:

            report_lines.append(
                f"[{severity.upper()}] {title}"
            )

            report_lines.append(message)
            report_lines.append("")

    else:

        report_lines.append(
            "No smart insights were generated for this location."
        )

    # Record the climate comparison window
    if dashboard_climate_ready and len(dashboard_climate_df) >= 60:

        climate_sorted = (
            dashboard_climate_df
            .sort_values("Date")
            .reset_index(drop=True)
        )

        report_lines.append(
            "Climate comparison windows:"
        )

        report_lines.append(
            f"Earlier period: "
            f"{climate_sorted['Date'].iloc[-60].date()} to "
            f"{climate_sorted['Date'].iloc[-31].date()}"
        )

        report_lines.append(
            f"Recent period: "
            f"{climate_sorted['Date'].iloc[-30].date()} to "
            f"{climate_sorted['Date'].iloc[-1].date()}"
        )

    # Record the soil-wetness comparison window
    if dashboard_wetness_ready and len(dashboard_wetness_df) >= 14:

        wetness_sorted = (
            dashboard_wetness_df
            .sort_values("Date")
            .reset_index(drop=True)
        )

        report_lines.append(
            "Soil-wetness comparison windows:"
        )

        report_lines.append(
            f"Earlier period: "
            f"{wetness_sorted['Date'].iloc[-14].date()} to "
            f"{wetness_sorted['Date'].iloc[-8].date()}"
        )

        report_lines.append(
            f"Recent period: "
            f"{wetness_sorted['Date'].iloc[-7].date()} to "
            f"{wetness_sorted['Date'].iloc[-1].date()}"
        )

    # Record the NDVI comparison window
    if dashboard_ndvi_ready and len(dashboard_ndvi_df) >= 2:

        ndvi_sorted = (
            dashboard_ndvi_df
            .sort_values("Date")
            .reset_index(drop=True)
        )

        report_lines.append(
            "MODIS NDVI comparison dates: "
            f"{ndvi_sorted['Date'].iloc[-2].date()} and "
            f"{ndvi_sorted['Date'].iloc[-1].date()}"
        )

    report_lines.append("")
    report_lines.append(
        "Alert thresholds are experimental comparison rules, "
        "not validated agricultural warning thresholds."
    )

    report_lines.append(
        "Climate and soil-wetness values are modeled or "
        "gridded indicators. NDVI represents vegetation "
        "greenness, not direct crop yield."
    )

    report_lines.append(
        "These insights should be checked against actual "
        "farm conditions and local agronomic advice."
    )

    report_lines.append("")

    report_lines.append("9. DATA LIMITATIONS")
    report_lines.append("-" * 30)

    report_lines.append(
        "NASA POWER climate and soil-wetness values are "
        "gridded or modeled environmental estimates."
    )

    report_lines.append(
        "MODIS NDVI indicates vegetation greenness, "
        "not direct crop yield."
    )

    report_lines.append(
        "Crop rotation scores and climate scenarios are "
        "experimental screening tools, not validated "
        "agronomic predictions."
    )

    report_lines.append("")
    report_lines.append(
        "Prepared by Siddhi Services | AgriOrbit"
    )

    st.session_state["farm_adaptation_report"] = (
        "\n".join(report_lines)
    )

    st.session_state["farm_adaptation_report_location"] = (
        current_location
    )

    st.success("Farm Adaptation Report generated successfully!")

# Display and download the report

if "farm_adaptation_report" in st.session_state:

    if (
        st.session_state.get("farm_adaptation_report_location")
        == current_location
    ):

        st.subheader("📋 Report Preview")

        st.text_area(
            "Generated report",
            value=st.session_state["farm_adaptation_report"],
            height=400,
            disabled=True
        )

        st.download_button(
            "⬇️ Download Farm Adaptation Report",
            data=st.session_state["farm_adaptation_report"],
            file_name="AgriOrbit_Farm_Adaptation_Report.txt",
            mime="text/plain"
        )

        # Generate professional PDF report
        pdf_buffer = io.BytesIO()

        pdf_doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=45,
            leftMargin=45,
            topMargin=55,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()

        
        # Premium AgriOrbit cover title
        cover_title = ParagraphStyle(
            "CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=32,
            leading=40,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#176B45"),
            spaceAfter=18
        )

        # Cover page subtitle
        cover_subtitle = ParagraphStyle(
            "CoverSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#52645A"),
            spaceAfter=8
        )

        # Cover page information panel
        cover_info = ParagraphStyle(
            "CoverInfo",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#176B45"),
            backColor=colors.HexColor("#EEF6F0"),
            borderColor=colors.HexColor("#176B45"),
            borderWidth=1,
            borderPadding=12,
            spaceBefore=10,
            spaceAfter=10
        )
        
        # Professional report section heading
        section_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=18,
            textColor=colors.HexColor("#176B45"),
            backColor=colors.HexColor("#EEF6F0"),
            borderColor=colors.HexColor("#176B45"),
            borderWidth=0.8,
            borderPadding=7,
            spaceBefore=16,
            spaceAfter=10,
            keepWithNext=1
        )

        # Clean and readable report body
        body_style = ParagraphStyle(
            "ReportBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#26352D"),
            spaceAfter=7
        )


        # Footer with page numbers
        
        # Professional PDF header and footer
        def draw_pdf_footer(canvas, document):

            canvas.saveState()

            # Header title
            canvas.setFont("Helvetica-Bold", 9)
            canvas.setFillColor(
                colors.HexColor("#176B45")
            )

            canvas.drawString(
                45,
                A4[1] - 30,
                "AGRIORBIT | FARM ADAPTATION REPORT"
            )

            # Header divider
            canvas.setStrokeColor(
                colors.HexColor("#176B45")
            )

            canvas.setLineWidth(1.2)

            canvas.line(
                45,
                A4[1] - 40,
                A4[0] - 45,
                A4[1] - 40
            )

            # Footer divider
            canvas.setStrokeColor(
                colors.HexColor("#D0D7D3")
            )

            canvas.setLineWidth(0.6)

            canvas.line(
                45,
                32,
                A4[0] - 45,
                32
            )

            # Footer text
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(
                colors.HexColor("#666666")
            )

            canvas.drawString(
                45,
                20,
                "Prepared by Siddhi Services"
            )

            canvas.drawRightString(
                A4[0] - 45,
                20,
                f"Page {document.page}"
            )

            canvas.restoreState()


        # Cover page
        story = []

        story.append(Spacer(1, 110))

        story.append(
            Paragraph(
                "AGRIORBIT",
                cover_title
            )
        )

        story.append(
            Paragraph(
                "FARM ADAPTATION REPORT",
                cover_subtitle
            )
        )

        story.append(Spacer(1, 25))

        story.append(
            Paragraph(
                "NASA Earth Observation and "
                "Farm Adaptation Decision Support",
                cover_subtitle
            )
        )

        story.append(Spacer(1, 50))

        
        story.append(
            Paragraph(
                f"REPORT DATE: {date.today()}<br/>"
                f"FARM COORDINATES: "
                f"{current_location[0]}, "
                f"{current_location[1]}",
                cover_info
            )
        )


        story.append(Spacer(1, 80))

        story.append(
            Paragraph(
                "Prepared by Siddhi Services",
                cover_subtitle
            )
        )

        story.append(PageBreak())

        # PDF EXECUTIVE SUMMARY PAGE

        story.append(Paragraph(
            "EXECUTIVE SUMMARY",
            section_style
        ))
        story.append(Spacer(1, 10))

        # Check environmental data for the selected location
        pdf_climate_ready = (
            isinstance(st.session_state.get("climate_data"), pd.DataFrame)
            and not st.session_state["climate_data"].empty
            and st.session_state.get("climate_data_location")
            == current_location
        )

        pdf_wetness_ready = (
            isinstance(st.session_state.get("smap_data"), pd.DataFrame)
            and not st.session_state["smap_data"].empty
            and st.session_state.get("wetness_data_location")
            == current_location
        )

        pdf_ndvi_ready = (
            isinstance(st.session_state.get("ndvi_data"), pd.DataFrame)
            and not st.session_state["ndvi_data"].empty
            and st.session_state.get("ndvi_data_location")
            == current_location
        )

        pdf_rotation_ready = (
            bool(st.session_state.get("rotation_results"))
            and st.session_state.get("rotation_location")
            == current_location
        )

        pdf_soil_profile = st.session_state.get("soil_profile", {})

        pdf_priority = st.session_state.get(
            "farmer_priority",
            "Not selected"
        )

        # Project overview
        story.append(Paragraph(
            "<b>Project:</b> AgriOrbit - NASA-powered farm adaptation "
            "decision-support prototype developed by Siddhi Services.",
            body_style
        ))

        story.append(Paragraph(
            f"<b>Report date:</b> {date.today()}",
            body_style
        ))

        story.append(Paragraph(
            f"<b>Farm coordinates:</b> "
            f"{current_location[0]}, {current_location[1]}",
            body_style
        ))

        story.append(Paragraph(
            f"<b>Farmer priority:</b> {escape(str(pdf_priority))}",
            body_style
        ))

        story.append(Spacer(1, 10))

        # Environmental data availability
        story.append(Paragraph(
            "<b>ENVIRONMENTAL DATA AVAILABILITY</b>",
            section_style
        ))

        story.append(Paragraph(
            f"NASA POWER Climate: "
            f"{'Available' if pdf_climate_ready else 'Not available'}",
            body_style
        ))

        story.append(Paragraph(
            f"NASA POWER Soil Wetness: "
            f"{'Available' if pdf_wetness_ready else 'Not available'}",
            body_style
        ))

        story.append(Paragraph(
            f"NASA MODIS NDVI: "
            f"{'Available' if pdf_ndvi_ready else 'Not available'}",
            body_style
        ))

        story.append(Spacer(1, 10))

        # Climate snapshot
        story.append(Paragraph(
            "<b>KEY ENVIRONMENTAL FINDINGS</b>",
            section_style
        ))

        if pdf_climate_ready:
            pdf_climate = st.session_state["climate_data"]

            story.append(Paragraph(
                f"Average temperature: "
                f"{pdf_climate['Temperature'].mean():.1f} degrees C",
                body_style
            ))

            story.append(Paragraph(
                f"Total recorded precipitation: "
                f"{pdf_climate['Rainfall'].sum():.1f} mm",
                body_style
            ))
        else:
            story.append(Paragraph(
                "Climate observations are not available for this location.",
                body_style
            ))

        if pdf_wetness_ready:
            pdf_wetness = st.session_state["smap_data"].iloc[-1]

            story.append(Paragraph(
                f"Latest modeled surface wetness: "
                f"{pdf_wetness['Surface Moisture']:.3f}",
                body_style
            ))

            story.append(Paragraph(
                f"Latest modeled root-zone wetness: "
                f"{pdf_wetness['Root Zone Moisture']:.3f}",
                body_style
            ))

        if pdf_ndvi_ready:
            pdf_ndvi = st.session_state["ndvi_data"]

            story.append(Paragraph(
                f"Latest vegetation NDVI: "
                f"{pdf_ndvi['NDVI'].iloc[-1]:.3f}",
                body_style
            ))

        story.append(Spacer(1, 10))

        # Farm planning summary
        story.append(Paragraph(
            "<b>FARM ADAPTATION PLANNING</b>",
            section_style
        ))

        if pdf_soil_profile:
            story.append(Paragraph(
                f"Soil profile saved: Yes | "
                f"pH: {pdf_soil_profile.get('pH', 'N/A')} | "
                f"Texture: {escape(str(pdf_soil_profile.get('texture', 'N/A')))}",
                body_style
            ))
        else:
            story.append(Paragraph(
                "Soil profile: Not saved",
                body_style
            ))

        if pdf_rotation_ready:
            pdf_best_rotation = st.session_state["rotation_results"][0]

            story.append(Paragraph(
                f"Top-ranked crop rotation: "
                f"{escape(str(pdf_best_rotation['Rotation']))}",
                body_style
            ))

            story.append(Paragraph(
                f"Comparative screening score: "
                f"{pdf_best_rotation['Score']}/100",
                body_style
            ))
        else:
            story.append(Paragraph(
                "Crop rotation strategy: Not generated",
                body_style
            ))

        pdf_simulation_ready = (
            bool(st.session_state.get("simulated_results"))
            and st.session_state.get("simulation_location")
            == current_location
        )

        story.append(Paragraph(
            f"Climate scenario simulation: "
            f"{'Generated' if pdf_simulation_ready else 'Not generated'}",
            body_style
        ))

        story.append(Spacer(1, 12))

        # Interpretation note
        story.append(Paragraph(
            "<b>Overall interpretation:</b> This summary reflects "
            "the environmental data and farm-planning information "
            "available for the selected location at report generation. "
            "Missing data is not treated as zero. Crop rotation scores "
            "are experimental comparative screening indicators, "
            "not validated agronomic predictions.",
            body_style
        ))

        # Start charts on a new page
        story.append(PageBreak())

        # Add NASA POWER climate charts to PDF

        climate_pdf_df = st.session_state.get(
            "climate_data"
        )

        climate_pdf_location = st.session_state.get(
            "climate_data_location"
        )

        if (
            isinstance(climate_pdf_df, pd.DataFrame)
            and climate_pdf_location == current_location
            and not climate_pdf_df.empty
        ):

            climate_plot_df = climate_pdf_df.copy()

            climate_plot_df["Date"] = pd.to_datetime(
                climate_plot_df["Date"],
                errors="coerce"
            )

            climate_plot_df = climate_plot_df.dropna(
                subset=["Date", "Temperature", "Rainfall"]
            )

            if not climate_plot_df.empty:

                monthly_rainfall_pdf = (
                    climate_plot_df
                    .set_index("Date")["Rainfall"]
                    .resample("MS")
                    .sum()
                )

                fig, (ax1, ax2) = plt.subplots(
                    2, 1,
                    figsize=(10, 6),
                    sharex=True
                )

                # Temperature chart
                ax1.plot(
                    climate_plot_df["Date"],
                    climate_plot_df["Temperature"]
                )

                ax1.set_title(
                    "Daily Average Temperature"
                )

                ax1.set_ylabel(
                    "Temperature (degrees C)"
                )

                ax1.grid(True, alpha=0.3)

                # Monthly rainfall chart
                ax2.bar(
                    monthly_rainfall_pdf.index,
                    monthly_rainfall_pdf.values,
                    width=20
                )

                ax2.set_title(
                    "Monthly Total Precipitation"
                )

                ax2.set_ylabel(
                    "Rainfall (mm)"
                )

                ax2.set_xlabel(
                    "Date"
                )

                ax2.grid(True, alpha=0.3)

                fig.tight_layout()

                # Save chart temporarily in memory
                climate_chart_buffer = io.BytesIO()

                fig.savefig(
                    climate_chart_buffer,
                    format="png",
                    dpi=180,
                    bbox_inches="tight"
                )

                plt.close(fig)

                climate_chart_buffer.seek(0)

                # Add chart to PDF
                story.append(
                    Paragraph(
                        "NASA POWER CLIMATE TRENDS",
                        section_style
                    )
                )

                story.append(
                    Spacer(1, 10)
                )

                story.append(
                    Image(
                        climate_chart_buffer,
                        width=460,
                        height=230
                    )
                )

                story.append(
                    Spacer(1, 15)
                )
                        # Add NASA POWER soil wetness chart to PDF

        wetness_pdf_df = st.session_state.get(
            "smap_data"
        )

        wetness_pdf_location = st.session_state.get(
            "wetness_data_location"
        )

        if (
            isinstance(wetness_pdf_df, pd.DataFrame)
            and wetness_pdf_location == current_location
            and not wetness_pdf_df.empty
        ):

            wetness_plot_df = wetness_pdf_df.copy()

            wetness_plot_df["Date"] = pd.to_datetime(
                wetness_plot_df["Date"],
                errors="coerce"
            )

            moisture_columns = [
                "Surface Moisture",
                "Root Zone Moisture",
                "Profile Moisture"
            ]

            wetness_plot_df = wetness_plot_df.dropna(
                subset=["Date"] + moisture_columns
            )

            if not wetness_plot_df.empty:

                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )

                for column in moisture_columns:

                    ax.plot(
                        wetness_plot_df["Date"],
                        wetness_plot_df[column],
                        label=column
                    )

                ax.set_title(
                    "NASA POWER Soil Wetness Indicators"
                )

                ax.set_xlabel("Date")

                ax.set_ylabel(
                    "Relative Wetness (0-1)"
                )

                ax.legend()

                ax.grid(True, alpha=0.3)

                fig.tight_layout()

                wetness_chart_buffer = io.BytesIO()

                fig.savefig(
                    wetness_chart_buffer,
                    format="png",
                    dpi=180,
                    bbox_inches="tight"
                )

                plt.close(fig)

                wetness_chart_buffer.seek(0)

                story.append(
                    Paragraph(
                        "NASA POWER SOIL WETNESS TRENDS",
                        section_style
                    )
                )

                story.append(
                    Spacer(1, 10)
                )

                story.append(
                    Image(
                        wetness_chart_buffer,
                        width=460,
                        height=230
                    )
                )

                story.append(
                    Spacer(1, 15)
                )

                story.append(
                    Paragraph(
                        "Note: These are modeled soil-wetness "
                        "indicators, not direct SMAP Level-4 "
                        "measurements or field laboratory results.",
                        body_style
                    )
                )
                        # Add MODIS NDVI vegetation chart to PDF

        ndvi_pdf_df = st.session_state.get(
            "ndvi_data"
        )

        ndvi_pdf_location = st.session_state.get(
            "ndvi_data_location"
        )

        if (
            isinstance(ndvi_pdf_df, pd.DataFrame)
            and ndvi_pdf_location == current_location
            and not ndvi_pdf_df.empty
        ):

            ndvi_plot_df = ndvi_pdf_df.copy()

            ndvi_plot_df["Date"] = pd.to_datetime(
                ndvi_plot_df["Date"],
                errors="coerce"
            )

            ndvi_plot_df["NDVI"] = pd.to_numeric(
                ndvi_plot_df["NDVI"],
                errors="coerce"
            )

            ndvi_plot_df = ndvi_plot_df.dropna(
                subset=["Date", "NDVI"]
            )

            if not ndvi_plot_df.empty:

                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )

                ax.plot(
                    ndvi_plot_df["Date"],
                    ndvi_plot_df["NDVI"],
                    marker="o"
                )

                ax.set_title(
                    "MODIS Vegetation Greenness (NDVI)"
                )

                ax.set_xlabel(
                    "Observation Date"
                )

                ax.set_ylabel(
                    "NDVI"
                )

                ax.grid(True, alpha=0.3)

                fig.tight_layout()

                ndvi_chart_buffer = io.BytesIO()

                fig.savefig(
                    ndvi_chart_buffer,
                    format="png",
                    dpi=180,
                    bbox_inches="tight"
                )

                plt.close(fig)

                ndvi_chart_buffer.seek(0)

                story.append(
                    Paragraph(
                        "MODIS VEGETATION GREENNESS TRENDS",
                        section_style
                    )
                )

                story.append(
                    Spacer(1, 10)
                )

                story.append(
                    Image(
                        ndvi_chart_buffer,
                        width=460,
                        height=230
                    )
                )

                story.append(
                    Spacer(1, 10)
                )

                story.append(
                    Paragraph(
                        "Note: NDVI indicates vegetation greenness. "
                        "It does not directly measure crop yield "
                        "or provide a definitive crop-health diagnosis.",
                        body_style
                    )
                )
                        # Add crop rotation comparison chart to PDF

        rotation_pdf_results = st.session_state.get(
            "rotation_results"
        )

        rotation_pdf_location = st.session_state.get(
            "rotation_location"
        )

        if (
            isinstance(rotation_pdf_results, list)
            and rotation_pdf_location == current_location
            and len(rotation_pdf_results) > 0
        ):

            rotation_pdf_df = pd.DataFrame(
                rotation_pdf_results
            )

            if (
                "Rotation" in rotation_pdf_df.columns
                and "Score" in rotation_pdf_df.columns
            ):

                rotation_pdf_df["Score"] = pd.to_numeric(
                    rotation_pdf_df["Score"],
                    errors="coerce"
                )

                rotation_pdf_df = rotation_pdf_df.dropna(
                    subset=["Score"]
                )

                if not rotation_pdf_df.empty:

                    fig, ax = plt.subplots(
                        figsize=(10, 5)
                    )

                    ax.barh(
                        rotation_pdf_df["Rotation"],
                        rotation_pdf_df["Score"]
                    )

                    ax.set_title(
                        "Crop Rotation Strategy Comparison"
                    )

                    ax.set_xlabel(
                        "Comparative Sustainability Score"
                    )

                    ax.set_xlim(0, 100)

                    ax.invert_yaxis()

                    ax.grid(
                        axis="x",
                        alpha=0.3
                    )

                    for index, score in enumerate(
                        rotation_pdf_df["Score"]
                    ):

                        ax.text(
                            score + 1,
                            index,
                            f"{score:.1f}",
                            va="center"
                        )

                    fig.tight_layout()

                    rotation_chart_buffer = io.BytesIO()

                    fig.savefig(
                        rotation_chart_buffer,
                        format="png",
                        dpi=180,
                        bbox_inches="tight"
                    )

                    plt.close(fig)

                    rotation_chart_buffer.seek(0)

                    story.append(
                        Paragraph(
                            "CROP ROTATION STRATEGY COMPARISON",
                            section_style
                        )
                    )

                    story.append(
                        Spacer(1, 10)
                    )

                    story.append(
                        Image(
                            rotation_chart_buffer,
                            width=460,
                            height=230
                        )
                    )

                    story.append(
                        Spacer(1, 10)
                    )

                    story.append(
                        Paragraph(
                            "Note: These scores are experimental "
                            "comparative screening scores based on "
                            "AgriOrbit prototype assumptions. They "
                            "are not validated agronomic predictions.",
                            body_style
                        )
                    )
                            # PDF Data Sources and Limitations page
        story.append(PageBreak())

        story.append(Paragraph(
            "DATA SOURCES &amp; LIMITATIONS",
            section_style
        ))
        story.append(Spacer(1, 12))

        story.append(Paragraph(
            "<b>1. NASA POWER - Climate Data</b>",
            body_style
        ))
        story.append(Paragraph(
            "AgriOrbit retrieves temperature (T2M) and precipitation "
            "(PRECTOTCORR) data from NASA POWER. These are gridded "
            "environmental data products and may not represent the exact "
            "conditions measured at an individual farm.",
            body_style
        ))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "<b>2. NASA POWER - Soil Wetness Indicators</b>",
            body_style
        ))
        story.append(Paragraph(
            "The application uses GWETTOP, GWETROOT and GWETPROF from "
            "the NASA POWER Agroclimatology community. These represent "
            "modeled soil-wetness indicators for different soil depths. "
            "They are not direct field measurements, laboratory soil "
            "tests or SMAP Level-4 soil-moisture observations.",
            body_style
        ))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "<b>3. NASA MODIS - Vegetation Index</b>",
            body_style
        ))
        story.append(Paragraph(
            "AgriOrbit uses MODIS MOD13Q1 NDVI data to assess vegetation "
            "greenness where retrieval is available. NDVI is an indicator "
            "of vegetation condition; it does not directly measure crop "
            "yield, plant disease or soil fertility.",
            body_style
        ))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "<b>4. Farmer-Provided Soil Profile</b>",
            body_style
        ))
        story.append(Paragraph(
            "Soil pH, organic carbon, nitrogen and texture are based on "
            "the information entered by the farmer. Their accuracy depends "
            "on the quality and recency of the supplied information.",
            body_style
        ))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "<b>5. Crop Rotation and Adaptation Scores</b>",
            body_style
        ))
        story.append(Paragraph(
            "Crop rotation rankings and adaptation scores are experimental "
            "decision-support outputs. They are comparative screening "
            "indicators, not validated agronomic predictions or guarantees "
            "of crop performance.",
            body_style
        ))
        story.append(Spacer(1, 10))

        story.append(Paragraph(
            "<b>6. Data Availability and Interpretation</b>",
            body_style
        ))
        story.append(Paragraph(
            "Data availability depends on the relevant NASA service, "
            "location coverage and successful retrieval. Missing or "
            "unavailable observations should not be interpreted as zero "
            "values. Climate simulations are hypothetical scenarios, "
            "not weather forecasts.",
            body_style
        ))
        story.append(Spacer(1, 14))

        story.append(Paragraph(
            "<b>Important:</b> AgriOrbit is an experimental farm "
            "adaptation and decision-support prototype. Its outputs "
            "should be interpreted alongside local observations, "
            "soil testing and qualified agricultural advice.",
            body_style
        ))

        story.append(PageBreak())
        # Convert existing TXT report into PDF sections
        report_text = st.session_state[
            "farm_adaptation_report"
        ]

        for original_line in report_text.splitlines():

            line = original_line.strip()

            if not line:
                story.append(Spacer(1, 5))
                continue

            if set(line) <= {"=", "-"}:
                continue

            # Keep PDF text compatible with standard fonts
            line = (
                line.replace("°", " degrees")
                .replace("–", "-")
                .replace("—", "-")
                .encode("ascii", "replace")
                .decode("ascii")
            )

            safe_line = escape(line)

            is_heading = (
                line.isupper()
                and any(character.isalpha() for character in line)
                and len(line) < 100
            )

            if is_heading:
                story.append(
                    Paragraph(
                        safe_line,
                        section_style
                    )
                )
            else:
                story.append(
                    Paragraph(
                        safe_line,
                        body_style
                    )
                )

        # Build PDF
        pdf_doc.build(
            story,
            onFirstPage=draw_pdf_footer,
            onLaterPages=draw_pdf_footer
        )

        pdf_bytes = pdf_buffer.getvalue()

        st.download_button(
            "📕 Download Farm Adaptation Report (PDF)",
            data=pdf_bytes,
            file_name="AgriOrbit_Farm_Adaptation_Report.pdf",
            mime="application/pdf"
        )

    else:

        st.warning(
            "This report belongs to a different farm location. "
            "Generate a new report for the selected location."
        )
# ==========================================
# AGRIORBIT FARM ADAPTATION SCORECARD
# ==========================================

st.divider()

st.header("🏆 Farm Adaptation Scorecard")

st.write(
    "A live overview of environmental data availability "
    "and farm-planning progress for the selected location."
)

# Check current-location crop rotation plan

rotation_ready = (
    "rotation_results" in st.session_state
    and st.session_state.get("rotation_location")
    == current_location
    and bool(st.session_state.get("rotation_results"))
)

# Check current-location climate simulation

simulation_ready = (
    "simulated_results" in st.session_state
    and st.session_state.get("simulation_location")
    == current_location
    and bool(st.session_state.get("simulated_results"))
)

# Count available environmental data streams

available_streams = sum([
    climate_ready,
    wetness_ready,
    ndvi_ready
])

st.metric(
    "Environmental Data Streams Available",
    f"{available_streams}/3"
)

st.divider()

# Environmental data status

st.subheader("🛰️ Environmental Data")

data_col1, data_col2, data_col3 = st.columns(3)

with data_col1:
    st.metric(
        "Climate Data",
        "Available" if climate_ready else "Needs Retrieval"
    )

with data_col2:
    st.metric(
        "Soil Wetness",
        "Available" if wetness_ready else "Needs Retrieval"
    )

with data_col3:
    st.metric(
        "MODIS Vegetation",
        "Available" if ndvi_ready else "Needs Retrieval"
    )

st.divider()

# Farm planning status

st.subheader("🌱 Farm Planning Progress")

plan_col1, plan_col2, plan_col3 = st.columns(3)

with plan_col1:
    st.metric(
        "Farmer Soil Profile",
        "Saved" if "soil_profile" in st.session_state
        else "Not Saved"
    )

with plan_col2:
    st.metric(
        "Crop Rotation Plan",
        "Generated" if rotation_ready
        else "Not Generated"
    )

with plan_col3:
    st.metric(
        "Climate Simulation",
        "Generated" if simulation_ready
        else "Not Generated"
    )

st.divider()

# Selected farmer priority

st.subheader("🎯 Selected Farmer Priority")

st.info(
    f"Current priority: {priority}"
)

# Overall readiness explanation

if available_streams == 3 and rotation_ready and simulation_ready:
    st.success(
        "All three environmental data streams are available, "
        "and farm-planning outputs have been generated."
    )

elif available_streams > 0:
    st.warning(
        "AgriOrbit has partial environmental data or "
        "farm-planning outputs. Complete the remaining steps "
        "to improve dashboard readiness."
    )

else:
    st.info(
        "Retrieve environmental data and generate farm-planning "
        "outputs to complete the scorecard."
    )

st.caption(
    "This scorecard tracks data availability and workflow progress. "
    "It is not a scientific farm-health score or a validated "
    "measure of agricultural adaptation."
)

# ==========================================
# AGRIORBIT FARMER ACTION PLAN
# ==========================================

st.divider()

st.header("🧑‍🌾 Farmer Adaptation Action Plan")

st.write(
    "Convert the selected crop rotation strategy "
    "into practical next steps for farm planning."
)

if rotation_ready:

    # Select the highest-ranked existing rotation
    best_rotation = st.session_state["rotation_results"][0]

    st.subheader("🌱 Selected Crop Rotation")

    st.success(
        f"Top-ranked strategy: {best_rotation['Rotation']}"
    )

    st.write(
        f"**Three-year crop sequence:** "
        f"{best_rotation['Sequence']}"
    )

    st.metric(
        "Comparative Screening Score",
        f"{best_rotation['Score']}/100"
    )

    # Action suggestions based on farmer priority
    priority_actions = {

        "Water Conservation": [
            "Review the farm's irrigation schedule and identify opportunities to reduce unnecessary water use.",
            "Discuss soil-cover and mulching practices suitable for the local crops and soil.",
            "Monitor available soil-wetness indicators alongside actual field conditions.",
            "Verify the water requirements of each proposed crop before planting."
        ],

        "Soil Health Improvement": [
            "Arrange a soil test to verify pH, organic carbon and available nutrients.",
            "Review residue management and soil-cover practices with a local agronomist.",
            "Evaluate the role of the legume crop in the proposed sequence.",
            "Track soil test results over time to assess changes in soil condition."
        ],

        "Climate Resilience": [
            "Compare the proposed crops with locally observed temperature and rainfall patterns.",
            "Review suitable sowing windows with local agricultural extension services.",
            "Evaluate drought and heat risks before selecting crop varieties.",
            "Keep a record of seasonal rainfall, temperature and crop performance."
        ],

        "Balanced Sustainability": [
            "Review water requirements and soil suitability for every crop in the sequence.",
            "Arrange soil testing and monitor changes in soil condition.",
            "Evaluate crop diversity and the role of legumes in the rotation.",
            "Compare the proposed sequence with local growing seasons and market conditions."
        ]
    }

    action_items = priority_actions[priority]

    st.subheader("📋 Recommended Next Steps")

    for index, action in enumerate(action_items, start=1):
        st.markdown(f"**{index}.** {action}")

    # Data-based follow-up actions
    st.subheader("🛰️ Environmental Monitoring")

    if climate_ready:
        st.write("✅ NASA POWER climate data is available for this location.")
    else:
        st.write("⬜ Retrieve NASA POWER climate data for this location.")

    if wetness_ready:
        st.write("✅ NASA POWER soil-wetness indicators are available.")
    else:
        st.write("⬜ Retrieve NASA POWER soil-wetness indicators.")

    if ndvi_ready:
        st.write("✅ MODIS vegetation observations are available.")
    else:
        st.write("⬜ Retrieve MODIS NDVI observations when the service is available.")

    # Build downloadable action plan
    action_report = [
        "AGRIORBIT FARMER ADAPTATION ACTION PLAN",
        "=" * 45,
        "",
        f"Farm coordinates: {current_location[0]}, {current_location[1]}",
        f"Farmer priority: {priority}",
        f"Selected strategy: {best_rotation['Rotation']}",
        f"Crop sequence: {best_rotation['Sequence']}",
        f"Comparative screening score: {best_rotation['Score']}/100",
        "",
        "RECOMMENDED NEXT STEPS",
        "-" * 30
    ]

    for index, action in enumerate(action_items, start=1):
        action_report.append(f"{index}. {action}")

    action_report.extend([
        "",
        "ENVIRONMENTAL DATA STATUS",
        "-" * 30,
        f"Climate data: {'Available' if climate_ready else 'Needs retrieval'}",
        f"Soil wetness: {'Available' if wetness_ready else 'Needs retrieval'}",
        f"MODIS NDVI: {'Available' if ndvi_ready else 'Needs retrieval'}",
        "",
        "IMPORTANT VALIDATION NOTES",
        "-" * 30,
        "This action plan is an experimental planning aid.",
        "Crop rotation scores are rule-based screening scores,",
        "not validated yield or profitability predictions.",
        "Verify crop suitability, sowing dates, water requirements,",
        "soil conditions and local regulations with qualified",
        "agricultural experts before making farm decisions.",
        "",
        "Prepared by Siddhi Services | AgriOrbit"
    ])

    st.download_button(
        "⬇️ Download Farmer Action Plan",
        data="\n".join(action_report),
        file_name="AgriOrbit_Farmer_Action_Plan.txt",
        mime="text/plain"
    )

else:
    st.warning(
        "Generate a current-location crop rotation plan first "
        "to create your Farmer Action Plan."
    )

st.caption(
    "The action plan uses the existing prototype rotation ranking. "
    "It is intended to support discussion and planning, not replace "
    "local agronomic advice."
)


# ==========================================
# 6. DATA SOURCE
# ==========================================

st.divider()

st.header("📡 NASA Earth Observation Data Sources")

st.markdown("""
AgriOrbit uses NASA Earth observation and
environmental datasets to explore climate conditions,
soil wetness and vegetation greenness.
""")

# ------------------------------------------
# 1. NASA POWER - CLIMATE DATA
# ------------------------------------------

st.subheader("1. NASA POWER – Climate Data")

st.markdown("""
**Prediction Of Worldwide Energy Resources (POWER)**

- **T2M:** Daily mean air temperature at 2 metres.
- **PRECTOTCORR:** Corrected daily precipitation.
- **Community:** Agroclimatology.
- **Data type:** Gridded meteorological data.

These variables help assess temperature and
precipitation conditions at the selected farm location.
""")

st.markdown(
    "[NASA POWER Official Portal](https://power.larc.nasa.gov/)"
)

# ------------------------------------------
# 2. NASA POWER - SOIL WETNESS
# ------------------------------------------

st.subheader("2. NASA POWER – Soil Wetness Indicators")

st.markdown("""
AgriOrbit also uses NASA POWER soil-wetness
indicators to explore modeled water availability
conditions in different soil layers.

- **GWETTOP:** Surface soil wetness.
- **GWETROOT:** Root-zone soil wetness.
- **GWETPROF:** Soil wetness across the soil profile.
- **Community:** As configured in the application API request.
- **Data type:** Model-derived environmental indicators.

These indicators provide an approximate picture
of soil wetness. They are not direct field soil
moisture measurements or soil laboratory results.
They should not be interpreted as direct SMAP
Level-4 observations.
""")

st.markdown(
    "[NASA POWER Documentation](https://power.larc.nasa.gov/docs/)"
)

# ------------------------------------------
# 3. NASA MODIS - VEGETATION INDEX
# ------------------------------------------

st.subheader("3. NASA MODIS – Vegetation Monitoring")

st.markdown("""
**MODIS MOD13Q1 – Vegetation Indices**

AgriOrbit uses the MODIS vegetation index dataset
to explore vegetation greenness around the selected
farm location.

- **NDVI:** Normalized Difference Vegetation Index.
- **Product:** MOD13Q1.
- **Spatial resolution:** 250 metres.
- **Temporal resolution:** 16-day composite.
- **Data type:** Satellite-derived vegetation index.

NDVI helps observe vegetation greenness and
changes over time. It is not a direct measurement
of crop yield or a definitive crop-health diagnosis.

Data retrieval depends on the availability of the
external MODIS data service.
""")

st.markdown(
    "[NASA MODIS MOD13Q1 Product Information]"
    "(https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/MOD13Q1/)"
)

# ------------------------------------------
# DATA INTERPRETATION AND LIMITATIONS
# ------------------------------------------

st.subheader("🔍 Data Interpretation and Limitations")

st.info("""
AgriOrbit is a farm adaptation decision-support
prototype.

NASA POWER climate and soil-wetness variables
are gridded or model-derived indicators.
MODIS NDVI represents satellite-observed vegetation
greenness.

Crop rotation scores and climate scenario results
are illustrative decision-support estimates, not
validated agronomic predictions.

Local field measurements and expert agronomic
advice are recommended before making farm
management decisions.
""")

st.divider()

st.caption(
    "AgriOrbit | Developed by Siddhi Services | "
    "NASA Space Apps Challenge 2026"
)