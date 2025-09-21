# app.py
import streamlit as st
from stegano import lsb
import io
from PIL import Image
import tempfile

st.set_page_config(page_title="Image Steganography (Encrypt / Decrypt)", layout="centered")

st.title("Image Steganography — Encrypt (hide) / Decrypt (reveal)")

# UI: choose mode
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

                # Save to temporary PNG (stegano expects a file path)
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

            except Exception as e:
                st.error(f"Failed to hide message: {e}")

elif mode.startswith("Decrypt"):
    st.subheader("Decrypt / Reveal a message from a stego image")

    uploaded = st.file_uploader("Upload stego image (the image with a hidden message)", type=["png", "jpg", "jpeg"])
    if st.button("Decrypt / Reveal message"):
        if not uploaded:
            st.error("Please upload the stego image.")
        else:
            try:
                # Open uploaded as PNG to preserve LSBs
                pil = Image.open(uploaded).convert("RGBA")
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpf:
                    pil.save(tmpf.name, format="PNG")
                    tmp_path = tmpf.name

                revealed = lsb.reveal(tmp_path)
                if revealed is None:
                    st.error("No hidden message detected in image.")
                else:
                    st.success("🔓 Revealed message:")
                    st.code(revealed)

            except Exception as e:
                st.error(f"Failed to reveal message: {e}")

st.markdown("---")
st.caption( " Thank u for using ")
