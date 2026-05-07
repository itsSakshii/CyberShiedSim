import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg-grad-1: #f4ecff;
            --bg-grad-2: #e8f3ff;
            --bg-grad-3: #f6f3ff;
            --text-main: #322f46;
            --text-muted: #5f5a79;
            --card-bg: rgba(255, 255, 255, 0.88);
            --card-border: #ddd8f5;
            --card-shadow: 0 12px 28px rgba(132, 145, 195, 0.18);
            --accent: #8d82f0;
            --accent-2: #6ea4ff;
            --info-bg: #f2f6ff;
            --success-bg: #eef9f3;
            --warn-bg: #fff9ee;
            --error-bg: #fff1f1;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-grad-1: #17162a;
                --bg-grad-2: #1a2234;
                --bg-grad-3: #201d35;
                --text-main: #edeafc;
                --text-muted: #c5c1df;
                --card-bg: rgba(33, 35, 56, 0.82);
                --card-border: #3f4168;
                --card-shadow: 0 14px 30px rgba(5, 6, 13, 0.42);
                --accent: #a497ff;
                --accent-2: #8db5ff;
                --info-bg: rgba(77, 110, 176, 0.18);
                --success-bg: rgba(69, 141, 96, 0.2);
                --warn-bg: rgba(156, 126, 57, 0.2);
                --error-bg: rgba(168, 81, 81, 0.24);
            }
        }

        .stApp {
            background: radial-gradient(circle at 15% 15%, rgba(166, 153, 255, 0.12), transparent 25%),
                        radial-gradient(circle at 85% 10%, rgba(123, 182, 255, 0.15), transparent 28%),
                        linear-gradient(135deg, var(--bg-grad-1) 0%, var(--bg-grad-2) 50%, var(--bg-grad-3) 100%);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }
        .block-container {
            max-width: 1120px;
            padding-top: 2rem;
            padding-bottom: 2.5rem;
        }
        h1, h2, h3, h4 {
            color: var(--text-main) !important;
            letter-spacing: 0.15px;
        }
        .hero-text {
            font-size: 1.04rem;
            line-height: 1.68;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }
        .edu-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.1rem 1.1rem 1rem 1.1rem;
            margin: 0.45rem 0 1rem 0;
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }
        .explain-box {
            background: color-mix(in srgb, var(--card-bg) 85%, transparent);
            border-left: 4px solid var(--accent);
            border-radius: 12px;
            padding: 0.8rem 0.9rem;
            margin: 0.5rem 0 0.8rem 0;
        }
        div[data-testid="stSidebar"] {
            background: color-mix(in srgb, var(--card-bg) 85%, transparent);
            border-right: 1px solid var(--card-border);
        }
        div[data-testid="stSidebar"] * {
            color: var(--text-main) !important;
        }
        .stMetric {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 0.35rem 0.55rem;
            box-shadow: var(--card-shadow);
        }
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        textarea,
        input {
            border-radius: 12px !important;
            border: 1px solid var(--card-border) !important;
            background: color-mix(in srgb, var(--card-bg) 93%, transparent) !important;
            color: var(--text-main) !important;
        }
        .stButton > button {
            border-radius: 12px;
            border: 1px solid color-mix(in srgb, var(--accent) 55%, var(--card-border));
            background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 80%, white), color-mix(in srgb, var(--accent-2) 75%, white));
            color: #ffffff;
            font-weight: 600;
            padding: 0.45rem 0.85rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 8px 18px rgba(102, 116, 186, 0.28);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 22px rgba(96, 111, 188, 0.34);
        }
        div[data-testid="stAlert"] {
            border-radius: 12px;
            border: 1px solid var(--card-border);
        }
        div[data-testid="stAlert"][kind="info"] {
            background: var(--info-bg);
        }
        div[data-testid="stAlert"][kind="success"] {
            background: var(--success-bg);
        }
        div[data-testid="stAlert"][kind="warning"] {
            background: var(--warn-bg);
        }
        div[data-testid="stAlert"][kind="error"] {
            background: var(--error-bg);
        }
        .stCodeBlock {
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
