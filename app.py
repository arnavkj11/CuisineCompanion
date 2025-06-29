import streamlit as st
import base64
import tempfile
import os
from PIL import Image
import io
import speech_recognition as sr
from openai_helper import (
    generate_recipe_from_ingredients,
    recognize_ingredients_from_image,
    transcribe_audio_to_text
)
from utils import validate_ingredients, format_recipe_display

# Configure page settings
st.set_page_config(
    page_title="Cuisine Companion",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dynamic CSS based on theme selection
def get_theme_css(is_dark_mode):
    if is_dark_mode:
        return """
        <style>
            /* Dark Mode Styles */
            .main .block-container {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #1a1a2e 100%) !important;
                color: #ffffff !important;
            }
            
            .main-header {
                font-size: 3rem !important;
                font-weight: bold !important;
                text-align: center !important;
                color: #64ffda !important;
                margin-bottom: 2rem !important;
                text-shadow: 0 0 20px rgba(100, 255, 218, 0.5) !important;
            }
            
            .section-header {
                font-size: 2rem !important;
                font-weight: bold !important;
                color: #bb86fc !important;
                margin: 2rem 0 1rem 0 !important;
                text-shadow: 0 0 10px rgba(187, 134, 252, 0.3) !important;
            }
            
            .instruction-text {
                font-size: 1.2rem !important;
                line-height: 1.6 !important;
                color: #e0e0e0 !important;
                margin-bottom: 1rem !important;
                background: rgba(255, 255, 255, 0.1) !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                border-left: 4px solid #64ffda !important;
                backdrop-filter: blur(10px) !important;
            }
            
            .stButton > button {
                font-size: 1.5rem !important;
                padding: 1rem 2rem !important;
                border-radius: 10px !important;
                font-weight: bold !important;
                min-height: 60px !important;
                background: linear-gradient(135deg, #6200ea, #3700b3) !important;
                color: #ffffff !important;
                border: 2px solid #bb86fc !important;
                box-shadow: 0 4px 15px rgba(98, 0, 234, 0.3) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #3700b3, #6200ea) !important;
                box-shadow: 0 6px 20px rgba(98, 0, 234, 0.5) !important;
                transform: translateY(-2px) !important;
            }
            
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #64ffda, #00bcd4) !important;
                color: #000000 !important;
                border: 2px solid #64ffda !important;
            }
            
            .stTextInput > div > div > input {
                font-size: 1.3rem !important;
                padding: 1rem !important;
                background: rgba(255, 255, 255, 0.1) !important;
                color: #ffffff !important;
                border: 2px solid #64ffda !important;
                border-radius: 10px !important;
            }
            
            .stTextArea > div > div > textarea {
                font-size: 1.3rem !important;
                padding: 1rem !important;
                background: rgba(255, 255, 255, 0.1) !important;
                color: #ffffff !important;
                border: 2px solid #64ffda !important;
                border-radius: 10px !important;
            }
            
            .recipe-container {
                background: rgba(255, 255, 255, 0.1) !important;
                padding: 2rem !important;
                border-radius: 15px !important;
                border: 2px solid #64ffda !important;
                margin: 1rem 0 !important;
                backdrop-filter: blur(10px) !important;
                color: #ffffff !important;
            }
            
            .ingredient-list {
                font-size: 1.2rem !important;
                line-height: 1.8 !important;
                color: #64ffda !important;
                background: rgba(100, 255, 218, 0.1) !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                border-left: 4px solid #64ffda !important;
            }
            
            .success-message {
                background: rgba(76, 175, 80, 0.2) !important;
                color: #4caf50 !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                font-size: 1.2rem !important;
                margin: 1rem 0 !important;
                border: 2px solid #4caf50 !important;
            }
            
            .error-message {
                background: rgba(244, 67, 54, 0.2) !important;
                color: #f44336 !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                font-size: 1.2rem !important;
                margin: 1rem 0 !important;
                border: 2px solid #f44336 !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                background: rgba(255, 255, 255, 0.1) !important;
                border-radius: 10px !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #bb86fc !important;
                font-weight: bold !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: rgba(100, 255, 218, 0.2) !important;
                color: #64ffda !important;
            }
            
            .stSelectbox > div > div {
                background: rgba(255, 255, 255, 0.1) !important;
                color: #ffffff !important;
                border: 2px solid #64ffda !important;
            }
            
            .theme-toggle {
                position: fixed !important;
                top: 1rem !important;
                right: 1rem !important;
                z-index: 999 !important;
                background: rgba(100, 255, 218, 0.2) !important;
                padding: 0.5rem !important;
                border-radius: 25px !important;
                border: 2px solid #64ffda !important;
            }
        </style>
        """
    else:
        return """
        <style>
            /* Light Mode Styles - White and Gray Theme */
            .main .block-container {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 25%, #e9ecef 50%, #dee2e6 100%) !important;
                color: #2c3e50 !important;
            }
            
            .main-header {
                font-size: 3rem !important;
                font-weight: bold !important;
                text-align: center !important;
                color: #2c3e50 !important;
                margin-bottom: 2rem !important;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
            }
            
            .section-header {
                font-size: 2rem !important;
                font-weight: bold !important;
                color: #495057 !important;
                margin: 2rem 0 1rem 0 !important;
            }
            
            .instruction-text {
                font-size: 1.2rem !important;
                line-height: 1.6 !important;
                color: #2c3e50 !important;
                margin-bottom: 1rem !important;
                background: rgba(255, 255, 255, 0.9) !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                border-left: 4px solid #6c757d !important;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
            }
            
            .stButton > button {
                font-size: 1.5rem !important;
                padding: 1rem 2rem !important;
                border-radius: 10px !important;
                font-weight: bold !important;
                min-height: 60px !important;
                background: linear-gradient(135deg, #6c757d, #495057) !important;
                color: #ffffff !important;
                border: 2px solid #6c757d !important;
                box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #495057, #343a40) !important;
                box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4) !important;
                transform: translateY(-2px) !important;
            }
            
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #343a40, #212529) !important;
                color: #ffffff !important;
                border: 2px solid #343a40 !important;
            }
            
            .stTextInput > div > div > input {
                font-size: 1.3rem !important;
                padding: 1rem !important;
                background: rgba(255, 255, 255, 0.95) !important;
                color: #2c3e50 !important;
                border: 2px solid #ced4da !important;
                border-radius: 10px !important;
            }
            
            .stTextArea > div > div > textarea {
                font-size: 1.3rem !important;
                padding: 1rem !important;
                background: rgba(255, 255, 255, 0.95) !important;
                color: #2c3e50 !important;
                border: 2px solid #ced4da !important;
                border-radius: 10px !important;
            }
            
            .recipe-container {
                background: rgba(255, 255, 255, 0.95) !important;
                padding: 2rem !important;
                border-radius: 15px !important;
                border: 2px solid #dee2e6 !important;
                margin: 1rem 0 !important;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
                color: #2c3e50 !important;
            }
            
            .ingredient-list {
                font-size: 1.2rem !important;
                line-height: 1.8 !important;
                color: #2c3e50 !important;
                background: rgba(248, 249, 250, 0.8) !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                border-left: 4px solid #6c757d !important;
            }
            
            .success-message {
                background: rgba(212, 237, 218, 0.8) !important;
                color: #155724 !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                font-size: 1.2rem !important;
                margin: 1rem 0 !important;
                border: 2px solid #c3e6cb !important;
            }
            
            .error-message {
                background: rgba(248, 215, 218, 0.8) !important;
                color: #721c24 !important;
                padding: 1rem !important;
                border-radius: 10px !important;
                font-size: 1.2rem !important;
                margin: 1rem 0 !important;
                border: 2px solid #f5c6cb !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                background: rgba(255, 255, 255, 0.9) !important;
                border-radius: 10px !important;
                border: 1px solid #dee2e6 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #6c757d !important;
                font-weight: bold !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: rgba(248, 249, 250, 0.8) !important;
                color: #495057 !important;
            }
            
            .stSelectbox > div > div {
                background: rgba(255, 255, 255, 0.95) !important;
                color: #2c3e50 !important;
                border: 2px solid #ced4da !important;
            }
            
            .theme-toggle {
                position: fixed !important;
                top: 1rem !important;
                right: 1rem !important;
                z-index: 999 !important;
                background: rgba(255, 255, 255, 0.95) !important;
                padding: 0.5rem !important;
                border-radius: 25px !important;
                border: 2px solid #dee2e6 !important;
            }
        </style>
        """



def main():
    # Initialize session state for theme
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # Theme toggle in sidebar/top
    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        theme_button_text = "🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"
        if st.button(theme_button_text, key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🍳 Cuisine Companion</h1>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-text" style="text-align: center;">Tell me what ingredients you have, and I\'ll suggest delicious recipes you can make!</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'ingredients' not in st.session_state:
        st.session_state.ingredients = []
    if 'current_recipe' not in st.session_state:
        st.session_state.current_recipe = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["📝 Type Ingredients", "📷 Photo of Ingredients", "🎤 Voice Input"])
    
    with tab1:
        handle_text_input()
    
    with tab2:
        handle_photo_input()
    
    with tab3:
        handle_voice_input()
    
    # Display current ingredients
    if st.session_state.ingredients:
        display_ingredients()
    
    # Generate recipe button
    if st.session_state.ingredients and not st.session_state.processing:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🍽️ Get Recipe Suggestions", type="primary", use_container_width=True):
                generate_recipe()
    
    # Display recipe
    if st.session_state.current_recipe:
        display_recipe()

def handle_text_input():
    st.markdown('<h2 class="section-header">Type Your Ingredients</h2>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-text">Enter the ingredients you have, separated by commas (e.g., chicken, rice, onions, tomatoes)</p>', unsafe_allow_html=True)
    
    ingredient_input = st.text_area(
        "Your ingredients:",
        placeholder="Type your ingredients here...",
        height=150,
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Add These Ingredients", use_container_width=True):
            if ingredient_input.strip():
                new_ingredients = [ing.strip() for ing in ingredient_input.split(',') if ing.strip()]
                validated_ingredients = validate_ingredients(new_ingredients)
                st.session_state.ingredients.extend(validated_ingredients)
                st.session_state.ingredients = list(set(st.session_state.ingredients))  # Remove duplicates
                st.rerun()
            else:
                st.error("Please enter some ingredients first.")
    
    with col2:
        if st.button("Clear All", use_container_width=True):
            st.session_state.ingredients = []
            st.session_state.current_recipe = None
            st.rerun()

def handle_photo_input():
    st.markdown('<h2 class="section-header">Photo of Your Ingredients</h2>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-text">Take a photo of your ingredients or upload an image from your device</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Your ingredients photo", use_column_width=True)
        
        if st.button("🔍 Recognize Ingredients from Photo", use_container_width=True):
            with st.spinner("Analyzing your photo... This may take a moment."):
                try:
                    # Convert image to base64
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format='JPEG')
                    img_str = base64.b64encode(img_buffer.getvalue()).decode()
                    
                    # Recognize ingredients using OpenAI Vision
                    recognized_ingredients = recognize_ingredients_from_image(img_str)
                    
                    if recognized_ingredients:
                        st.session_state.ingredients.extend(recognized_ingredients)
                        st.session_state.ingredients = list(set(st.session_state.ingredients))  # Remove duplicates
                        st.markdown(f'<div class="success-message">Found ingredients: {", ".join(recognized_ingredients)}</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-message">Could not identify any ingredients in the photo. Please try a clearer image.</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f'<div class="error-message">Error analyzing photo: {str(e)}</div>', unsafe_allow_html=True)

def handle_voice_input():
    st.markdown('<h2 class="section-header">Voice Input</h2>', unsafe_allow_html=True)
    st.markdown('<p class="instruction-text">Record yourself saying what ingredients you have</p>', unsafe_allow_html=True)
    
    # Audio recording using streamlit-audio-recorder would be ideal, but we'll use file upload for now
    st.markdown('<p class="instruction-text">Upload an audio file (WAV, MP3, M4A) where you mention your ingredients</p>', unsafe_allow_html=True)
    
    audio_file = st.file_uploader(
        "Choose an audio file",
        type=['wav', 'mp3', 'm4a'],
        label_visibility="collapsed"
    )
    
    if audio_file is not None:
        st.audio(audio_file, format='audio/wav')
        
        if st.button("🎧 Convert Speech to Text", use_container_width=True):
            with st.spinner("Converting your speech to text... Please wait."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                        tmp_file.write(audio_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Transcribe audio using OpenAI Whisper
                    transcribed_text = transcribe_audio_to_text(tmp_file_path)
                    
                    # Clean up temporary file
                    os.unlink(tmp_file_path)
                    
                    if transcribed_text:
                        st.markdown(f'<div class="success-message">You said: "{transcribed_text}"</div>', unsafe_allow_html=True)
                        
                        # Extract ingredients from transcribed text
                        ingredients_from_speech = extract_ingredients_from_text(transcribed_text)
                        
                        if ingredients_from_speech:
                            st.session_state.ingredients.extend(ingredients_from_speech)
                            st.session_state.ingredients = list(set(st.session_state.ingredients))  # Remove duplicates
                            st.markdown(f'<div class="success-message">Added ingredients: {", ".join(ingredients_from_speech)}</div>', unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown('<div class="error-message">Could not identify any ingredients from your speech. Please try again.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">Could not transcribe the audio. Please try again with a clearer recording.</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f'<div class="error-message">Error processing audio: {str(e)}</div>', unsafe_allow_html=True)

def extract_ingredients_from_text(text):
    """Extract ingredients from transcribed text using OpenAI"""
    try:
        from openai_helper import extract_ingredients_from_speech
        return extract_ingredients_from_speech(text)
    except Exception as e:
        st.error(f"Error extracting ingredients: {str(e)}")
        return []

def display_ingredients():
    st.markdown('<h2 class="section-header">Your Ingredients</h2>', unsafe_allow_html=True)
    
    # Display ingredients in a nice format
    ingredients_text = ", ".join(st.session_state.ingredients)
    st.markdown(f'<div class="ingredient-list">🥕 {ingredients_text}</div>', unsafe_allow_html=True)
    
    # Option to remove individual ingredients
    if len(st.session_state.ingredients) > 1:
        st.markdown('<p class="instruction-text">Remove an ingredient:</p>', unsafe_allow_html=True)
        ingredient_to_remove = st.selectbox(
            "Select ingredient to remove:",
            options=st.session_state.ingredients,
            label_visibility="collapsed"
        )
        
        if st.button(f"Remove {ingredient_to_remove}", use_container_width=True):
            st.session_state.ingredients.remove(ingredient_to_remove)
            st.rerun()

def generate_recipe():
    st.session_state.processing = True
    
    with st.spinner("Finding delicious recipes for you... This may take a moment."):
        try:
            recipe = generate_recipe_from_ingredients(st.session_state.ingredients)
            st.session_state.current_recipe = recipe
            st.session_state.processing = False
            st.rerun()
        except Exception as e:
            st.session_state.processing = False
            st.markdown(f'<div class="error-message">Error generating recipe: {str(e)}</div>', unsafe_allow_html=True)

def display_recipe():
    st.markdown('<h2 class="section-header">🍽️ Recipe Suggestions</h2>', unsafe_allow_html=True)
    
    recipe = st.session_state.current_recipe
    
    # Display recipe in a formatted container
    st.markdown('<div class="recipe-container">', unsafe_allow_html=True)
    
    if isinstance(recipe, dict):
        # If recipe is structured JSON
        st.markdown(f"### {recipe.get('title', 'Suggested Recipe')}")
        
        if recipe.get('description'):
            st.markdown(f"**Description:** {recipe['description']}")
        
        if recipe.get('prep_time'):
            st.markdown(f"**Preparation Time:** {recipe['prep_time']}")
        
        if recipe.get('servings'):
            st.markdown(f"**Servings:** {recipe['servings']}")
        
        if recipe.get('ingredients'):
            st.markdown("**Ingredients:**")
            for ingredient in recipe['ingredients']:
                st.markdown(f"• {ingredient}")
        
        if recipe.get('instructions'):
            st.markdown("**Instructions:**")
            for i, instruction in enumerate(recipe['instructions'], 1):
                st.markdown(f"{i}. {instruction}")
        
        if recipe.get('tips'):
            st.markdown("**Tips:**")
            for tip in recipe['tips']:
                st.markdown(f"💡 {tip}")
    else:
        # If recipe is plain text
        st.markdown(recipe)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Option to get another recipe
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Get Another Recipe", use_container_width=True):
            generate_recipe()
    
    with col2:
        if st.button("🆕 Start Over", use_container_width=True):
            st.session_state.ingredients = []
            st.session_state.current_recipe = None
            st.rerun()

if __name__ == "__main__":
    main()
