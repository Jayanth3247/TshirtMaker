import streamlit as st
from dotenv import load_dotenv
import os

from parse_prompt import parse_design_prompt
from generate_images import generate_image

load_dotenv()

st.set_page_config(page_title="AI T-shirt Designer", layout="centered")
st.title("🧠🎨 AI T-shirt Design Generator")
st.markdown("Describe your dream t-shirt design and let AI bring it to life!")

with st.form("design_form"):
    base_color = st.text_input("Base T-shirt Color", placeholder="e.g., black")
    design_prompt = st.text_area("Design Description", placeholder="Describe front and back designs...")
    submitted = st.form_submit_button("Generate Design")

if submitted:
    if not base_color or not design_prompt:
        st.warning("Please fill in both fields.")
    else:
        with st.spinner("🧠 Thinking..."):
            front_prompt, back_prompt = parse_design_prompt(base_color, design_prompt)

        st.subheader("🎯 Enhanced Prompts")
        st.text_area("Front Prompt", front_prompt, height=100)
        st.text_area("Back Prompt", back_prompt, height=100)

        front_img_path, back_img_path = None, None

        with st.spinner("🎨 Generating Front Design..."):
            front_img_path = generate_image(front_prompt, "front")

        with st.spinner("🎨 Generating Back Design..."):
            if back_prompt.lower() != "plain":
                back_img_path = generate_image(back_prompt, "back")

        if front_img_path:
            st.image(front_img_path, caption="Front Design", use_column_width=True)
        if back_img_path:
            st.image(back_img_path, caption="Back Design", use_column_width=True)
        elif back_prompt.lower() == "plain":
            st.info("Back design is plain (no image generated).")
