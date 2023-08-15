import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pages import home, salaried, business_profession
from pages.home import show as show_home

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
        "store",
        # ... (other menu icons)
    ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Navigation
if selected == "Home":
    st.title("Welcome to Tax Consult")
    st.write("Explore tax-related information and tools using the navigation menu.")
    # Add more content to your home page as needed
elif selected == "Salaried":
    salaried.show()
elif selected == "Business / Profession":
    business_profession.show()

st.warning('Please note that this app is based on tax laws as of the 2023 fiscal year. Always consult with a tax professional to ensure compliance with the latest regulations.')
