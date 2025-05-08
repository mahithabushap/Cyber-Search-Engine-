import streamlit as st
import pandas as pd
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Cyber Breach Search Engine", page_icon="🔍", layout="wide")

# Load the mock dataset using st.cache_data
@st.cache_data
def load_data():
    data = pd.read_csv('breach_data.csv')
    return data

# Load dataset
data = load_data()

# Page title and description
st.title("🔍 Cyber Breach Search Engine")
st.markdown("**A simple tool to check if your personal data was involved in any known data breaches.**")
st.write("Input your information below to see if it has been compromised.")

# Sidebar for Search Options
st.sidebar.header("🔍 Search Options")
search_type = st.sidebar.selectbox("Search by:", ["Email", "Name", "Breach Type"])
search_input = st.sidebar.text_input("Enter your search term")
sort_by_date = st.sidebar.checkbox("Sort by Date (Newest First)")

# Function to search data based on input
def search_data(search_type, search_input):
    if search_type == "Email":
        results = data[data['Email'].str.contains(search_input, case=False, na=False)]
    elif search_type == "Name":
        results = data[data['Name'].str.contains(search_input, case=False, na=False)]
    elif search_type == "Breach Type":
        results = data[data['Exposed Data'].str.contains(search_input, case=False, na=False)]
    if sort_by_date:
        results = results.sort_values(by="Date", ascending=False)
    return results

# Display search results when user clicks the search button
if st.sidebar.button("Search"):
    if search_input:
        results = search_data(search_type, search_input)
        if not results.empty:
            st.write(f"### Search Results for `{search_input}`")
            st.dataframe(results[['Breach Name', 'Date', 'Exposed Data', 'Source']], width=800)
            
            # Cybersecurity Recommendations based on the breach types in results
            st.markdown("### Cybersecurity Recommendations")
            if 'passwords' in results['Exposed Data'].values:
                st.warning("🔑 **Change Passwords**: Your passwords were exposed. Consider updating them.")
            if 'credit cards' in results['Exposed Data'].values:
                st.warning("💳 **Monitor Financial Activity**: Keep an eye on credit card statements for unusual activity.")
            if 'emails' in results['Exposed Data'].values:
                st.info("📧 **Beware of Phishing Emails**: Scammers may attempt to use your email in phishing schemes.")

            # Additional visual information
            st.markdown("---")
            st.markdown("For more information on each breach, visit the respective source sites or contact the organizations.")
        else:
            st.error("No data breaches found for the given search term.")
    else:
        st.info("Please enter a search term to start.")


st.sidebar.subheader("💡 Cybersecurity Tips")
st.sidebar.markdown(
   
)

# Footer
st.markdown("---")
st.markdown("🔒 **Stay Secure**: Protect your data and stay informed on cybersecurity practices.")
