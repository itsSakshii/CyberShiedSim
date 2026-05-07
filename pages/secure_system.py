import time

import streamlit as st

from components.ui import card
from utils.auth import hash_password_bcrypt, password_strength, verify_password_bcrypt
from utils.crypto import decrypt_bytes_fernet, decrypt_text_fernet, encrypt_bytes_fernet, encrypt_text_fernet
from utils.state import add_log, bump_login_attempts, init_state
from utils.style import apply_theme


def loader() -> None:
    with st.spinner("Processing..."):
        time.sleep(0.3)


st.set_page_config(page_title="Secure System | CyberShieldSim", layout="wide")
init_state()
apply_theme()

st.title("Secure System")
st.markdown(
    '<p class="hero-text">Practical authentication, role-based access, and AES-based encryption workflow.</p>',
    unsafe_allow_html=True,
)

tabs = st.tabs(["Registration", "Login", "RBAC", "File/Text Encryption"])

with tabs[0]:
    with card("Registration with bcrypt + salt"):
        st.info("What is happening: User password is hashed with bcrypt before storage.")
        user = st.text_input("Username", key="new_user")
        pwd = st.text_input("Password", type="password", key="new_pwd")
        role = st.selectbox("Role", ["user", "admin"], key="new_role")

        if pwd:
            hashed_preview = hash_password_bcrypt(pwd)
            c1, c2, c3 = st.columns(3)
            c1.write("Input")
            c1.code(pwd)
            c2.write("Processing")
            c2.code("bcrypt + random salt")
            c3.write("Output")
            c3.code(hashed_preview[:60] + "...")

        if st.button("Register"):
            loader()
            if not user or not pwd:
                st.error("Username and password are required.")
            elif user in st.session_state.users_db:
                st.warning("User already exists.")
            else:
                st.session_state.users_db[user] = {
                    "password_hash": hash_password_bcrypt(pwd),
                    "role": role,
                }
                add_log("register", f"User registered: {user} ({role})", actor="system")
                st.success("User created with hashed password.")

        st.markdown("#### Behind the scenes")
        st.write("bcrypt automatically adds salt and stores only hashed output.")
        st.markdown("#### Why it matters")
        st.success("If database leaks, plain passwords are not exposed.")

with tabs[1]:
    with card("Login with bcrypt verification"):
        st.info("What is happening: Entered password is verified against stored bcrypt hash.")
        username = st.text_input("Login username", key="login_user")
        password = st.text_input("Login password", type="password", key="login_pwd")
        st.write("Behind the scenes: Input password -> bcrypt verify -> allow/deny")

        if st.button("Login"):
            loader()
            bump_login_attempts()
            add_log("login_attempt", f"Login attempt for {username or 'unknown'}")
            record = st.session_state.users_db.get(username)
            if record and verify_password_bcrypt(password, record["password_hash"]):
                st.session_state.current_user = username
                add_log("login_success", f"Logged in: {username}", actor=username)
                st.success("Authentication successful.")
            else:
                st.error("Authentication failed.")

        current = st.session_state.current_user
        if current:
            st.success(f"Logged in as {current} ({st.session_state.users_db[current]['role']})")
            if st.button("Logout"):
                add_log("logout", f"Logged out: {current}", actor=current)
                st.session_state.current_user = None
                st.info("Logged out.")

        st.markdown("#### Why it matters")
        st.success("Only valid users are authenticated; password is never stored in plain text.")

with tabs[2]:
    with card("Role-Based Access Control"):
        st.info("What is happening: System allows or denies actions based on selected role.")
        selected_role = st.selectbox("Select role to test", ["user", "admin"], key="rbac_select_role")
        current = st.session_state.current_user
        c1, c2, c3 = st.columns(3)
        c1.write("Input")
        c1.code(f"user={current or 'guest'}\nrole={selected_role}")
        c2.write("Processing")
        c2.code("Check allowed actions by role")
        c3.write("Output")
        if selected_role == "admin":
            c3.success("Admin actions allowed")
            if st.button("Admin action: Audit users"):
                add_log("admin_action", "User audit executed", actor=current or "guest")
                st.success("Admin action completed.")
        else:
            c3.error("Admin actions blocked")
            st.warning("Normal user can only perform basic actions.")
        st.markdown("#### Why it matters")
        st.success("RBAC limits privilege misuse and supports least privilege.")

