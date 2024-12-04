import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Title and Description
st.title("Regional Commodity Prices")
st.markdown("Enter the details of the commodity below or upload an Excel file.")

# Upload your Excel file
st.markdown("### Upload Your Excel File")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

# Fetch and Display Data
if uploaded_file is not None:
    try:
        # Reading the uploaded Excel file
        df = pd.read_excel(uploaded_file)
        df = df.dropna(how="all")  # Remove empty rows
        st.markdown("### Existing Data")
        st.dataframe(df)  # Display the content of the Excel file
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
else:
    st.info("Please upload an Excel file to proceed.")

# Add input fields for manual data entry
st.markdown("### Add New Commodity Details")
personnel_id = st.text_input(label="Personnel_ID")
input_date = st.date_input(label="Input Date (DD-MM-YYYY)")
week = st.text_input(label="Week (week of the year)")
town = st.text_input(label="Town")
region = st.text_input(label="Region")
commodity_name = st.text_input("Commodity Name")
price = st.number_input("Price", min_value=0.0, step=0.1)
contact = st.text_input(label="Contact Person")

# Submit button for manual input
if st.button("Submit"):
    if commodity_name and price > 0:  # Check if the commodity name is entered and price is greater than 0
        try:
            # Convert input_date to string
            input_date_str = input_date.strftime('%Y-%m-%d')  # Format the date as a string (e.g., '2024-12-04')

            # Connect to Google Sheets using gspread
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            
            # Make sure to point to the correct location of your credentials file (either absolute or environment variable)
            creds_file = os.path.join(os.getcwd(), "entry-form-443710-adec8e1e100a.json")  # Path to your credentials file
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            gc = gspread.authorize(credentials)

            # Open the Google Sheet by URL (ensure this is the correct URL for your Google Sheet)
            spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/14t7C004jPf5boOdE3puHG3UJ4DzXInRmoJWmOlMXHis/edit")  # Correct URL
            worksheet = spreadsheet.sheet1  # Selecting the first sheet of the spreadsheet

            # Prepare the data row to be added
            new_row = [personnel_id, input_date_str, week, town, region, commodity_name, price, contact]
            worksheet.append_row(new_row)  # Append the row to the sheet

            # Feedback to the user
            st.success(f"Added {commodity_name} with price {price}.")
        except Exception as e:
            st.error(f"Error connecting to Google Sheets: {e}")
    else:
        st.warning("Please fill in all fields to submit.")



