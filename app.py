import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Set up the Gemini API key using an environment variable
GEMINI_API_KEY = 'GEMINI_API_KEY'
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY   
# Configure the API
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the GenerativeModel with the appropriate model name
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",  # Ensure this is the correct model name
    generation_config=generation_config,
)

# Start a Flask app
app = Flask(__name__)

# Initialize a chat session globally
chat_session = model.start_chat(history=[])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    if user_input.lower() == "exit":
        return jsonify({"response": "Exiting the chat."})

    response = chat_session.send_message(user_input)
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)
