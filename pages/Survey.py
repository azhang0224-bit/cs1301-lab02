# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import csv
from pathlib import Path
import pandas as pd
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

#Data file path 
CSV_PATH = Path(__file__).parent.parent / "data.csv"

# PAGE TITLE AND USER DIRECTIONS
st.title("Coffee Survey")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    favorite = st.selectbox(
        "What is your favorite coffee drink?",
        ["Drip Coffee", "Americano", "Double Espresso", "Latte", "Cappuccino",
         "Flat White", "Mocha", "Cold Brew", "Caramel Macchiato", "Nitro Cold Brew"],
    )
    cups = st.text_input("How many cups of coffee do you drink per day? (a number)")
    sleep = st.text_input("How many hours did you sleep last night? (a number)")
    time_of_day = st.selectbox(
        "When do you usually drink coffee?",
        ["Morning", "Afternoon", "Evening"]
    )
  
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
if submitted:
    if cups == "" or sleep == "":
        st.warning("Please answer every question.")
    elif not (cups.replace(".", "", 1).isdigit() and sleep.replace(".", "", 1).isdigit()):
        st.warning("Cups and sleep hours must be numbers.")
    else:
        file_exists = CSV_PATH.exists() and CSV_PATH.stat().st_size > 0

        with open(CSV_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["favorite", "cups", "sleep", "time_of_day"])
            writer.writerow([favorite, cups, sleep, time_of_day])

        st.success("Thanks! Your answers were saved.")
        st.success("Your data has been submitted!")
        st.write(
            f"You entered: **Favorite drink:** {favorite}, "
            f"**Cups per day:** {cups}, "
            f"**Hours of sleep:** {sleep}, "
            f"**Time of day:** {time_of_day}"
        )
                 
# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")


# Check if the CSV file exists and is not empty before trying to read it.
if CSV_PATH.exists() and CSV_PATH.stat().st_size > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv(CSV_PATH)
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
