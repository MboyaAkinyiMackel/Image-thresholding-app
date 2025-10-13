import streamlit as st

st.title("🎨 Image Thresholding App")
st.write("Welcome! This is a simple Streamlit test app to confirm deployment works.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Your app is working correctly!")
