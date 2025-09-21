# app.py
import streamlit as st
from stegano import lsb
import io
from PIL import Image
import tempfile
import traceback
import logging

# basic logging to file (appears in Cloud logs too)
logging.basicConfig(filename="app_error.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

st.set_page_config(page_title="Image Steganography (Encrypt/Decrypt) - Debuggable", layout="centered")
st.title("Image Steganography — Encrypt (hide) / Decrypt (reveal)")

st.markdown("Use PNG (lossless) for reliable results. This app now shows full tracebacks on error for debugging.")

mode = st.radio("Choose mode", ("Encrypt (hide message)", "Decrypt (reveal message)"))

if mode.startswith("Encrypt"):
    st.subheader("Encrypt / Hide a message into an image")
    uploaded = st.file_uploader("Upload cover image (PNG recommended)", type=["png", "jpg", "jpeg"])
    message = st.text_area("Message to hide", height=120)
    if st.button("Encrypt & Generate stego image"):
        if not uploaded:
            st.error("Please upload a cover image (PNG recommended).")
        elif not message:
            st.error("Please enter a message to hide.")
        else:
            try:
                # Read uploaded file as PIL image
                pil_img = Image.open(uploaded).convert("RGBA")

                # OPTIONAL: cap size to avoid memory issues (resize if very large)
                max_side = 1600
                if max(pil_img.size) > max_side:
                    pil_img.thumbnail((max_side, max_side))

                # Save to temporary PNG (stegano expects a filesystem path)
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpf:
                    pil_img.save(tmpf.name, format="PNG")
                    tmp_path = tmpf.name

                # Hide message
                secret_img = lsb.hide(tmp_path, message)
                # Save to buffer
                buf = io.BytesIO()
                secret_img.save(buf, format="PNG")
                buf.seek(0)

                st.success("✅ Stego image generated successfully.")
                st.image(buf.getvalue(), caption="Generated stego image (preview)", use_container_width=True)

                # Download button
                st.download_button(
                    label="Download stego image (PNG)",
                    data=buf.getvalue(),
                    file_name="stego.png",
                    mime="image/png"
                )

            except Exception:
                tb = traceback.format_exc()
                logging.error(tb)
                st.error("An error occurred during encoding. See full traceback below.")
                st.text_area("Traceback (encode)", tb, height=300)

elif mode.startswith("Decrypt"):
    st.subheader("Decrypt / Reveal a message from a stego image")
    uploaded = st.file_uploader("Upload stego image (the image with a hidden message)", type=["png", "jpg", "jpeg"])
    if st.button("Decrypt / Reveal message"):
        if not uploaded:
            st.error("Please upload the stego image.")
        else:
            try:
                # Open and save as PNG to preserve bits
                pil = Image.open(uploaded).convert("RGBA")
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpf:
                    pil.save(tmpf.name, format="PNG")
                    tmp_path = tmpf.name

                revealed = lsb.reveal(tmp_path)
                if revealed is None:
                    st.error("No hidden message detected in image. Make sure the image is a PNG with a hidden message (not a re-saved JPG).")
                else:
                    st.success("🔓 Revealed message:")
                    st.code(revealed)

            except Exception:
                tb = traceback.format_exc()
                logging.error(tb)
                st.error("An error occurred during decoding. See full traceback below.")
                st.text_area("Traceback (decode)", tb, height=300)

st.markdown("---")
st.caption("Notes: Uses stegano.lsb. If app still fails, run `streamlit run app.py` locally to see console traceback.")
