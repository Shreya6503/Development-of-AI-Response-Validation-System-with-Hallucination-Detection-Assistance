
import re
import streamlit as st

from backend.auth.auth import login_user


st.title("User Authentication")
st.header("Login")

st.write(
    "Sign in to access the AI Response Validation System."
)

with st.form("login_form"):

    email = st.text_input(
        "Email Address",
        placeholder="Enter your registered email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    submitted = st.form_submit_button(
        "Sign In",
        use_container_width=True
    )

    if submitted:

        if not email.strip() or not password:
            st.error(
                "Email address and password are required."
            )

        elif not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email.strip()
        ):
            st.error("Please enter a valid email address.")

        else:
            success, result = login_user(
                email.strip(),
                password
            )

            if success:
                st.session_state["authenticated"] = True
                st.session_state["user"] = result

                st.rerun()

            else:
                st.error(result)
