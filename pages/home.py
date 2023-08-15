import streamlit as st

def show():
    # Sidebar content
    with st.sidebar.container():
        st.sidebar.title("🔍 TaxInsight")
        st.sidebar.markdown("**Your Comprehensive Tax Analysis Tool**")
        st.sidebar.markdown("---")
        
        st.sidebar.markdown("📖 **About**")
        st.sidebar.markdown("Designed for individuals and businesses alike. Stay updated with the latest tax rules and make informed financial decisions!")
        st.sidebar.markdown("---")

        st.sidebar.markdown("📬 **Contact Us**")
        st.sidebar.markdown("For any queries or support, leave a comment!")
        st.sidebar.markdown("---")

        st.sidebar.markdown("📚 **User Guide**")
        st.sidebar.markdown("Need help using TaxInsight? Check our Learning Manuals!")
        st.sidebar.markdown("---")

        st.sidebar.markdown("💬 **Feedback**")
        st.sidebar.markdown("We value your feedback! Share your thoughts through our Github!")
        st.sidebar.markdown("---")
        st.sidebar.markdown("_Explore TaxInsight and gain control over your financial decisions!_")

    # Main content
    st.title("TaxInsight: Your Comprehensive Tax Analysis Tool")
    st.write("Welcome to TaxInsight, your all-in-one solution for understanding and analyzing taxes. With a user-friendly interface and a variety of options, TaxInsight helps you navigate complex tax scenarios effortlessly. Whether you're a salaried employee, a business professional, or just curious about tax regulations, TaxInsight has the insights you need.")
    st.warning("Please note that while TaxInsight provides valuable insights, it's important to consult with a tax professional for specific advice.")