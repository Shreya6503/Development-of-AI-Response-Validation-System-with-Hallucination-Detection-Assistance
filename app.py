
import streamlit as st

st.set_page_config(
    page_title="AI Response Validation System",
    page_icon="🔍",
    layout="wide"
)

# Main application page
def home():
    st.title("AI Response Validation System")
    st.subheader("With Hallucination Detection Assistance")

    st.write(
        "Welcome! This application will help evaluate AI-generated "
        "responses for factual accuracy, relevance, and hallucinations."
    )

    st.info("Please login or register to continue.")

# Navigation pages
pg = st.navigation([
    st.Page(home, title="Home", icon="🏠", default=True),
    st.Page("pages/login.py", title="Login", icon="🔐"),
    st.Page("pages/register.py", title="Register", icon="📝"),
])

pg.run()
