import streamlit as st

from components.ui import card
from utils.state import init_state
from utils.style import apply_theme


st.set_page_config(page_title="About | CyberShieldSim", layout="wide")
init_state()
apply_theme()

st.title("About CyberShieldSim")
st.markdown(
    '<p class="hero-text">Cybersecurity Learning & Analysis Platform with practical authentication, encryption, signatures, and key exchange demos.</p>',
    unsafe_allow_html=True,
)

with card("Module Overview"):
    st.markdown(
        """
        - **Dashboard (`app.py`)**: live metrics and navigation entry
        - **Attack Simulation Lab (`pages/simulator.py`)**: weak encryption, MITM, DH secure-vs-insecure
        - **Secure System (`pages/secure_system.py`)**: bcrypt auth, RBAC, AES(Fernet) file/text encryption
        - **Security Tools (`pages/tools.py`)**: RSA signatures, hash generator, password analyzer
        - **Logs (`pages/logs.py`)**: action history in memory
        """
    )

with card("Working"):
    st.markdown(
        """
        - Work 1: Attack lab scenarios and learning flow
        - Work 2: Secure system authentication, RBAC, encryption workflows
        - Work 3: Security tools, dashboard, logging, and documentation
        """
    )
