import os
from streamlit.runtime.scriptrunner.script_runner import RerunException
import streamlit as st

def show_welcomepage():
    # ── Session state to control splash vs. main UI ──
    if "show_splash" not in st.session_state:
        st.session_state.show_splash = True

    if st.session_state.show_splash:
        # Inline CSS to make the splash image full viewport and style button
        st.markdown(
            """
            <style>
              .splash-img {
                display: flex;
                justify-content: center;
                align-items: top;
                height: 100vh;
              }
              .splash-img > img {
                width: 75vw;
                height: 75vh;
                object-fit: cover;
              }
              .stButton > button {
                position: fixed;
                bottom: 0.5rem;
                left: 50%;
                transform: translateX(-50%);
                padding: 0.25rem 2rem;
                font-size: 1.2rem;
                background-color: White;
                color: Black;
                border: none;
                border-radius: 50px;
                cursor: pointer;
                
              }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Splash image (local file)
        img_path = os.path.join(os.path.dirname(__file__), "Welcome_Image2.png")
        st.image(img_path, use_container_width=True)

        # Streamlit button with styling from CSS above
        if st.button("Enter"):
            st.session_state.show_splash = False
            raise RerunException(rerun_data=None)
        st.stop()


if __name__ == "__main__":
    show_welcomepage()
    # Demo main
    st.write("Splash dismissed, now in main app")