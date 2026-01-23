
import streamlit as st
import cv2
import numpy as np
import os

st.title("🎮 SVD MATRIX ORDER GAME")

# --------- Load Image ----------
IMAGE_PATH = "pic.jpeg"

if not os.path.exists(IMAGE_PATH):
    st.error("❌ pic.png not found in folder")
    st.stop()

img = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)

if img is None:
    st.error("❌ pic.png not readable")
    st.stop()

# 🔥 Resize for speed (very important for cloud)
img = cv2.resize(img, (256, 256))

img = img.astype(np.float32)
h, w = img.shape

# --------- CACHE SVD (KEY OPTIMIZATION) ----------
@st.cache_resource
def compute_svd(image):
    U, S, VT = np.linalg.svd(image, full_matrices=False)
    return U, np.diag(S), VT

U, Sigma, VT = compute_svd(img)

matrices = {
    "U": U,
    "Sigma": Sigma,
    "VT": VT
}

# --------- Helpers ----------
def normalize(mat):
    return cv2.normalize(mat, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

def random_image(shape):
    return np.random.randint(0, 256, shape).astype(np.uint8)

# --------- Dropdown Menus ----------
st.subheader("Select multiplication order")

col1, col2, col3 = st.columns(3)

with col1:
    m1 = st.selectbox("Matrix 1", ["U", "VT", "Sigma"], key="m1")

with col2:
    m2 = st.selectbox("Matrix 2", ["U", "VT", "Sigma"], key="m2")

with col3:
    m3 = st.selectbox("Matrix 3", ["U", "VT", "Sigma"], key="m3")

# --------- Action ----------
if st.button("▶️ Multiply"):

    with st.spinner("Computing matrix multiplication..."):
        try:
            A = matrices[m1]
            B = matrices[m2]
            C = matrices[m3]

            result = A @ B @ C
            output_img = normalize(result)
            title = f"{m1} × {m2} × {m3}"

            st.subheader("Reconstructed Image")
            st.image(output_img, clamp=True)
            st.success(f"Order used: {title}")

        except:
            st.subheader("Reconstructed Image")
            st.image(random_image((h, w)), clamp=True)
            st.warning("Wrong order → Random noise shown")
