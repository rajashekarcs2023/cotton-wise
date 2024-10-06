import streamlit as st

st.set_page_config(page_title="CottonDrip: Smart Advisor for Maharashtra Cotton Farmers", page_icon="🌱", layout="wide")

st.title("🌱 CottonDrip: Smart Advisor for Maharashtra Cotton Farmers")
st.markdown("""
Welcome to CottonDrip! This tool provides personalized advice for cotton farmers in Maharashtra, 
helping you make informed decisions about irrigation, pest control, and more.

Use the sidebar to navigate between different features:
- **Farm Advice**: Get personalized recommendations based on your farm's data.
- **AI Chat**: Have a conversation with our AI advisor about any cotton farming topics.

Get started by selecting a page from the sidebar!
""")

st.sidebar.success("Select a page above.")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ for Maharashtra's cotton farmers. For support, contact support@cottondrip.com")