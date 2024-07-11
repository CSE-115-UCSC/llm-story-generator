# Import Statements
import openai
from flask import Flask, request, jsonify, Response, stream_with_context

import story

app = Flask(__name__)

# Initializing the StoryManager instance
story_manager = story.StoryManager()

# Route to generate a new chapter
@app.route('/generate_chapter', methods=['POST'])
def generate_chapter():
    data = request.json
    prompt = data.get('prompt')
    clear_previous = data.get('clear_previous', False)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    return Response(stream_with_context(story_manager.generate_chapter_streaming(prompt, clear_previous)), content_type='text/plain')

# Route to regenerate an existing chapter
@app.route('/regenerate_chapter', methods=['POST'])
def regenerate_chapter():
    data = request.json
    chapter_num = data.get('chapter_num')
    prompt = data.get('prompt')

    if not chapter_num or not prompt:
        return jsonify({"error": "Chapter number and prompt are required"}), 400

    return Response(stream_with_context(story_manager.regenerate_chapter(chapter_num, prompt)), content_type='text/plain')

# Route to fetch all chapters
@app.route('/chapters', methods=['GET'])
def get_chapters():
    return jsonify({"chapters": story_manager.chapter.get_all()})

# Route to fetch all summaries
@app.route('/summaries', methods=['GET'])
def get_summaries():
    return jsonify({"summaries": story_manager.summary.get_all()})

# Route to fetch all character characteristics
@app.route('/characters', methods=['GET'])
def get_characters():
    return jsonify({"characteristics": story_manager.character.get_all()})

# Route to clear all stored data
@app.route('/clear', methods=['POST'])
def clear_data():
    story_manager.__init__()
    return jsonify({"status": "Cleared all stored data"})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
