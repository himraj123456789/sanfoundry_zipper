import streamlit as st
from PIL import Image
import io
import tempfile
import traceback

st.set_page_config(page_title="Image Steganography (no stegano)", layout="centered")
st.title("Image Steganography — Encrypt / Decrypt ")


# ---- LSB encode/decode (pure Pillow) ----
def _int_to_bits(n: int, bits: int):
    return [(n >> (bits - 1 - i)) & 1 for i in range(bits)]

def _bits_to_int(bits):
    n = 0
    for b in bits:
        n = (n << 1) | (b & 1)
    return n

def _data_to_bits(data: bytes):
    for byte in data:
        for i in range(8):
            yield (byte >> (7 - i)) & 1

def lsb_hide(pil_img: Image.Image, message: str) -> Image.Image:
    """
    Hide message in a copy of pil_img, return new PIL image (RGBA).
    Stores 32-bit message length (bytes) then message bytes.
    """
    img = pil_img.convert("RGBA")
    pixels = list(img.getdata())
    msg_bytes = message.encode("utf-8")
    msg_len = len(msg_bytes)

    capacity_bits = len(pixels) * 3  # using R,G,B LSBs
    needed_bits = 32 + msg_len * 8
    if needed_bits > capacity_bits:
        raise ValueError(f"Message too large for image capacity. Capacity bits={capacity_bits}, needed_bits={needed_bits}")

    length_bits = _int_to_bits(msg_len, 32)
    message_bits = list(_data_to_bits(msg_bytes))
    all_bits = iter(length_bits + message_bits)

    new_pixels = []
    for px in pixels:
        r, g, b, a = px
        new_rgb = []
        for color in (r, g, b):
            try:
                bit = next(all_bits)
                color = (color & ~1) | bit
            except StopIteration:
                # no more bits to write; leave remaining colors unchanged
                pass
            new_rgb.append(color)
        new_pixels.append((new_rgb[0], new_rgb[1], new_rgb[2], a))

    out = Image.new(img.mode, img.size)
    out.putdata(new_pixels)
    return out

def lsb_reveal(pil_img: Image.Image) -> str | None:
    """
    Reveal hidden message (returns string) or None if not present/incomplete.
    """
    img = pil_img.convert("RGBA")
    pixels = list(img.getdata())
    all_lsbs = []
    for (r, g, b, a) in pixels:
        all_lsbs.extend([r & 1, g & 1, b & 1])

    if len(all_lsbs) < 32:
        return None
    length_bits = all_lsbs[:32]
    msg_len = _bits_to_int(length_bits)
    total_message_bits = msg_len * 8
    if len(all_lsbs) < 32 + total_message_bits:
        return None  # truncated / no message
    message_bits = all_lsbs[32:32 + total_message_bits]

    msg_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        byte_bits = message_bits[i:i+8]
        val = _bits_to_int(byte_bits)
        msg_bytes.append(val)

    try:
        return msg_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None

# ---- UI ----
mode = st.radio("Mode", ("Encrypt (hide message)", "Decrypt (reveal message)"))

if mode == "Encrypt (hide message)":
    st.subheader("Encrypt / Hide a message into an image")
    uploaded = st.file_uploader("Upload cover image ", type=["png", "jpg", "jpeg"])
    message = st.text_area("Message to hide", height=160)
    if st.button("Encrypt & Generate stego image"):
        if not uploaded:
            st.error("Please upload a cover image (PNG recommended).")
        elif not message:
            st.error("Please enter a message to hide.")
        else:
            try:
                pil = Image.open(uploaded).convert("RGBA")

                # optional: downscale very large images to avoid memory issues
                max_side = 1600
                if max(pil.size) > max_side:
                    pil.thumbnail((max_side, max_side))

                stego = lsb_hide(pil, message)

                buf = io.BytesIO()
                stego.save(buf, format="PNG")
                buf.seek(0)

                st.success("✅ Stego image generated.")
                st.image(buf.getvalue(), caption="Stego image preview", use_container_width=True)

                st.download_button(
                    label="Download stego image (PNG)",
                    data=buf.getvalue(),
                    file_name="stego.png",
                    mime="image/png"
                )

            except Exception as e:
                tb = traceback.format_exc()
                st.error(f"Failed to create stego image: {e}")
                st.text_area("Traceback", tb, height=300)

elif mode == "Decrypt (reveal message)":
    st.subheader("Decrypt / Reveal a message from a stego image")
    uploaded = st.file_uploader("Upload stego image (PNG containing hidden message)", type=["png", "jpg", "jpeg"])
    if st.button("Decrypt / Reveal message"):
        if not uploaded:
            st.error("Please upload the stego image.")
        else:
            try:
                pil = Image.open(uploaded).convert("RGBA")
                # Save as PNG in-memory to preserve bits, then reveal
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpf:
                    pil.save(tmpf.name, format="PNG")
                    tmp_path = tmpf.name
                # Re-open from disk to mimic consistent reading
                pil2 = Image.open(tmp_path).convert("RGBA")
                revealed = lsb_reveal(pil2)
                if revealed is None:
                    st.error("No hidden message found or message corrupted (maybe image was saved as JPG).")
                else:
                    st.success("🔓 Revealed message:")
                    st.code(revealed)

            except Exception as e:
                tb = traceback.format_exc()
                st.error(f"Failed to reveal message: {e}")
                st.text_area("Traceback", tb, height=300)

st.markdown("---")
st.caption("Notes: uses simple LSB; keep messages reasonably short. Always use PNG for stego images. This implementation avoids stegano and OpenCV.")
