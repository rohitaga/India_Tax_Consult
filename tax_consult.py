import streamlit as st
from streamlit_option_menu import option_menu
from pages import home, salaried, business_profession, senior_citizens

# Set the page config with a custom icon
st.set_page_config(page_title="TaxInsight", layout="wide", initial_sidebar_state="expanded", page_icon="🔍")

st.sidebar.image('taxinsight_option_1.png', use_column_width="always", caption='TaxInsight')

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
        "Business",
        "Senior Citizens", # Existing option
    ],
    icons=[
        "house",
        "wallet",
        "briefcase",
        "building",
    ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Navigation
if selected == "Home":
    home.show()
elif selected == "Salaried":
    st.info('Note: You can switch between the Tax Calculator and Learning Manual sections using the sidebar navigation on the left.')    
    salaried.show()
elif selected == "Business":
    st.info('Note: You can switch between the Tax Calculator and Learning Manual sections using the sidebar navigation on the left.')    
    business_profession.show()
elif selected == "Senior Citizens": # Existing condition
    st.info('Note: You can switch between the Tax Calculator and Learning Manual sections using the sidebar navigation on the left.')    
    senior_citizens.show()

st.warning('Please note that this app is based on tax laws as of the 2023 fiscal year. Always consult with a tax professional to ensure compliance with the latest regulations.')