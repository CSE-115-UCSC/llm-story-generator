# The llm we're using 
from openai import OpenAI

# what manages our API resources and server
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS, cross_origin
import dotenv # for env vars

# our model
from model.story import Story

app = Flask(__name__)

# CORS config
CORS(app)

dotenv.load_dotenv()
llm = OpenAI()

# Initializing the StoryManager instance
story_manager = Story()

# Route to generate a new chapter
@app.route('/chapter/<int:chapter>', methods=['GET'])
def generate_chapter(chapter: int):
    # if request.method == 'POST':
    #     data = request.json
    #     prompt = data.get('prompt')
    #     clear_previous = data.get('clear_previous', False)
    #     if not prompt:
    #         return jsonify({"error": "Prompt is required"}), 400
    #     return Response(stream_with_context(story_manager.generate_chapter_streaming(prompt, clear_previous)), content_type='text/plain')
    
    #elif request.method == 'GET':
    # def generate():
    #     yield '<p>Hello '
    #     yield escape(request.args['name'])
    #     yield '!</p>'
    # return stream_with_context(generate())
    def g(chapter):
        openai_stream = llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "who is ChatGPT in 500 words."}],
            temperature=0.1,
            stream=True,
        )
        text = ""
        for chunk in openai_stream:
            if chunk.choices[0].delta.content is not None:
                text += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
        story_manager.set_chapter(chapter, text)

    return Response(stream_with_context(g(chapter)), content_type='text/event-stream')

    
# Route to regenerate an existing chapter
@app.route('/chapter/<int:chapter>', methods=['POST'])
def regenerate_chapter(chapter: int):
    data = request.json
    prompt = data.get('prompt')
    print(prompt)
#     if not chapter_num or not prompt:
#         return jsonify({"error": "Chapter number and prompt are required"}), 400

#     return Response(stream_with_context(story_manager.regenerate_chapter(chapter_num, prompt)), content_type='text/plain')

# # Route to fetch a specific chapter
@app.route('/character', methods=['GET'])
def get_chapters():
    return "Hi"

# # Route to fetch a specific summary
# @app.route('/chapter/{number}/summary', methods=['GET'])
# def get_summaries():
#     return jsonify({"summaries": story_manager.summary.get_all()})

# # Route to fetch a specific character
# @app.route('/chapter/{number}/character', methods=['GET'])
# def get_characters():
#     return jsonify({"characteristics": story_manager.character.get_all()})

# # Route to clear data of a chapter
# @app.route('/chapter/{number}/clear', methods=['POST'])
# def clear_data():
#     story_manager.__init__()
#     return jsonify({"status": "Cleared all stored data"})

# #these might be outdated since they do all 

# # Route to fetch all chapters
# @app.route('/chapters', methods=['GET'])
# def get_chapters():
#     return jsonify({"chapters": story_manager.chapter.get_all()})

# # Route to fetch all summaries
# @app.route('/summaries', methods=['GET'])
# def get_summaries():
#     return jsonify({"summaries": story_manager.summary.get_all()})

# # Route to fetch all character characteristics
# @app.route('/characters', methods=['GET'])
# def get_characters():
#     return jsonify({"characteristics": story_manager.character.get_all()})

# # Route to clear all stored data
# @app.route('/clear', methods=['POST'])
# def clear_data():
#     story_manager.__init__()
#     return jsonify({"status": "Cleared all stored data"})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, threaded=True)