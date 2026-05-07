from contextlib import contextmanager
import time

import streamlit as st


@contextmanager
def card(title: str):
    st.markdown(f'<div class="edu-card"><h3 style="margin-top:0;">{title}</h3>', unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)


def run_step_animation(steps: list[tuple[str, str]], delay: float = 0.6) -> None:
    """
    steps: list of (level, message), level in {"info", "warning", "error", "success"}.
    """
    progress = st.progress(0)
    placeholder = st.empty()
    total = len(steps) if steps else 1

    for index, (level, message) in enumerate(steps, start=1):
        progress.progress(int(index * 100 / total))
        if level == "warning":
            placeholder.warning(message)
        elif level == "error":
            placeholder.error(message)
        elif level == "success":
            placeholder.success(message)
        else:
            placeholder.info(message)
        time.sleep(delay)

    progress.progress(100)
