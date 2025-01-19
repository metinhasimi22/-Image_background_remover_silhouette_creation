import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import numpy as np

# Set page config first
st.set_page_config(page_title="Background Removal App", layout="wide")

# Dark mod için CSS stilleri
st.markdown("""
    <style>
    /* Genel stil */
    body {
        background-color: black;
        color: white;
        font-family: 'Arial', sans-serif;
    }

    /* Buton stilleri */
    .stDownloadButton button {
        background-color: #4F8BF9;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        transition: background-color 0.3s ease;
        font-size: 16px;
        font-weight: bold;
    }
    .stDownloadButton button:hover {
        background-color: #3B6BB0;
    }

    /* Footer stilleri */
    .footer {
        text-align: center;
        padding: 10px;
        background-color: #333;
        border-radius: 8px;
        margin-top: 20px;
    }

    /* Tooltip stilleri */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Butonun üstünde */
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("🎨 Modern Background Removal App")
st.write("""
    📸 **Upload an image or use your camera to see the background removed results!**
    This app is developed using the `rembg` library.
""")

# Yükleme ekranını daha iyi bir yere taşı
with st.expander("📁 Upload Image or Use Camera", expanded=True):
    option = st.radio("Choose Input Method:", ("Upload Image", "Use Camera"))

    if option == "Upload Image":
        uploaded_file = st.file_uploader("Select an image...", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = st.camera_input("Take a photo")

if uploaded_file is not None:
    # Open and display the original image
    image = Image.open(uploaded_file)
    st.subheader("🖼️ Original Image")
    st.image(image, use_container_width=True, caption="Uploaded Image")

    # Image manipulation options
    st.subheader("🛠️ Image Adjustment")
    rotate_angle = st.slider("Rotate Image (Degrees)", -180, 180, 0, help="Rotate the image by the specified angle.")
    resize_width = st.slider("Resize Width", 100, 1000, image.width, help="Resize the image width while maintaining aspect ratio.")

    # Apply image transformations
    if rotate_angle != 0:
        image = image.rotate(rotate_angle, resample=Image.Resampling.BICUBIC)
    if resize_width != image.width:
        ratio = resize_width / image.width
        height = int(image.height * ratio)
        image = image.resize((resize_width, height), resample=Image.Resampling.LANCZOS)

    # Display the adjusted image
    st.image(image, use_container_width=True, caption="Adjusted Image")

    # Process image to remove background
    with st.spinner("⏳ Removing background... Please wait."):
        output_image = remove(image)

    # Display background removed image
    st.subheader("✅ Background Removed Image")
    st.image(output_image, use_container_width=True, caption="Background Removed Image")

    # Create silhouette
    silhouette = np.array(output_image)
    silhouette[silhouette[..., -1] > 0] = [255, 255, 255, 255]  # Foreground white
    silhouette[silhouette[..., -1] == 0] = [0, 0, 0, 255]  # Background black

    # Display silhouette
    st.subheader("⚫ Silhouette")
    st.image(silhouette, use_container_width=True, caption="Silhouette Image")

    # Download buttons for results
    st.markdown("### 📥 Download Options")

    # Download background removed image
    st.download_button(
        label="⬇️ Download Background Removed Image",
        data=output_image.tobytes(),
        file_name="foreground_image.png",
        mime="image/png",
        key="download_foreground",
        help="Download the image with the background removed."
    )

    # Download silhouette
    silhouette_img = Image.fromarray(silhouette)
    st.download_button(
        label="⬇️ Download Silhouette",
        data=silhouette_img.tobytes(),
        file_name="silhouette_image.png",
        mime="image/png",
        key="download_silhouette",
        help="Download the silhouette image."
    )

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        🚀 **Developed by Metin Haşimi.**<br>
        🌟 Connect with me on <a href="https://www.linkedin.com/in/metin-hasimi-33aa82269" target="_blank">LinkedIn</a> or check out my <a href="https://github.com/metinhasimi22" target="_blank">GitHub</a>.
    </div>
""", unsafe_allow_html=True)