# The llm we're using 
from openai import OpenAI
# what manages our API resources and server
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import logging

# our model
from model.story import Story
from llm import LLM

# Create the Flask APP and set Cors headers
app = Flask(__name__)
CORS(app)

# OpenAI expects an environmental variable named OPENAI_API_KEY=<sk-yourAPIkey>
llm = LLM()

# This is a spy for logging what happes in the backend. Use app.logger.info(), and NEVER print()
logging.basicConfig(level=logging.INFO)

# Initializing the StoryManager instance (Singleton Pattern)
story_manager = Story()

'''API Routes'''

# Route to fetch a specific summary
@app.route('/summaries', methods=['GET'])
def summaries():
    summary_dict = story_manager.get_summaries()
    app.logger.info(f"/summaries: {summary_dict}")
    return jsonify(summary_dict)

# # Route to fetch all chapters
@app.route('/chapters', methods=['GET'])
def chapters():
    return jsonify(story_manager.get_chapters())

@app.route('/chapter/<int:chapter_num>', methods=["GET", "POST"])
def chapter(chapter_num: int):
    if request.method == "GET":
        chapter_text= story_manager.get_chapter(1).text
        app.logger.info(f"/chapter: {chapter_text}")
        return jsonify(chapter_text)
        
    # body contains a prompt, the prompt creates a chapter
    elif request.method == "POST":

        '''This is a generator for streaming data to the client. It also streams data from the llm.'''
        def g(chapter_num: int):
            # the POST from the client must have a {"query": prompt} key-value pair in the data header
            data = request.json
            query = data.get('query')
            
            # llm.write_chapter is a generator that streams data from the llm so 
            # we can ourselves stream it to the client so they can have near 
            # immedaite feedback.
            chapter = ""
            for chunk in llm.write_chapter(query):
                chapter += chunk
                yield chunk

            # add the chapter and the prompt to the model and log.
            story_manager.set_chapter(number=chapter_num, text=chapter)
            story_manager.set_prompt(chapter_num, query)
            app.logger.info(f"Story().chapter:\n number: {story_manager.get_chapter(chapter_num).number}\n text: {story_manager.get_chapter(chapter_num).text}")
            app.logger.info(f"Story().prompt:\n number: {story_manager.get_prompt(chapter_num).number}\n text: {story_manager.get_prompt(chapter_num).text}")
            
            # produce the summary and add the chapter to the model.
            summary = llm.summarize(chapter)
            story_manager.chapters[chapter_num].summary = summary
            app.logger.info(f"Story().summary:\n number: {story_manager.get_chapter(chapter_num).number}\n text: {story_manager.get_chapter(chapter_num).summary}")

            # produce the characters and traits and then
            # update the characters in the model.
            characters = llm.identify_characters_and_traits( story_manager.chapters[chapter_num].text)
            for name,traits in characters.items():  
                story_manager.set_character(name, chapter_num, traits)
            app.logger.info(f"characters {story_manager.characters}")

        return Response(stream_with_context(g(chapter_num)), content_type='text/event-stream')
    
    return Response(status=404)

@app.route('/characters', methods=['GET', 'PUT'])
def characters():
    if request.method == 'GET':
        return jsonify(story_manager.get_characters())
    elif request.method == 'PUT':
        app.logger.info(f"PUT /characters {request.data}")
    else:
        return Response(status = 404)

@app.route('/characters/<string:character>', methods=['GET'])
def character(character: str):
    if request.method == 'GET':
        characters = story_manager.get_characters()
        if character in characters:
            return jsonify(story_manager.get_characters()[character])
        else:
            return Response(status = 404)
    elif request.method == 'PUT':
        app.logger.info(f"PUT /characters {request.data}")
    else:
        return Response(status = 404)

@app.route('/characters/<string:character>/<int:chapter>', methods=['GET'])
def character_chapter_traits(character: str, chapter: int):
    if request.method == 'GET':
        # mess with the story object (our model)
        # get or set the character via story_manager
        return jsonify(story_manager.get_characters()[character][chapter])
    elif request.method == 'PUT':
        app.logger.info(f"PUT /characters {request.data}")
    else:
        return Response(status = 404)


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
