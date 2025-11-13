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
    "default": "I specialize in rural career guidance. You can ask me about: career options, training programs, job opportunities, skill development, or specific fields like agriculture, education, or healthcare.",
    "career": "You can ask me about careers, jobs, courses, skills or anything.",
    "agriculture": "Agriculture careers: farming, organic farming, agritech, food processing.",
    "education": "Education careers: teacher, instructor, trainer, counselor.",
    "jobs": "Local jobs include teaching, healthcare, agri-support, digital services.",
    "training": "Training includes ITI, PMKVY, online courses, apprenticeships.",
    "10th": "10th ke baad Science, Commerce, Arts, ITI, Polytechnic options hain.",
    "after 10th": "After 10th you can choose Science/Commerce/Arts/ITI/Polytechnic.",
    "12th": "12th ke baad engineering, medical, BSc, BCom, BA, nursing, diploma etc.",
    "after 12th": "After 12th choose degree, diploma, govt job prep or skill training.",
    "engineering": "Engineering branches include CSE, Mechanical, Civil, IT and more.",
    "btech": "BTech popular branches: CSE, IT, AI, Mechanical, Civil.",
    "ias": "IAS ke liye UPSC CSE exam clear karna padta hai.",
    "ips": "IPS ke liye UPSC exam + physical fitness zaroori hai.",
    "upsc": "UPSC prep includes NCERTs, reading, writing practice, current affairs.",
    "computer": "Computer field me jobs: coding, data entry, graphics, web dev.",
    "digital": "Digital jobs: freelancing, marketing, content creation.",
    "skills": "In-demand skills: coding, English speaking, graphic design.",
    "hinglish": "Aap mujhse Hinglish me bhi puch sakte ho!",

    "software engineer": "Software engineer banne ke liye coding, BTech ya online skills seekho.",
    "software engineer kaise bane": "Software engineer banne ke liye Python/Java, DSA, projects aur internships chahiye.",
    "coder": "Coder banne ke liye Python ya Java se start karo.",
    "programming": "Programming languages: Python, Java, C++, JavaScript.",
    "learn coding": "Coding seekhne ke liye daily practice aur projects karna important hai.",
    "ssc": "SSC me CHSL, CGL popular exams hain.",
    "bank job": "Bank jobs ke liye IBPS PO, Clerk, RRB exams hoti hain.",
    "police job": "Police me state constable, SI exams hoti hain.",
    "paramedical": "Paramedical courses: lab technician, radiology, OT technician.",
    "hospital job": "Hospital jobs me nurse, technician, receptionist, ward assistant.",
    "job": "Aap kis type ki job chahte ho?",
    "iti": "ITI me electrician, fitter, welder, COPA popular trades hain.",
    "polytechnic": "Polytechnic diploma 3 years ka hota hai engineering branches me.",
    "diploma": "Diploma mechanical, civil, electrical, computer me hota hai.",
    "skill courses": "Short skills: computer, tally, English speaking, design.",
    "agriculture jobs": "Agriculture jobs: Krishi sevak, farm manager, agri-officer.",
    "farming": "Farming me organic, dairy, poultry, fish farming options hain.",
    "dairy farming": "Dairy farming me cows/buffalo aur milk processing hota hai.",
    "poultry": "Poultry me chicken farming profitable ho sakta hai.",
    "goat farming": "Goat farming low investment business hai.",
    "beekeeping": "Beekeeping profitable rural business hai.",
    "food processing": "Food processing me packaging, dehydration, pickles, spices.",

    "business": "Small business ideas: dairy, poultry, shop, online services.",
    "startup": "Startup ke liye idea, execution aur problem solving chahiye.",
    "small business": "Small businesses me kirana, repair shop, tailoring, tuition.",
    "shop ideas": "Shop ideas: mobile repair, stationery, grocery, photocopy.",
    "online business": "Online business me e-commerce, reselling, services enter hota hai.",

    "english": "English improve karne ke liye reading aur speaking practice karo.",
    "communication skills": "Communication skills jobs me bahut important hoti hain.",
    "resume": "Resume simple rakho: skills, education, projects likho.",
    "interview": "Interview me confidence, clear answers aur honesty important hai.",
    "motivation": "Hard work + skill development = success.",
    "computer course": "Computer courses: basics, tally, typing, programming.",
    "tally": "Tally accounting ke liye important software hai."
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