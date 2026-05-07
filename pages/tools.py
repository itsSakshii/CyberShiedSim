import base64
import time

import streamlit as st

from components.ui import card
from utils.auth import password_strength
from utils.crypto import md5_hash, sha256_hash
from utils.signatures import generate_rsa_keys
from utils.signatures import sign_message, verify_signature
from utils.state import add_log, init_state
from utils.style import apply_theme


def loader() -> None:
    with st.spinner("Processing..."):
        time.sleep(0.3)


st.set_page_config(page_title="Security Tools | CyberShieldSim", layout="wide")
init_state()
apply_theme()

st.title("Security Tools")
st.markdown(
    '<p class="hero-text">Hands-on cryptography and validation tools with beginner-friendly flow.</p>',
    unsafe_allow_html=True,
)

tabs = st.tabs(["RSA Signature Tool", "Hash Generator", "Password Analyzer"])

with tabs[0]:
    with card("Digital Signature (RSA)"):
        st.info("What is happening: Message is signed with private key and verified with public key.")
        if st.button("Generate New RSA Keys"):
            loader()
            private_pem, public_pem = generate_rsa_keys()
            st.session_state.rsa_private_pem = private_pem
            st.session_state.rsa_public_pem = public_pem
            st.success("New key pair generated.")

        message = st.text_area("Message to sign", "Payment approved for order #552")
        tampered = st.text_area("Tampered message check", "Payment approved for order #552")

        c1, c2, c3 = st.columns(3)
        c1.write("Input")
        c1.code(message)
        c2.write("Processing")
        c2.code("RSA private key signs message")
        c3.write("Output")

        if st.button("Sign and Verify"):
            loader()
            signature = sign_message(message, st.session_state.rsa_private_pem)
            sig_b64 = base64.b64encode(signature).decode()
            valid_original = verify_signature(message, signature, st.session_state.rsa_public_pem)
            valid_tampered = verify_signature(tampered, signature, st.session_state.rsa_public_pem)

            c3.code(sig_b64[:220] + ("..." if len(sig_b64) > 220 else ""))
            if valid_original:
                st.success("Original message verification: VALID")
            else:
                st.error("Original message verification: FAILED")

            if not valid_tampered:
                st.warning("Tampered message verification: FAILED (expected)")
            else:
                st.error("Tampered message unexpectedly verified.")

            add_log("rsa_sign_verify", "RSA signature generated and verified", actor=st.session_state.current_user or "guest")

        st.markdown("#### Behind the scenes")
        st.write("Private key creates signature; public key validates authenticity and integrity.")
        st.markdown("#### Why it matters")
        st.success("Digital signatures prevent silent tampering and prove sender authenticity.")

with tabs[1]:
    with card("Hash Generator (SHA-256 + MD5)"):
        st.info("What is happening: Input text is converted to a fixed-length fingerprint.")
        text = st.text_area("Text to hash", "Cybersecurity is practical and important.")

        c1, c2, c3 = st.columns(3)
        c1.write("Input")
        c1.code(text)
        c2.write("Processing")
        c2.code("Apply SHA-256 and MD5")
        c3.write("Output")

        if st.button("Generate Hashes"):
            loader()
            sha_value = sha256_hash(text)
            md5_value = md5_hash(text)
            c3.code(f"SHA-256:\n{sha_value}\n\nMD5:\n{md5_value}")
            st.info("Hash meaning: a fingerprint used for integrity checks.")
            add_log("hash_generation", "Generated SHA-256 and MD5", actor=st.session_state.current_user or "guest")

        st.markdown("#### Behind the scenes")
        st.write("A tiny input change creates a very different hash output.")
        st.markdown("#### Why it matters")
        st.success("Hashes help detect data corruption and tampering.")

with tabs[2]:
    with card("Password Strength Analyzer"):
        st.info("What is happening: Password is evaluated live against common security rules.")
        password = st.text_input("Enter password", type="password")

        if password:
            label, score, tips = password_strength(password)
            display_label = "Medium" if label == "Moderate" else label
            c1, c2, c3 = st.columns(3)
            c1.write("Input")
            c1.code("*" * len(password))
            c2.write("Processing")
            c2.code("Length + uppercase + lowercase + number + symbol")
            c3.write("Output")
            c3.code(f"{display_label} ({score}/5)")

            if display_label == "Strong":
                st.success("Strong password.")
            elif display_label == "Medium":
                st.warning("Medium strength password.")
            else:
                st.error("Weak password.")

            if tips:
                st.info("How to improve:")
                for tip in tips:
                    st.write(f"- {tip}")
            add_log("password_analysis", f"Password analyzed: {display_label}", actor=st.session_state.current_user or "guest")

        st.markdown("#### Why it matters")
        st.success("Strong passwords reduce brute-force and credential attack risk.")
