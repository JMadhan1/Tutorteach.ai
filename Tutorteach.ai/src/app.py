from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from transformers import pipeline

app = Flask(__name__)

# Load models from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
question_generator = pipeline("text2text-generation", model="t5-base")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_video', methods=['POST'])
def generate_video():
    topic = request.form['topic']
    video_url = generate_ai_video(topic)
    return jsonify({'video_url': video_url})

def generate_ai_video(topic):
    # Placeholder for video generation logic (you can use your API)
    return "https://example.com/generated_video.mp4"

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    text = request.form['text']
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return jsonify({'summary': summary[0]['summary_text']})

@app.route('/generate_questions', methods=['POST'])
def generate_questions():
    summary = request.form['summary']
    questions = question_generator(f"generate questions: {summary}")
    return jsonify({'questions': questions[0]['generated_text']})

@app.route('/assignment', methods=['GET', 'POST'])
def assignment():
    if request.method == 'POST':
        answers = request.form.getlist('answers')
        # Here, implement scoring logic and determine strengths/weaknesses
        score = calculate_score(answers)
        return render_template('score_prediction.html', score=score)
    
    summary = request.args.get('summary')
    questions = request.args.get('questions')
    return render_template('assignment.html', summary=summary, questions=questions)

def calculate_score(answers):
    # Placeholder logic for score calculation
    return len(answers)  # Return the number of answered questions as a simple score

@app.route('/score')
def score():
    return render_template('score_prediction.html')

if __name__ == '__main__':
    app.run(debug=True)
