import streamlit as st

# Page config
st.set_page_config(page_title="Msg", layout="centered")

# Custom styling
st.markdown(
    """
    <style>
    .container {
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
        margin-top: 25vh;
    }
    .emoji {
        font-size: 90px;
    }
    .text {
        font-size: 38px;
        font-weight: 600;
        color: #444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display message
st.markdown(
    """
    <div class="container">
        <div class="emoji">😢</div>
        <div class="text">Time expired Due public github</div>
    </div>
    """,
    unsafe_allow_html=True
)
