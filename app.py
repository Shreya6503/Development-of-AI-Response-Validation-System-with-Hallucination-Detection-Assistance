
import streamlit as st


st.set_page_config(
    page_title="AI Response Validation System",
    layout="wide"
)


def home():
    st.title("AI Response Validation System")
    st.subheader("With Hallucination Detection Assistance")

    if st.session_state.get("authenticated", False):
        user = st.session_state.get("user", {})

        st.success(
            f"Welcome, {user.get('username', 'User')}!"
        )

        st.write(
            "You are successfully authenticated. "
            "Open the Dashboard to continue."
        )
    else:
        st.write(
            "Welcome! This application evaluates AI-generated "
            "responses for factual accuracy, relevance, "
            "and potential hallucinations."
        )

        st.info("Please log in or register to continue.")


def dashboard():
    # Protect the dashboard from unauthenticated access.
    if not st.session_state.get("authenticated", False):
        st.error("Please log in to access the dashboard.")
        st.stop()

    user = st.session_state.get("user", {})

    st.title("User Dashboard")

    st.write(
        f"Welcome, {user.get('username', 'User')}!"
    )

    st.write(
        "Your account is authenticated."
    )

    st.subheader("AI Response Validation System")

    st.info(
        "The dashboard is ready. AI response evaluation "
        "functionality will be integrated in a later step."
    )

    st.divider()

    if st.button("Logout"):
        st.session_state.pop("authenticated", None)
        st.session_state.pop("user", None)

        st.rerun()


# Configure application navigation.
authenticated = st.session_state.get("authenticated", False)

if authenticated:
    pages = [
        st.Page(home, title="Home"),
        st.Page(dashboard, title="Dashboard", default=True),
    ]
else:
    pages = [
        st.Page(home, title="Home", default=True),
        st.Page("pages/login.py", title="Login"),
        st.Page("pages/register.py", title="Register"),
    ]

navigation = st.navigation(pages)
navigation.run()
