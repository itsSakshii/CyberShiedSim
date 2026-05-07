import base64
import hashlib
import time

import streamlit as st
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from components.ui import card
from utils.crypto import caesar_encrypt, encrypt_text_fernet, generate_fernet_key
from utils.state import add_log, bump_simulations, init_state
from utils.style import apply_theme


def vigenere_encrypt(text: str, keyword: str) -> str:
    if not keyword:
        return text
    keyword = "".join(ch.upper() for ch in keyword if ch.isalpha())
    if not keyword:
        return text

    result = []
    k_idx = 0
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            shift = ord(keyword[k_idx % len(keyword)]) - ord("A")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            k_idx += 1
        else:
            result.append(ch)
    return "".join(result)


def aes_encrypt(text: str, key: bytes) -> str:
    return encrypt_text_fernet(text, key)


def rsa_encrypt(text: str, public_key) -> bytes:
    return public_key.encrypt(
        text.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(ciphertext: bytes, private_key) -> str:
    plain = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return plain.decode(errors="ignore")


def generate_hash(text: str) -> tuple[str, str]:
    return hashlib.sha256(text.encode()).hexdigest(), hashlib.md5(text.encode()).hexdigest()


def run_steps(messages: list[tuple[str, str]], delay: float = 0.6) -> None:
    progress = st.progress(0)
    status = st.empty()
    total = len(messages)
    for i, (kind, msg) in enumerate(messages, start=1):
        progress.progress(int(i * 100 / total))
        if kind == "warning":
            status.warning(msg)
        elif kind == "error":
            status.error(msg)
        elif kind == "success":
            status.success(msg)
        else:
            status.info(msg)
        time.sleep(delay)
    progress.progress(100)


def render_learning_text(what: str, behind: str, why: str) -> None:
    st.info(f"What is happening: {what}")
    st.write(f"Behind the scenes: {behind}")
    st.success(f"Why it matters: {why}")


st.set_page_config(page_title="Simulator | CyberShieldSim", layout="wide")
init_state()
apply_theme()

if "sim_fernet_key" not in st.session_state:
    st.session_state.sim_fernet_key = generate_fernet_key()

if "sim_rsa_private" not in st.session_state or "sim_rsa_public" not in st.session_state:
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    st.session_state.sim_rsa_private = private
    st.session_state.sim_rsa_public = private.public_key()

st.title("Attack Simulation Lab")
st.markdown(
    '<p class="hero-text">Interactive cryptography playground with algorithm-level simulation and attack awareness.</p>',
    unsafe_allow_html=True,
)

algo = st.selectbox(
    "Choose algorithm simulation",
    [
        "Caesar Cipher",
        "Vigenere Cipher",
        "AES (Fernet)",
        "RSA Encryption/Decryption",
        "Hashing (SHA-256 vs MD5)",
        "Base64 Encoding",
        "Compare Algorithms",
    ],
)

if algo == "Caesar Cipher":
    with card("Input Card"):
        text = st.text_input("Input text", "HELLO")
        shift = st.slider("Shift value", 1, 25, 3)

    with card("Processing Card"):
        st.markdown("Flow: Input -> Caesar Shift -> Cipher Text")
        if st.button("Start Simulation", key="caesar_start"):
            run_steps(
                [
                    ("info", "Encrypting input text."),
                    ("info", "Applying Caesar shift."),
                    ("warning", "Trying brute-force attack on small key space."),
                ]
            )
            bump_simulations()
            add_log("simulation_run", "Caesar Cipher", actor=st.session_state.current_user or "guest")
            encrypted = caesar_encrypt(text, shift)
            st.session_state.caesar_output = encrypted

    with card("Output Card"):
        encrypted = st.session_state.get("caesar_output", "")
        if encrypted:
            st.code(f"Input: {text}\nProcess: Caesar shift +{shift}\nOutput: {encrypted}")
            brute = "\n".join([f"k={k}: {caesar_encrypt(encrypted, -k)}" for k in range(1, 8)])
            st.code(f"Brute-force preview:\n{brute}")

    with card("Attack Explanation Card"):
        render_learning_text(
            "Caesar shifts each letter by a fixed number.",
            "It uses one small numeric key for all letters.",
            "Small key space makes brute-force attacks easy.",
        )
        st.warning("Weakness: Small key space.")
        st.warning("Attack type: Brute-force.")

elif algo == "Vigenere Cipher":
    with card("Input Card"):
        text = st.text_input("Input text", "HELLO WORLD", key="vig_text")
        keyword = st.text_input("Keyword", "KEY", key="vig_key")

    with card("Processing Card"):
        st.markdown("Flow: Input -> Vigenere keyword shifts -> Cipher Text")
        if st.button("Start Simulation", key="vig_start"):
            run_steps(
                [
                    ("info", "Normalizing keyword."),
                    ("info", "Applying per-character shifting."),
                    ("success", "Generating Vigenere output."),
                ]
            )
            bump_simulations()
            add_log("simulation_run", "Vigenere Cipher", actor=st.session_state.current_user or "guest")
            st.session_state.vig_output = vigenere_encrypt(text, keyword)

    with card("Output Card"):
        output = st.session_state.get("vig_output", "")
        if output:
            st.code(f"Input: {text}\nProcess: Vigenere key '{keyword}'\nOutput: {output}")

    with card("Attack Explanation Card"):
        render_learning_text(
            "Vigenere uses a keyword to vary letter shifts.",
            "Each character may be shifted by a different amount.",
            "It is stronger than Caesar but still breakable with enough known text.",
        )
        st.warning("Weakness: Repeated keyword patterns can leak structure.")
        st.warning("Attack type: Frequency/Kasiski analysis.")

elif algo == "AES (Fernet)":
    with card("Input Card"):
        text = st.text_area("Input text", "Confidential note for secure channel", key="aes_text")
        if st.button("Generate Key", key="aes_key"):
            st.session_state.sim_fernet_key = generate_fernet_key()
            st.success("New Fernet key generated.")
        st.code(f"Current key (preview): {st.session_state.sim_fernet_key.decode()[:24]}...")

    with card("Processing Card"):
        st.markdown("Flow: Input -> Fernet key encryption -> Cipher Token")
        if st.button("Start Simulation", key="aes_start"):
            run_steps(
                [
                    ("info", "Encrypting with Fernet."),
                    ("info", "Generating authentication-safe token."),
                    ("success", "Encryption complete."),
                ]
            )
            bump_simulations()
            add_log("simulation_run", "AES Fernet", actor=st.session_state.current_user or "guest")
            token = aes_encrypt(text, st.session_state.sim_fernet_key)
            st.session_state.aes_output = token

    with card("Output Card"):
        token = st.session_state.get("aes_output", "")
        if token:
            st.code(f"Input: {text}\nOutput token: {token[:260]}{'...' if len(token) > 260 else ''}")

    with card("Attack Explanation Card"):
        render_learning_text(
            "Fernet uses modern symmetric cryptography for secure encryption.",
            "A strong random key encrypts and authenticates content.",
            "It protects confidentiality and integrity for practical app usage.",
        )
        st.success("Weakness: No practical brute-force attack with strong key management.")
        st.success("Attack type: Key theft risk if key handling is poor.")

elif algo == "RSA Encryption/Decryption":
    with card("Input Card"):
        text = st.text_input("Input text", "Secure message for RSA", key="rsa_text")
        if st.button("Generate RSA Key Pair", key="rsa_generate"):
            private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            st.session_state.sim_rsa_private = private
            st.session_state.sim_rsa_public = private.public_key()
            st.success("RSA key pair regenerated.")

    with card("Processing Card"):
        st.markdown("Flow: Input -> Public-key encryption -> Private-key decryption")
        if st.button("Start Simulation", key="rsa_start"):
            run_steps(
                [
                    ("info", "Encrypting message with public key."),
                    ("info", "Decrypting message with private key."),
                    ("success", "RSA cycle complete."),
                ]
            )
            bump_simulations()
            add_log("simulation_run", "RSA Encrypt/Decrypt", actor=st.session_state.current_user or "guest")
            encrypted_bytes = rsa_encrypt(text, st.session_state.sim_rsa_public)
            decrypted_text = rsa_decrypt(encrypted_bytes, st.session_state.sim_rsa_private)
            st.session_state.rsa_output = (encrypted_bytes, decrypted_text)

    with card("Output Card"):
        rsa_out = st.session_state.get("rsa_output")
        if rsa_out:
            encrypted_bytes, decrypted_text = rsa_out
            encoded = base64.b64encode(encrypted_bytes).decode()
            st.code(
                f"Input: {text}\nEncrypted (base64 preview): {encoded[:220]}{'...' if len(encoded) > 220 else ''}\nDecrypted: {decrypted_text}"
            )

    with card("Attack Explanation Card"):
        render_learning_text(
            "RSA uses separate public and private keys.",
            "Public key encrypts; only matching private key decrypts.",
            "It enables secure key exchange and hybrid encryption workflows.",
        )
        st.warning("Weakness: Weak key sizes are vulnerable.")
        st.warning("Attack type: Factorization attacks on small keys.")

elif algo == "Hashing (SHA-256 vs MD5)":
    with card("Input Card"):
        text = st.text_area("Input text", "Hash this message", key="hash_text")

    with card("Processing Card"):
        st.markdown("Flow: Input -> Hash function -> Fixed-length digest")
        if st.button("Start Simulation", key="hash_start"):
            run_steps(
                [
                    ("info", "Computing SHA-256 digest."),
                    ("info", "Computing MD5 digest."),
                    ("success", "Digest generation complete."),
                ]
            )
            bump_simulations()
            add_log("simulation_run", "Hash Comparison", actor=st.session_state.current_user or "guest")
            st.session_state.hash_output = generate_hash(text)

    with card("Output Card"):
        out = st.session_state.get("hash_output")
        if out:
            sha_digest, md5_digest = out
            st.code(f"Input: {text}\nSHA-256: {sha_digest}\nMD5: {md5_digest}")

    with card("Attack Explanation Card"):
        render_learning_text(
            "Hashing converts text into a one-way digest.",
            "SHA-256 is stronger than MD5 for integrity checks.",
            "Use modern hash algorithms for secure validation.",
        )
        st.warning("Weakness: MD5 is collision-prone.")
        st.warning("Attack type: Collision attack.")

elif algo == "Base64 Encoding":
    with card("Input Card"):
        text = st.text_input("Input text", "HELLO BASE64", key="b64_text")

    with card("Processing Card"):
        st.markdown("Flow: Input -> Base64 encoding -> Encoded output")
        if st.button("Start Simulation", key="b64_start"):
            run_steps(
                [
                    ("info", "Encoding bytes to Base64."),
                    ("warning", "Base64 is formatting, not encryption."),
                    ("success", "Encoded output ready."),
                ]
            )
            bump_simulations()
            add_log("simulation_run", "Base64 Encoding", actor=st.session_state.current_user or "guest")
            encoded = base64.b64encode(text.encode()).decode()
            decoded = base64.b64decode(encoded.encode()).decode(errors="ignore")
            st.session_state.base64_output = (encoded, decoded)

    with card("Output Card"):
        out = st.session_state.get("base64_output")
        if out:
            encoded, decoded = out
            st.code(f"Input: {text}\nEncoded: {encoded}\nDecoded: {decoded}")

    with card("Attack Explanation Card"):
        render_learning_text(
            "Base64 converts binary/text to transport-safe text format.",
            "Anyone can decode Base64 without a secret key.",
            "It is useful for encoding, not for security protection.",
        )
        st.error("Weakness: No secrecy at all.")
        st.error("Attack type: Immediate decode (no attack needed).")

else:
    with card("Compare Algorithms"):
        compare_text = st.text_input("Enter one text to compare", "HELLO CyberShieldSim", key="cmp_text")
        compare_shift = st.slider("Caesar shift", 1, 25, 3, key="cmp_shift")
        compare_keyword = st.text_input("Vigenere keyword", "KEY", key="cmp_key")

        if st.button("Start Simulation", key="cmp_start"):
            run_steps(
                [
                    ("info", "Running Caesar encryption."),
                    ("info", "Running Vigenere encryption."),
                    ("info", "Running AES(Fernet) encryption."),
                    ("info", "Running hash generation."),
                    ("success", "Comparison ready."),
                ]
            )
            bump_simulations()
            add_log("simulation_run", "Algorithm Comparison", actor=st.session_state.current_user or "guest")

            caesar_out = caesar_encrypt(compare_text, compare_shift)
            vig_out = vigenere_encrypt(compare_text, compare_keyword)
            aes_out = aes_encrypt(compare_text, st.session_state.sim_fernet_key)
            sha_out, md5_out = generate_hash(compare_text)

            st.code(
                "INPUT -> PROCESS -> OUTPUT\n\n"
                f"Caesar (+{compare_shift}) -> {caesar_out}\n"
                f"Vigenere ({compare_keyword}) -> {vig_out}\n"
                f"AES(Fernet) -> {aes_out[:120]}{'...' if len(aes_out) > 120 else ''}\n"
                f"SHA-256 -> {sha_out}\n"
                f"MD5 -> {md5_out}"
            )

            st.markdown("#### Security Summary")
            st.warning("Caesar: weak, brute-force friendly")
            st.warning("Vigenere: moderate, pattern analysis risk")
            st.success("AES(Fernet): strong with proper key management")
            st.info("Hashes: integrity checks (not encryption)")
