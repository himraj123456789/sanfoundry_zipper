# app.py
import requests
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Random Image Generator", layout="centered")

st.title(" 🖼️ Random Image Generator 🖼️")
#st.write("Click the button to fetch a random 800×800 image from Picsum.")

WIDTH, HEIGHT = 800, 800  # fixed size

if st.button("Random Image"):
    url = f"https://picsum.photos/{WIDTH}/{HEIGHT}"
    try:
        # Request the image (Picsum redirects to the final image)
        resp = requests.get(url, stream=True, timeout=15)
        resp.raise_for_status()

        # Read bytes
        image_bytes = resp.content
        final_url = resp.url  # resolved image URL after redirect

        # Display
        st.image(BytesIO(image_bytes), caption="Random 800×800 image", use_container_width=True)
        #st.markdown(f"**Final image URL:** {final_url}")

    except requests.RequestException as e:
        st.error(f"Failed to fetch image: {e}")

st.markdown("---")
st.caption(" ❤️ Thanku for using ❤️ ")


