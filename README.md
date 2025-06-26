# Recipe Helper App 🍳

A user-friendly web application designed specifically for elderly people to discover delicious recipes based on available ingredients. The app supports three convenient input methods: text input, photo recognition, and voice commands.

## Features

- **Text Input**: Type your available ingredients separated by commas
- **Photo Recognition**: Upload a photo of your ingredients and let AI identify them
- **Voice Input**: Record yourself mentioning your ingredients for hands-free operation
- **AI-Powered Recipe Generation**: Get personalized recipe suggestions using OpenAI's GPT-4o
- **Elderly-Friendly Design**: Large fonts, clear buttons, and intuitive interface
- **Smart Ingredient Management**: Add, remove, and manage your ingredient list easily

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Services**: OpenAI GPT-4o for recipe generation, Vision API for image recognition, Whisper for speech-to-text
- **Image Processing**: PIL (Python Imaging Library)
- **Audio Processing**: SpeechRecognition library
- **Backend**: Python 3.11

## Prerequisites

- Python 3.11 or higher
- OpenAI API key (required for AI features)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/recipe-helper-app.git
   cd recipe-helper-app
   ```

2. **Install dependencies**:
   ```bash
   pip install streamlit openai pillow speechrecognition
   ```
   
   Or if you're using the provided configuration:
   ```bash
   pip install -r pyproject.toml
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root (recommended), or set the environment variable in your terminal:
   
   **On Windows (cmd.exe):**
   ```cmd
   set OPENAI_API_KEY=your-openai-api-key-here
   ```
   
   **On macOS/Linux (bash):**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```
   
   *(If you use a `.env` file, you may need to install the `python-dotenv` package and add a line to your code to load it. Let us know if you want this!)*

   **How to get an OpenAI API key**:
   - Visit [platform.openai.com](https://platform.openai.com)
   - Create an account or sign in
   - Navigate to API Keys section
   - Create a new API key
   - Copy the key (it starts with "sk-...")

## Running the Application

1. **Start the application**:
   In the same terminal where you set the environment variable (if not using a `.env` file), run:
   ```cmd
   streamlit run app.py --server.port 5000
   ```

2. **Access the app**:
   Open your web browser and go to `http://localhost:5000`

## How to Use

### Method 1: Text Input
1. Click on the "📝 Type Ingredients" tab
2. Enter your ingredients separated by commas (e.g., "chicken, rice, onions, tomatoes")
3. Click "Add These Ingredients"
4. Click "🍽️ Get Recipe Suggestions" to generate recipes

### Method 2: Photo Recognition
1. Click on the "📷 Photo of Ingredients" tab
2. Upload a photo of your ingredients (PNG, JPG, or JPEG format)
3. Click "🔍 Recognize Ingredients from Photo"
4. Review the identified ingredients and generate recipes

### Method 3: Voice Input
1. Click on the "🎤 Voice Input" tab
2. Upload an audio file (WAV, MP3, or M4A) where you mention your ingredients
3. Click "🎧 Convert Speech to Text"
4. The app will extract ingredients from your speech and suggest recipes

## Project Structure

```
recipe-helper-app/
├── app.py                 # Main Streamlit application
├── openai_helper.py       # OpenAI API integration functions
├── utils.py              # Utility functions for data processing
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── pyproject.toml        # Python dependencies and project configuration
├── uv.lock              # Dependency lock file
└── README.md            # This file
```

## Configuration

The app is configured for optimal performance with elderly users:

- **Large text sizes** for better readability
- **Clear, prominent buttons** for easy interaction
- **Simple navigation** with tabbed interface
- **Helpful error messages** with clear instructions
- **Safety considerations** in recipe suggestions

## API Usage

The application uses several OpenAI services:

- **GPT-4o**: For recipe generation and ingredient extraction from text
- **Vision API**: For identifying ingredients in uploaded photos
- **Whisper**: For converting audio recordings to text

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY environment variable is not set"**
   - Ensure you've set the OpenAI API key as an environment variable
   - Check that the key is valid and has sufficient credits

2. **Photo recognition not working**
   - Ensure the photo is clear and well-lit
   - Supported formats: PNG, JPG, JPEG
   - Try taking a photo with better lighting or closer to ingredients

3. **Voice input issues**
   - Supported audio formats: WAV, MP3, M4A
   - Speak clearly and mention ingredients specifically
   - Ensure audio file is not too long (under 25MB)

4. **App not loading**
   - Check that port 5000 is not being used by another application
   - Ensure all dependencies are properly installed

### Performance Tips

- For better photo recognition, ensure ingredients are clearly visible and well-separated
- When recording voice input, speak slowly and clearly
- List ingredients using common names (e.g., "tomato" instead of "cherry tomato")

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the OpenAI API documentation
3. Create an issue on GitHub with detailed information about the problem

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Powered by [OpenAI](https://openai.com/) for AI capabilities
- Designed with accessibility and elderly users in mind

---

**Note**: This application requires an active internet connection and valid OpenAI API key to function properly. API usage may incur costs based on OpenAI's pricing structure.