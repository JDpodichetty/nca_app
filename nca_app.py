import streamlit as st
import pandas as pd
import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt

# Function to calculate AUC using trapezoidal rule
def calculate_auc(time, concentration):
    return simps(concentration, time)

# Function to calculate Cmax and Tmax
def calculate_cmax_tmax(time, concentration):
    cmax = np.max(concentration)
    tmax = time[np.argmax(concentration)]
    return cmax, tmax

# Streamlit app title
st.title("Non-Compartmental Analysis (NCA) for Pharmacokinetic Data")

# Upload CSV data file
st.header("Upload Pharmacokinetic Data (CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    # Load the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Display the dataframe
    st.write("### Uploaded Pharmacokinetic Data:")
    st.write(df.head())

    # Select columns for time and concentration
    st.subheader("Select columns for Time and Concentration")
    time_column = st.selectbox("Select Time Column", df.columns)
    concentration_column = st.selectbox("Select Concentration Column", df.columns)

    # Check if the necessary columns are selected
    if time_column and concentration_column:
        # Extract the time and concentration data
        time = df[time_column].values
        concentration = df[concentration_column].values

        # Calculate pharmacokinetic parameters
        auc = calculate_auc(time, concentration)
        cmax, tmax = calculate_cmax_tmax(time, concentration)

        # Display the results
        st.write(f"### Pharmacokinetic Parameters:")
        st.write(f"**AUC (Area Under the Curve):** {auc:.2f}")
        st.write(f"**Cmax (Maximum Concentration):** {cmax:.2f}")
        st.write(f"**Tmax (Time to Cmax):** {tmax:.2f}")

        # Plot the concentration vs time curve
        st.write("### Concentration-Time Plot")
        fig, ax = plt.subplots()
        ax.plot(time, concentration, marker='o', linestyle='-', color='b')
        ax.set_xlabel("Time")
        ax.set_ylabel("Concentration")
        ax.set_title("Concentration vs Time")
        st.pyplot(fig)

        # Display calculated AUC using trapezoidal rule as a plot area
        auc_trapz = calculate_auc(time, concentration)
        st.write(f"### AUC Calculated using Trapezoidal Rule: {auc_trapz:.2f}")
        auc_fig, auc_ax = plt.subplots()
        auc_ax.fill_between(time, concentration, color="skyblue", alpha=0.4)
        auc_ax.plot(time, concentration, color="Slateblue", alpha=0.6, linewidth=2)
        auc_ax.set_xlabel("Time")
        auc_ax.set_ylabel("Concentration")
        auc_ax.set_title("AUC - Concentration-Time Curve")
        st.pyplot(auc_fig)

