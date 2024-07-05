import openai
from flask import Flask, request, jsonify
import json

openai.api_key = ""

app = Flask(__name__)

chapters = []
summaries = []
characteristics = {}

def call_chatgpt(prompt, max_tokens=2048):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message['content'].strip()

def summarize_text(text):
    prompt = f"Please summarize the following text:\n{text}"
    summary = call_chatgpt(prompt, max_tokens=150)
    return summary

def extract_characteristics(chapter):
    prompt = f"Extract the characteristics of all the main characters from the following text:\n{chapter}. The characterstics should be written in ths form - Character Name: Qualities."
    response = call_chatgpt(prompt, max_tokens=150)
    lines = response.split('\n')
    for line in lines:
        if ':' in line:
            char, characs = line.split(':', 1)
            char = char.strip()
            characs = characs.strip()
            if char in characteristics:
                characteristics[char] += f", {characs}"
            else:
                characteristics[char] = characs

@app.route('/generate_chapter', methods=['POST'])
def generate_chapter():
    data = request.json
    prompt = data.get('prompt')
    clear_previous = data.get('clear_previous', False)

    if clear_previous:
        chapters.clear()
        summaries.clear()
        characteristics.clear()

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    chapter = call_chatgpt(prompt)
    chapters.append(chapter)

    summary = summarize_text(chapter)
    summaries.append(summary)

    extract_characteristics(chapter)

    return jsonify({"chapter": chapter, "summary": summary, "characteristics": characteristics})

@app.route('/chapters', methods=['GET'])
def get_chapters():
    formatted_chapters = {}
    for idx, chapter in enumerate(chapters, 1):
        chapter_title = f"Chapter {idx}: {chapter.splitlines()[0]}"
        formatted_chapters[chapter_title] = chapter
    return jsonify({"chapters": formatted_chapters})

@app.route('/summaries', methods=['GET'])
def get_summaries():
    return jsonify({"summaries": summaries})

@app.route('/characters', methods=['GET'])
def get_characters():
    return jsonify({"characteristics": characteristics})

@app.route('/clear', methods=['POST'])
def clear_data():
    global chapters, summaries, characteristics
    chapters = []
    summaries = []
    characteristics = {}
    return jsonify({"status": "Cleared all stored data"})

if __name__ == '__main__':
    app.run(debug=True)