with tabs[3]:
    with card("AES-based File/Text Encryption (Fernet)"):
        st.info("What is happening: Text/file is encrypted with Fernet (AES-based) using a secure key.")
        key = st.session_state.fernet_key

        plaintext = st.text_area("Text input", "Confidential report for team")
        uploaded = st.file_uploader("Or upload file", type=["txt", "csv", "json", "md"], key="secure_upload")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Encrypt Text"):
                loader()
                cipher = encrypt_text_fernet(plaintext, key)
                st.session_state.encrypted_text = cipher
                add_log("encrypt_text", "Text encrypted with Fernet", actor=st.session_state.current_user or "guest")
                st.code(cipher[:220] + ("..." if len(cipher) > 220 else ""))
                st.success("Encrypted output is unreadable without key.")

            if uploaded is not None and st.button("Encrypt File"):
                loader()
                encrypted_bytes = encrypt_bytes_fernet(uploaded.getvalue(), key)
                add_log("encrypt_file", f"File encrypted: {uploaded.name}", actor=st.session_state.current_user or "guest")
                st.download_button(
                    "Download Encrypted File",
                    data=encrypted_bytes,
                    file_name=f"{uploaded.name}.encrypted",
                    mime="application/octet-stream",
                )
                st.success("File encrypted and ready to download.")

        with c2:
            encrypted_text = st.text_area("Encrypted text input", st.session_state.encrypted_text, key="enc_text_input")
            if st.button("Decrypt Text"):
                loader()
                try:
                    plain = decrypt_text_fernet(encrypted_text, key)
                    add_log("decrypt_text", "Text decrypted with Fernet", actor=st.session_state.current_user or "guest")
                    st.code(plain)
                    st.success("Decryption successful.")
                except Exception:
                    st.error("Decryption failed. Invalid token or key.")

            encrypted_upload = st.file_uploader("Upload encrypted file", key="enc_file_upload")
            if encrypted_upload is not None and st.button("Decrypt File"):
                loader()
                try:
                    plain_bytes = decrypt_bytes_fernet(encrypted_upload.getvalue(), key)
                    add_log("decrypt_file", f"File decrypted: {encrypted_upload.name}", actor=st.session_state.current_user or "guest")
                    st.download_button(
                        "Download Decrypted File",
                        data=plain_bytes,
                        file_name=encrypted_upload.name.replace(".encrypted", ".decrypted"),
                        mime="application/octet-stream",
                    )
                    st.success("File decrypted successfully.")
                except Exception:
                    st.error("File decryption failed.")

        st.markdown("#### Password Strength Checker (Interactive)")
        st.info("Enter any password below to see live strength and improvement tips.")
        password_input = st.text_input(
            "Try a password",
            type="password",
            key="live_password_strength",
            placeholder="Type password to analyze...",
        )
        if password_input:
            strength_label, score, tips = password_strength(password_input)
            display_label = "Medium" if strength_label == "Moderate" else strength_label

            p1, p2, p3 = st.columns(3)
            p1.write("Input")
            p1.code("*" * len(password_input))
            p2.write("Processing")
            p2.code("Length + uppercase + lowercase + number + symbol")
            p3.write("Output")
            p3.code(f"{display_label} ({score}/5)")

            if display_label == "Strong":
                st.success("Strong password.")
            elif display_label == "Medium":
                st.warning("Medium strength password.")
            else:
                st.error("Weak password.")

            if tips:
                st.info("Suggestions to improve:")
                for tip in tips:
                    st.write(f"- {tip}")
            else:
                st.success("Great! This password already meets all basic checks.")
        st.write(f"Key in use (preview): {key.decode()[:18]}...")
        st.markdown("#### Why it matters")
        st.success("Fernet uses strong symmetric cryptography for data confidentiality.")
