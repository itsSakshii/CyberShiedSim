# SecureSphere - Interactive Cybersecurity Learning & Analysis Platform

SecureSphere is a multi-page Streamlit project for academic cybersecurity learning.
It combines attack simulations, secure system controls, practical tools, dashboard analytics,
and in-memory activity logs.

## Project Structure

```text
info project/
├── app.py
├── requirements.txt
├── pages/
│   ├── simulator.py
│   ├── secure_system.py
│   ├── tools.py
│   ├── logs.py
│   └── about.py
└── utils/
    ├── auth.py
    ├── crypto.py
    ├── signatures.py
    ├── key_exchange.py
    ├── state.py
    └── style.py
```

## Features

- Dashboard with simulation count, login attempts, security score, and charts
- Attack Simulation Lab with existing and new scenarios
- Secure System with bcrypt registration/login, RBAC, and Fernet (AES-based) encryption
- Security Tools with RSA signature verification, SHA-256/MD5 hash generator, and password analyzer
- Diffie-Hellman key exchange simulation in Attack Lab for secure-vs-insecure communication
- Activity logs stored in memory and shown in table format
- Soft pastel UI with modern cards, tabs, columns, and spinner animations

## Suggested Team Contribution Split

- Developer 1: Attack Simulation Lab scenarios and explanations
- Developer 2: Secure System (auth, RBAC, file handling and protection demo)
- Developer 3: Dashboard, Security Tools, Activity Logs, and UI consistency

## Run Locally

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Start the app:
   - `streamlit run app.py`

## Notes

- This project uses in-memory storage (`st.session_state`) for simplicity.
- Uses real cryptographic libraries (`bcrypt`, `cryptography`) while remaining educational and simple.
