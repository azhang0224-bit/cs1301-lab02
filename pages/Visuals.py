# This creates the page for displaying data visualizations.

import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Coffee Choices")
st.write("Hi! This page compares 10 popular coffee drinks by caffeine, calories, and price.")

DATA_PATH = Path(__file__).parent.parent / "data.json"
with open(DATA_PATH) as f:
    data = json.load(f)

df = pd.DataFrame(data)

#my extra credit code:
def show_metrics(values, prefix, label):
    mean_now = values.mean()
    median_now = values.median()

    for stat, now in [("mean", mean_now), ("median", median_now)]:
        last_key = prefix + "_last_" + stat
        prev_key = prefix + "_prev_" + stat
        if last_key not in st.session_state:
            st.session_state[last_key] = now
            st.session_state[prev_key] = now
        if now != st.session_state[last_key]:
            st.session_state[prev_key] = st.session_state[last_key]
            st.session_state[last_key] = now

    col1, col2 = st.columns(2)
    col1.metric("Mean of " + label, round(mean_now, 2),
                round(mean_now - st.session_state[prefix + "_prev_mean"], 2))
    col2.metric("Median of " + label, round(median_now, 2),
                round(median_now - st.session_state[prefix + "_prev_median"], 2))

#PART 1: GRAPHS FROM data.json
st.subheader("Caffeine in Each Drink")

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(df["drink"], df["caffeine_mg"])
ax.set_title("Caffeine Content by Coffee Drink")
ax.set_xlabel("Drink")
ax.set_ylabel("Caffeine (mg)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)


st.subheader("Explore the Data")

if "y_choice" not in st.session_state:
    st.session_state.y_choice = "calories"

st.radio("Choose what to compare with caffeine:", ["calories", "price"], key="y_choice")
show_metrics(df[st.session_state.y_choice], "p1", st.session_state.y_choice)
st.scatter_chart(df, x="caffeine_mg", y=st.session_state.y_choice)

#PART 2: from my survey result graphs
st.header("Survey Results")

SURVEY_PATH = Path(__file__).parent.parent / "data.csv"

if not (SURVEY_PATH.exists() and SURVEY_PATH.stat().st_size > 0):
    st.warning("No survey responses yet. Fill out the Survey page first.")
    st.stop()

survey_df = pd.read_csv(SURVEY_PATH)
survey_df["cups"] = pd.to_numeric(survey_df["cups"], errors="coerce")
survey_df["sleep"] = pd.to_numeric(survey_df["sleep"], errors="coerce")
survey_df = survey_df.dropna()

if survey_df.empty:
    st.warning("No valid survey responses yet.")
    st.stop()

# Static chart: pie chart (Matplotlib = advanced)
st.subheader("Favorite Coffee Drinks from Survey Responses")

drink_counts = survey_df["favorite"].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(drink_counts, labels=drink_counts.index, autopct="%1.0f%%")
ax2.set_title("Favorite Coffee Drink Among Survey Responses")
st.pyplot(fig2)

# Dynamic chart: histogram controlled by two widgets
st.subheader("Explore the Survey Responses")

if "survey_metric" not in st.session_state:
    st.session_state.survey_metric = "cups"
if "time_filter" not in st.session_state:
    st.session_state.time_filter = "All"

st.radio("Show the distribution of:", ["cups", "sleep"], key="survey_metric")
st.selectbox("Time of day:", ["All", "Morning", "Afternoon", "Evening"], key="time_filter")

shown = survey_df
if st.session_state.time_filter != "All":
    shown = survey_df[survey_df["time_of_day"] == st.session_state.time_filter]

if shown.empty:
    st.warning("No responses for that time of day yet.")
else:
    show_metrics(shown[st.session_state.survey_metric], "p2", st.session_state.survey_metric)
    fig3, ax3 = plt.subplots()
    ax3.hist(shown[st.session_state.survey_metric], bins=5)
    fig3, ax3 = plt.subplots()
    ax3.hist(shown[st.session_state.survey_metric], bins=5)
    ax3.set_title("Distribution of " + st.session_state.survey_metric)
    ax3.set_xlabel(st.session_state.survey_metric)
    ax3.set_ylabel("Number of responses")
    st.pyplot(fig3)
