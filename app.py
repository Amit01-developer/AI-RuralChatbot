from flask import Flask, render_template, request, jsonify
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Fallback responses if API fails
FALLBACK_RESPONSES = {
    "hello": "Hello! I'm your Rural Career Guide. I can help you explore career options in agriculture, education, healthcare, and digital fields. What would you like to know?",
    "hi": "Hi there! I'm here to help rural communities find career opportunities. How can I assist you today?",
    "career": "Rural areas offer diverse career paths including: 1) Agriculture and agribusiness, 2) Healthcare services, 3) Education, 4) Tourism and hospitality, 5) Digital and remote work. Which area interests you?",
    "agriculture": "Modern agriculture careers include: organic farming, agricultural technology, food processing, farm management, agricultural research, and sustainable farming practices.",
    "education": "Education opportunities in rural areas: teaching positions, vocational training, adult education programs, and educational administration roles.",
    "jobs": "Local job opportunities include healthcare workers, teachers, agricultural specialists, tourism professionals, and digital service providers.",
    "training": "Available training programs: government skill development initiatives, online courses, vocational training centers, and apprenticeship programs.",
    "default": "I specialize in rural career guidance. You can ask me about: career options, training programs, job opportunities, skill development, or specific fields like agriculture, education, or healthcare."
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip().lower()
        
        if not user_message:
            return jsonify({'response': "Please type a message so I can help you with career guidance."})
        
        # Try to get AI response
        ai_response = get_ai_response(user_message)
        
        return jsonify({'response': ai_response})
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        # Fallback to predefined responses
        fallback_response = get_fallback_response(user_message)
        return jsonify({'response': fallback_response})

def get_ai_response(user_message):
    """Get response from OpenAI API"""
    try:
        if not openai.api_key:
            raise ValueError("API key not configured")
        
        prompt = f"""
        You are a helpful career guidance assistant for rural communities. 
        Provide practical, actionable advice about careers, education, and job opportunities in rural areas.
        Focus on agriculture, local businesses, healthcare, education, and remote work opportunities.
        Keep responses clear, concise, and encouraging.
        
        User question: {user_message}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career guidance expert specializing in rural employment opportunities."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"AI API error: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Get fallback response when AI service is unavailable"""
    user_message_lower = user_message.lower()
    
    for key in FALLBACK_RESPONSES:
        if key in user_message_lower:
            return FALLBACK_RESPONSES[key]
    
    return FALLBACK_RESPONSES["default"]

if __name__ == '__main__':
    app.run(debug=True)