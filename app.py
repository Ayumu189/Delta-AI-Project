from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from markdown import markdown

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

# This function converts user dictionary to user object
#Example: {role: "", text: ""}
# # ->  types.Content(role="user", parts=[types.Part(text="What is the CO2 emission of a Toyota Prius?")]),

def converter(object):
    return types.Content(role=object["role"], parts=[types.Part(text=object["text"])])

# define function that converts a list of laptops to a list of equivalent stations
def convert_history(history): # where history=[{}, {}]
    new_history = []
    for message in history:
        new_message=converter(message)
        new_history.append(new_message)
    return new_history

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
system_message = (
            "I am doing a project on carbon footprints from different cars and I want you to be my assistant in this project. "
                "I want to gather information about carbon emission of different car brands and car models. "
                "Whenever I ask you any question about carbon emission of different models, keep you answers concise and precise. "
                "Maintan a friendly and respectful tone in your responses. Polietly correct me if I am wrong at any stage. "
                "If the model isn't specific enough, assume the average and provide emmission" 
                "DO NOT ask the user for more specific commands — just provide an answer based on the best available data. "
)
client = genai.Client(api_key=GOOGLE_API_KEY)

@app.route("/", methods=["POST", "GET"])
def index():
    if 'history' not in session:
        session['history'] = []
    if request.method == 'POST':
        #get user message from the form
        user_input=request.form["user_input"]
        chat = client.chats.create(model="gemini-2.0-flash", 
                                config=types.GenerateContentConfig(
                                system_instruction=system_message),
                                history=convert_history(session['history'])
                                )
        response = chat.send_message(user_input)
        user_message = {"role": "user", "text": user_input}
        model_message = {"role": "model", "text": response.text}
        session['history'].append(user_message) 
        session['history'].append(model_message)
        session.modified = True
        return render_template('index.html', response=markdown(response.text))
    
    return render_template('index.html', response="Hello user, input your car model to show its carbon footprint")

@app.route("/health")
def health():
    return jsonify(status="ok"),200
