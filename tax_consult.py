import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pages import home, salaried, business_profession

# Set the page config with a custom icon
st.set_page_config(page_title="TaxInsight", layout="wide", initial_sidebar_state="collapsed", page_icon="🔍")

# Remove the Streamlit generated page components on the sidebar
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# Horizontal menu
selected = option_menu(
    menu_title=None,
    options=[
        "Home",
        "Salaried",
        "Business / Profession",
        # ... (other menu options)
    ],
    icons=[
        "house",
        "briefcase",
        "briefcase",
        # ... (other menu icons)
    ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Navigation
if selected == "Home":
    home.show()  # Assuming you have defined this function in the 'home' subfile
elif selected == "Salaried":
    # Note for Users
    st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.')    
    salaried.show()  # Using the imported 'show_salaried' function from 'salaried' module
elif selected == "Business / Profession":
    # Note for Users
    st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.') 
    business_profession.show()  # Using the imported 'show_business_profession' function from 'business_profession' module

st.warning('Please note that this app is based on tax laws as of the 2023 fiscal year. Always consult with a tax professional to ensure compliance with the latest regulations.')
