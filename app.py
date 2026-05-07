import streamlit as st

from components.ui import card
from utils.state import init_state
from utils.style import apply_theme


st.set_page_config(page_title="SecureSphere", layout="wide")
init_state()
apply_theme()

st.title("SecureSphere - Interactive Cybersecurity Learning & Analysis Platform")
st.markdown(
    '<p class="hero-text">Dashboard for practical cybersecurity learning modules: attack simulation, secure system, cryptographic tools, and logs.</p>',
    unsafe_allow_html=True,
)

stats = st.session_state.stats
col1, col2, col3 = st.columns(3)
col1.metric("Simulations Run", stats["simulations_run"])
col2.metric("Login Attempts", stats["login_attempts"])
col3.metric("Security Score", f'{stats["security_score"]}/100')

with card("Platform Trend Snapshot"):
    st.bar_chart(
        {
            "Simulations": [stats["simulations_run"]],
            "Login Attempts": [stats["login_attempts"]],
            "Security Score": [stats["security_score"]],
        }
    )

with card("How to Use"):
    st.info("Use the sidebar to navigate modules in sequence for a full learning flow.")
    st.markdown(
        """
        - Open **simulator** to see insecure vs secure behavior
        - Open **secure_system** to try bcrypt login, role control, and AES (Fernet) encryption
        - Open **tools** for RSA signatures, hashes, and password checks
        - Open **logs** to inspect recorded user actions
        - Open **about** for architecture and team split
        """
    )
    st.success("Tip: Read each section top-to-bottom. Every module follows a learning flow.")

st.caption("Built for academic evaluation with modular design for a 3-member team.")