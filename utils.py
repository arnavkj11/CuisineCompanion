import re
import streamlit as st

def validate_ingredients(ingredients):
    """Validate and clean ingredient list"""
    validated = []
    
    for ingredient in ingredients:
        # Clean the ingredient name
        cleaned = ingredient.strip().lower()
        
        # Remove extra spaces and special characters
        cleaned = re.sub(r'[^\w\s]', '', cleaned)
        cleaned = ' '.join(cleaned.split())
        
        # Skip empty or very short ingredients
        if len(cleaned) < 2:
            continue
            
        # Skip common non-ingredient words
        skip_words = {'and', 'or', 'the', 'a', 'an', 'some', 'any', 'with', 'have', 'got', 'i', 'we', 'my', 'our'}
        if cleaned in skip_words:
            continue
            
        # Capitalize first letter for display
        cleaned = cleaned.capitalize()
        validated.append(cleaned)
    
    return validated

def format_recipe_display(recipe_text):
    """Format recipe text for better display"""
    if not recipe_text:
        return "No recipe available"
    
    # Basic formatting improvements
    formatted = recipe_text.replace('\n\n', '\n')
    formatted = formatted.replace('**', '')
    
    return formatted

def is_valid_ingredient(ingredient):
    """Check if a string looks like a valid ingredient"""
    if not ingredient or len(ingredient.strip()) < 2:
        return False
    
    # Check if it contains mostly letters
    letter_count = sum(1 for c in ingredient if c.isalpha())
    total_count = len(ingredient.replace(' ', ''))
    
    if total_count == 0:
        return False
    
    letter_ratio = letter_count / total_count
    return letter_ratio > 0.5

def get_ingredient_suggestions():
    """Get common ingredient suggestions for elderly users"""
    suggestions = [
        "Chicken", "Beef", "Fish", "Eggs", "Rice", "Pasta", "Bread",
        "Onions", "Garlic", "Tomatoes", "Potatoes", "Carrots", "Broccoli",
        "Bell peppers", "Spinach", "Lettuce", "Mushrooms", "Cheese",
        "Milk", "Butter", "Olive oil", "Salt", "Pepper", "Herbs",
        "Bananas", "Apples", "Lemons", "Oranges"
    ]
    return suggestions

def display_error_message(message):
    """Display a user-friendly error message"""
    st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)

def display_success_message(message):
    """Display a success message"""
    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)

def display_info_message(message):
    """Display an info message"""
    st.info(f"ℹ️ {message}")

def chunk_ingredients(ingredients, chunk_size=10):
    """Split ingredients into smaller chunks for API calls"""
    for i in range(0, len(ingredients), chunk_size):
        yield ingredients[i:i + chunk_size]

def clean_recipe_json(recipe_data):
    """Clean and validate recipe JSON data"""
    if not isinstance(recipe_data, dict):
        return recipe_data
    
    # Ensure required fields exist
    required_fields = ['title', 'ingredients', 'instructions']
    for field in required_fields:
        if field not in recipe_data:
            recipe_data[field] = f"No {field} provided"
    
    # Clean ingredients list
    if isinstance(recipe_data.get('ingredients'), list):
        recipe_data['ingredients'] = [ing for ing in recipe_data['ingredients'] if ing and ing.strip()]
    
    # Clean instructions list
    if isinstance(recipe_data.get('instructions'), list):
        recipe_data['instructions'] = [inst for inst in recipe_data['instructions'] if inst and inst.strip()]
    
    return recipe_data

def estimate_cooking_difficulty(recipe_data):
    """Estimate cooking difficulty based on recipe complexity"""
    if not isinstance(recipe_data, dict):
        return "Medium"
    
    ingredients_count = len(recipe_data.get('ingredients', []))
    instructions_count = len(recipe_data.get('instructions', []))
    
    if ingredients_count <= 5 and instructions_count <= 5:
        return "Easy"
    elif ingredients_count <= 10 and instructions_count <= 10:
        return "Medium"
    else:
        return "Advanced"

def get_nutritional_tips():
    """Get general nutritional tips for elderly users"""
    tips = [
        "Include protein in every meal for muscle health",
        "Choose colorful vegetables for vitamins and minerals",
        "Stay hydrated by drinking water throughout the day",
        "Include calcium-rich foods for bone health",
        "Limit sodium to support heart health",
        "Include fiber-rich foods for digestive health"
    ]
    return tips
