
import re
import streamlit as st

from backend.auth.auth import register_user


st.title("User Registration")
st.header("Create an Account")

st.write(
    "Create an account to access the "
    "AI Response Validation System."
)

with st.form("registration_form"):

    username = st.text_input(
        "Username",
        placeholder="Choose a username"
    )

    email = st.text_input(
        "Email Address",
        placeholder="Enter your email address"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Create a password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter your password"
    )

    submitted = st.form_submit_button(
        "Create Account",
        use_container_width=True
    )

    if submitted:

        if not all([
            username.strip(),
            email.strip(),
            password,
            confirm_password
        ]):
            st.error("All fields are required.")

        elif not re.fullmatch(
            r"[A-Za-z0-9_]{3,30}",
            username.strip()
        ):
            st.error(
                "Username must be 3–30 characters and contain "
                "only letters, numbers, and underscores."
            )

        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email.strip()
        ):
            st.error("Please enter a valid email address.")

        elif len(password) < 8:
            st.error(
                "Password must contain at least 8 characters."
            )

        elif len(password.encode("utf-8")) > 72:
            st.error(
                "Password must not exceed 72 bytes."
            )

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:
            success, message = register_user(
                username.strip(),
                email.strip(),
                password
            )

            if success:
                st.success(message)
                st.info(
                    "You can now sign in using your email address."
                )
            else:
                st.error(message)
