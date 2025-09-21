# app.py
import requests
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Random Image Generator", layout="centered")

st.title("Random Image Generator")
st.write("Click the button to fetch a random image from Picsum.")

# Optional controls for size
col1, col2 = st.columns(2)
with col1:
    width = st.number_input("Width", min_value=1, max_value=4000, value=800, step=1)
with col2:
    height = st.number_input("Height", min_value=1, max_value=4000, value=800, step=1)

# Button to fetch
if st.button("Random Image"):
    url = f"https://picsum.photos/{width}/{height}"
    try:
        # Request the image (Picsum redirects to the final image)
        resp = requests.get(url, stream=True, timeout=15)
        resp.raise_for_status()

        # Read bytes
        image_bytes = resp.content
        final_url = resp.url  # resolved image URL after redirect

        # Display
        st.image(BytesIO(image_bytes), caption=f"Random image — {width}×{height}", use_column_width=True)
        st.markdown(f"**Final image URL:** {final_url}")

    except requests.RequestException as e:
        st.error(f"Failed to fetch image: {e}")

# Helpful footer
st.markdown("---")
st.caption("Images provided by picsum.photos")
