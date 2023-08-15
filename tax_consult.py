import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, salaried, business_profession, senior_citizens, huf_tax # Include huf_tax

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
        "Senior Citizens", # Existing option
        "Hindu Undivided Family", # New option
    ],
    icons=[
        "house",
        "wallet",
        "briefcase",
        "building",
        "briefcase", # New icon (you can choose another suitable icon)
    ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Navigation
if selected == "Home":
    home.show()
elif selected == "Salaried":
    st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.')    
    salaried.show()
elif selected == "Business / Profession":
    st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.') 
    business_profession.show()
elif selected == "Senior Citizens": # Existing condition
    st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.') 
    senior_citizens.show()
elif selected == "Hindu Undivided Family": # New condition
    st.info('Note: Default values have been provided for all fields. Please update them according to your financial details.') 
    huf_tax.show() # Using the imported 'show' function from 'huf_tax' module

st.warning('Please note that this app is based on tax laws as of the 2023 fiscal year. Always consult with a tax professional to ensure compliance with the latest regulations.')