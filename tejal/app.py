import streamlit as st
import requests
import numpy as np
import cv2
import os
from groq import Groq
from PIL import Image

# Constants
REMINI_API_KEY = 'oxbd3InxqF16tNdjTxz1uSrp10BangIGTFJ7cEbPhDtCRlBc'
REMINI_API_URL = 'https://api.remini.com/generate'
GROQ_API_KEY = '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'

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Function to call the Remini API
def call_remini_api(input_text):
    headers = {
        'Authorization': f'Bearer {REMINI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'input_text': input_text
    }
    response = requests.post(REMINI_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('generated_text')
    else:
        st.error(f"Error fetching data: {response.text}")
        return None

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

# Function to generate text using Groq API
def generate_text_groq(input_text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Streamlit UI
st.title("Reminiscence Generator, Photo Enhancer & Remini API")
st.write("Enter a starting sentence to reminisce about, upload a photo to enhance, or use the Remini API!")

# Text generation section
st.header("Generate Reminiscence")
user_input = st.text_input("Input your starting sentence:", key="text_input")

if st.button("Generate Reminiscence"):
    if user_input:
        # Generate text based on user input using Groq
        generated_text = generate_text_groq(user_input)
        st.markdown(f"**Generated Reminiscence:** {generated_text}")
    else:
        st.warning("Please enter a starting sentence.")

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

# API Call section
st.header("Remini API")
if st.button("Generate with Remini API"):
    if user_input:
        # Call Remini API to generate text based on user input
        generated_text_api = call_remini_api(user_input)
        if generated_text_api:
            st.markdown(f"**Generated Text (via API):** {generated_text_api}")
    else:
        st.warning("Please enter a starting sentence.")
