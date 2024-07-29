import streamlit as st
import numpy as np
import cv2
from PIL import Image
from rembg import remove

# Function to enhance the uploaded image
def enhance_image(image):
    # Convert image to numpy array
    img_np = np.array(image)
    
    # Convert RGB to BGR (OpenCV uses BGR format)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    
    # Enhance image (you can customize this enhancement)
    enhanced_img = cv2.detailEnhance(img_bgr, sigma_s=10, sigma_r=0.15)
    
    # Convert BGR back to RGB
    enhanced_img_rgb = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB)
    
    return enhanced_img_rgb

# Function to change background of the image
def change_background(image, background_image):
    # Remove the background from the original image
    img_no_bg = remove(np.array(image))
    
    # Convert images to PIL
    img_no_bg_pil = Image.fromarray(img_no_bg)
    background_pil = Image.open(background_image).resize(img_no_bg_pil.size)
    
    # Composite the images
    img_with_bg = Image.alpha_composite(background_pil.convert("RGBA"), img_no_bg_pil.convert("RGBA"))
    
    return img_with_bg.convert("RGB")

# Streamlit UI
st.title("Photo Enhancer and Background Changer")
st.write("Upload a photo to enhance or change its background!")

# Image enhancement section
st.header("Enhance Photo")
uploaded_image = st.file_uploader("Upload a photo to enhance (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Convert the uploaded file to an image
    image = Image.open(uploaded_image)
    
    # Display the uploaded image
    st.image(image, caption="Original Image", use_column_width=True)

    # Check if enhancement button is clicked
    if st.button("Enhance Photo"):
        # Enhance the image
        enhanced_image = enhance_image(image)
        
        # Display the enhanced image
        st.image(enhanced_image, caption="Enhanced Image", use_column_width=True)

    # Background change section
    st.header("Change Background")
    uploaded_bg_image = st.file_uploader("Upload a background image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"], key="bg_image")
    
    if uploaded_bg_image is not None:
        # Display the uploaded background image
        st.image(uploaded_bg_image, caption="Background Image", use_column_width=True)
        
        # Check if change background button is clicked
        if st.button("Change Background"):
            # Change the background of the original image
            result_image = change_background(image, uploaded_bg_image)
            
            # Display the image with the new background
            st.image(result_image, caption="Image with New Background", use_column_width=True)
