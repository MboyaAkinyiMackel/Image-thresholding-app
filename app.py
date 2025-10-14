import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ---------------------------
# APP CONFIG
# ---------------------------
st.set_page_config(page_title="Celestial Image Studio", page_icon="🌙", layout="wide")

# ---------------------------
# CUSTOM STYLE
# ---------------------------
# ---- Celestial UI polish (safe to add; does not change app logic) ----
st.markdown(
    """
    <style>
    /* page background: subtle starry gradient */
    .stApp {
      background: radial-gradient(circle at 10% 10%, rgba(255,255,255,0.03), transparent 5%),
                  radial-gradient(circle at 90% 90%, rgba(255,255,255,0.02), transparent 8%),
                  linear-gradient(180deg, #08020a 0%, #120025 40%, #002a2a 100%);
      color: #eae6ff;
      min-height: 100vh;
    }
    /* sidebar look */
    .css-1d391kg .css-1dq8tca {  /* narrow selection to avoid heavy overrides */
      background: linear-gradient(180deg, rgba(122,0,204,0.12), rgba(0,179,179,0.08));
      border-radius: 12px;
      padding: 18px;
    }
    /* headings */
    h1, h2, h3 {
      color: #f3e6ff;
      text-shadow: 0 2px 10px rgba(122,0,204,0.12);
    }
    /* subsection cards */
    .card {
      background: rgba(255,255,255,0.03);
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.45);
      border: 1px solid rgba(255,255,255,0.03);
    }
    /* buttons */
    .stButton>button {
      background: linear-gradient(90deg,#7a00cc,#00b3b3);
      color: white;
      border-radius: 10px;
      padding: 6px 12px;
    }
    /* small footer */
    .footer {
      color: #cfc7ff;
      font-size: 13px;
      opacity: 0.9;
      text-align: center;
      margin-top: 18px;
    }
    /* responsive tweak for image captions */
    .stImage > figcaption {
      color: #e9e2ff;
    }
    </style>

    <!-- Decorative header area -->
    <div style="display:flex; align-items:center; gap:14px; margin-bottom:12px;">
      <div style="width:64px; height:64px; border-radius:50%; background:
                  radial-gradient(circle at 30% 30%, #ffd27a 0%, #b38cff 40%, #7a00cc 100%);
                  box-shadow: 0 6px 20px rgba(122,0,204,0.25); display:flex; align-items:center; justify-content:center;">
        <span style="font-size:26px; font-weight:700; color:#081018;">🌙</span>
      </div>
      <div>
        <h1 style="margin:0;">Celestial Image Processing Studio</h1>
        <div style="color:#d6cfff; margin-top:4px;">Aesthetic · interactive · ready for experiments</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# optional small footer (place near the bottom of your app's main flow)
st.markdown(
    """<div class="footer">Made with 💜 • Purple · Gold · Turquoise accents • Designed for Kelma</div>""",
    unsafe_allow_html=True,
)
# -----------------------------------------------------------------------

# ---------------------------
# TITLE
# ---------------------------
st.title("🌙 Celestial Image Processing Studio")
st.write("✨ Upload or choose an image and apply transformations in your cosmic workspace.")

# ---------------------------
# SIDEBAR: IMAGE SELECTION
# ---------------------------
st.sidebar.header("🔮 Image Control Panel")
option = st.sidebar.selectbox("Choose how to load your image", ["Upload your own", "Use sample images"])

if option == "Upload your own":
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = np.array(Image.open(uploaded_file))
    else:
        image = None
else:
    sample = st.sidebar.selectbox("Choose a sample image", ["Fruits", "Smarties", "Sudoku", "Gradient", "Coins", "Shapes"])
    try:
        image = cv2.imread(f"images/{sample.lower()}.jpg")
        if image is None:
            image = cv2.imread(f"images/{sample.lower()}.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except:
        image = None

# ---------------------------
# SIDEBAR: TECHNIQUE
# ---------------------------
st.sidebar.subheader("🪄 Choose a Technique")
technique = st.sidebar.selectbox("Select technique", [
    "None",
    "Thresholding",
    "Blurring & Smoothing",
    "Edge Detection",
    "Contours",
    "Template Matching",
    "Segmentation (Watershed)",
    "Color Space Transformations",
    "Image Operations"
])

# ---------------------------
# HELPER: DISPLAY
# ---------------------------
def show_images(original, processed, title):
    st.markdown(f"### ✨ {title}")
    col1, col2 = st.columns(2)
    with col1:
        st.image(original, caption="🩵 Original", use_container_width=True)
    with col2:
        st.image(processed, caption="💜 Processed", use_container_width=True)

# ---------------------------
# PROCESSING SECTION
# ---------------------------
if image is not None:
    output = image.copy()

    # 1️⃣ Thresholding
    if technique == "Thresholding":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        method = st.sidebar.selectbox("Select Threshold Type", ["Binary", "Binary Inv", "Trunc", "ToZero", "Adaptive", "Otsu"])
        if method == "Binary":
            _, output = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        elif method == "Binary Inv":
            _, output = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        elif method == "Trunc":
            _, output = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
        elif method == "ToZero":
            _, output = cv2.threshold(gray, 127, 255, cv2.THRESH_TOZERO)
        elif method == "Adaptive":
            output = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                           cv2.THRESH_BINARY, 11, 2)
        elif method == "Otsu":
            _, output = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        show_images(image, output, "Thresholding")

    # 2️⃣ Blurring & Smoothing
    elif technique == "Blurring & Smoothing":
        method = st.sidebar.selectbox("Choose Blur Type", ["Average", "Gaussian", "Median"])
        k = st.sidebar.slider("Kernel Size", 1, 15, 3, step=2)
        if method == "Average":
            output = cv2.blur(image, (k, k))
        elif method == "Gaussian":
            output = cv2.GaussianBlur(image, (k, k), 0)
        elif method == "Median":
            output = cv2.medianBlur(image, k)
        show_images(image, output, "Blurring & Smoothing")

    # 3️⃣ Edge Detection
    # 3️⃣ Edge Detection
    elif technique == "Edge Detection":
        st.sidebar.subheader("⚡ Edge Detection Settings")
        method = st.sidebar.selectbox("Select Method", ["Sobel", "Scharr", "Laplacian", "Canny"])
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        if method == "Sobel":
            x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel = cv2.magnitude(x, y)
            output = cv2.convertScaleAbs(sobel)
            show_images(image, output, "Edge Detection (Sobel)")

        elif method == "Scharr":
            x = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
            y = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
            scharr = cv2.magnitude(x, y)
            output = cv2.convertScaleAbs(scharr)
            show_images(image, output, "Edge Detection (Scharr)")

        elif method == "Laplacian":
            lap = cv2.Laplacian(gray, cv2.CV_64F)
            output = cv2.convertScaleAbs(lap)
            show_images(image, output, "Edge Detection (Laplacian)")

        elif method == "Canny":
            t1 = st.sidebar.slider("Lower Threshold", 0, 255, 100)
            t2 = st.sidebar.slider("Upper Threshold", 0, 255, 200)
            output = cv2.Canny(gray, t1, t2)
            show_images(image, output, "Edge Detection (Canny)")

    # 4️⃣ Contours
    elif technique == "Contours":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        output = image.copy()
        cv2.drawContours(output, contours, -1, (255, 0, 255), 2)
        show_images(image, output, "Contour Detection")

    # 5️⃣ Template Matching
    elif technique == "Template Matching":
        st.sidebar.write("Upload a smaller template image to search within the main image.")
        template_file = st.sidebar.file_uploader("Upload template", type=["jpg", "png", "jpeg"])
        if template_file:
            template = np.array(Image.open(template_file))
            template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            method = st.sidebar.selectbox("Matching Method", [
                "cv2.TM_CCOEFF", "cv2.TM_CCOEFF_NORMED",
                "cv2.TM_CCORR", "cv2.TM_CCORR_NORMED",
                "cv2.TM_SQDIFF", "cv2.TM_SQDIFF_NORMED"
            ])
            result = cv2.matchTemplate(gray, template_gray, eval(method))
            _, _, _, max_loc = cv2.minMaxLoc(result)
            h, w = template_gray.shape
            output = image.copy()
            cv2.rectangle(output, max_loc, (max_loc[0]+w, max_loc[1]+h), (0, 255, 0), 2)
            show_images(image, output, "Template Matching")
        else:
            st.warning("Please upload a template image.")

    # 6️⃣ Segmentation (Watershed)
    elif technique == "Segmentation (Watershed)":
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(image, markers)
        output = image.copy()
        output[markers == -1] = [255, 0, 255]
        show_images(image, output, "Watershed Segmentation")

    # 7️⃣ Color Space
    elif technique == "Color Space Transformations":
        method = st.sidebar.selectbox("Convert To", ["Grayscale", "HSV", "BGR"])
        if method == "Grayscale":
            output = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        elif method == "HSV":
            output = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        elif method == "BGR":
            output = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        show_images(image, output, "Color Space Transformations")

    # 8️⃣ Image Operations
    elif technique == "Image Operations":
        resize_factor = st.sidebar.slider("Resize (%)", 10, 200, 100)
        brightness = st.sidebar.slider("Brightness", -100, 100, 0)
        contrast = st.sidebar.slider("Contrast", 0.5, 3.0, 1.0)

        height, width = image.shape[:2]
        new_dim = (int(width * resize_factor / 100), int(height * resize_factor / 100))
        output = cv2.resize(image, new_dim, interpolation=cv2.INTER_LINEAR)
        output = cv2.convertScaleAbs(output, alpha=contrast, beta=brightness)

        show_images(image, output, "Image Operations")

else:
    st.info("👆 Please upload or select an image to begin.")



