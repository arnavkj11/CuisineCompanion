import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_recipe_from_ingredients(ingredients):
    """Generate recipe suggestions based on available ingredients using OpenAI GPT-4o"""
    
    ingredients_text = ", ".join(ingredients)
    
    prompt = f"""
    You are a helpful cooking assistant for elderly people. Based on the following ingredients: {ingredients_text}
    
    Please suggest a simple, healthy, and delicious recipe that can be made with most or all of these ingredients.
    
    Provide your response in JSON format with the following structure:
    {{
        "title": "Recipe name",
        "description": "Brief description of the dish",
        "prep_time": "Estimated preparation time",
        "servings": "Number of servings",
        "ingredients": ["List of ingredients with measurements"],
        "instructions": ["Step-by-step cooking instructions"],
        "tips": ["Helpful cooking tips for elderly cooks"]
    }}
    
    Make sure the recipe is:
    - Easy to follow with clear, simple steps
    - Suitable for elderly people (not too complex)
    - Nutritious and balanced
    - Uses common cooking methods
    - Includes safety tips if needed
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant specialized in creating simple, healthy recipes for elderly people."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=1500,
            temperature=0.7
        )
        
        recipe_json = json.loads(response.choices[0].message.content)
        return recipe_json
        
    except json.JSONDecodeError as e:
        # Fallback to text response if JSON parsing fails
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant specialized in creating simple, healthy recipes for elderly people."},
                {"role": "user", "content": f"Based on these ingredients: {ingredients_text}, suggest a simple, healthy recipe with clear step-by-step instructions suitable for elderly people."}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content
        
    except Exception as e:
        raise Exception(f"Failed to generate recipe: {str(e)}")

def recognize_ingredients_from_image(base64_image):
    """Recognize ingredients from an image using OpenAI Vision API"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                            Look at this image and identify all the food ingredients you can see.
                            Return only a JSON object with an array of ingredient names.
                            Focus on identifying common cooking ingredients like vegetables, fruits, meats, dairy products, grains, spices, etc.
                            Use simple, common names for ingredients (e.g., "tomato" not "roma tomato").
                            
                            Format your response as:
                            {"ingredients": ["ingredient1", "ingredient2", "ingredient3"]}
                            
                            If you cannot identify any food ingredients, return: {"ingredients": []}
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=500
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("ingredients", [])
        
    except json.JSONDecodeError:
        # Fallback to text parsing if JSON fails
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Look at this image and list all the food ingredients you can see, separated by commas. Use simple ingredient names."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        text_result = response.choices[0].message.content
        ingredients = [ing.strip() for ing in text_result.split(',') if ing.strip()]
        return ingredients[:10]  # Limit to 10 ingredients
        
    except Exception as e:
        raise Exception(f"Failed to analyze image: {str(e)}")

def transcribe_audio_to_text(audio_file_path):
    """Transcribe audio file to text using OpenAI Whisper"""
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        return response.text
        
    except Exception as e:
        raise Exception(f"Failed to transcribe audio: {str(e)}")

def extract_ingredients_from_speech(transcribed_text):
    """Extract ingredients from transcribed speech using OpenAI"""
    
    prompt = f"""
    From the following text that was spoken by someone describing their available ingredients:
    "{transcribed_text}"
    
    Extract and list only the food ingredients mentioned. 
    Return the response in JSON format:
    {{"ingredients": ["ingredient1", "ingredient2", "ingredient3"]}}
    
    Only include actual food ingredients (vegetables, fruits, meats, dairy, grains, spices, etc.).
    Use simple, common names for ingredients.
    If no ingredients are mentioned, return: {{"ingredients": []}}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at identifying food ingredients from spoken text."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=300
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("ingredients", [])
        
    except json.JSONDecodeError:
        # Fallback method
        fallback_prompt = f"From this text: '{transcribed_text}', list only the food ingredients mentioned, separated by commas:"
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": fallback_prompt}
            ],
            max_tokens=200
        )
        
        text_result = response.choices[0].message.content
        ingredients = [ing.strip() for ing in text_result.split(',') if ing.strip()]
        return ingredients[:10]  # Limit to 10 ingredients
        
    except Exception as e:
        raise Exception(f"Failed to extract ingredients from speech: {str(e)}")
