# The llm we're using 
from openai import OpenAI
import re
# what manages our API resources and server
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import dotenv # for env vars
import logging
# our model
from model.story import Story

app = Flask(__name__)
CORS(app) # lax CORS confif
logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()
llm = OpenAI()

# Initializing the StoryManager instance
story_manager = Story()
# #Write a story about courageous bob, silly billy martin, and weird chloe in 100 words.
# story_manager.set_chapter(1,"""Courageous Bob, Silly Billy Martin, and Weird Chloe embarked on a peculiar adventure. In the enchanted forest, Bob fearlessly led the way, his sword glinting in the moonlight. Billy tripped over roots, making Chloe giggle with her odd, snorting laugh. They stumbled upon a mysterious cave. Inside, a dragon slept on a pile of gold. Bob stepped forward, heart pounding. "We need that gold", he whispered. Billy slipped on a banana peel, waking the dragon. Chloe, with her quirky charm, sang a strange melody, calming the beast. The dragon, enchanted, let them take the gold. Together, they triumphed, united by their quirks.""")
# story_manager.chapters[1].summary = """Courageous Bob, Silly Billy Martin, and Weird Chloe embarked on an adventure in an enchanted forest. Bob led the way, Billy's clumsiness made Chloe laugh, and they found a dragon guarding gold in a cave. After Billy accidentally woke the dragon, Chloe's quirky song calmed it, allowing them to take the gold. United by their quirks, they triumphed together."""

# story_manager.set_chapter(2,"jrgihewrjngejkrngoqb;oer")
# story_manager.chapters[2].summary = "shuhwgro"

# story_manager.set_chapter(3,"jrgihewrjngejkrngoqb;oer")
# story_manager.chapters[3].summary = "shuhwgro"

# story_manager.set_chapter(4,"jrgihewrjngejkrngoqb;oer")
# story_manager.chapters[4].summary = "shuhwgro"

# story_manager.set_chapter(5,"jrgihewrjngejkrngoqb;oer")
# story_manager.chapters[5].summary = "shuhwgro"

# story_manager.set_chapter(6,"jrgihewrjngejkrngoqb;oer")
# story_manager.chapters[6].summary = "shuhwgro"

# story_manager.set_chapter(7,"jrgihewrjngejkrngoqb;oer")
# story_manager.chapters[7].summary = "shuhwgro"


# Route to generate a new chapter
@app.route('/chapter/<int:chapter_num>', methods=["GET", "POST"])
def chapter(chapter_num: int):
    # body contains a prompt, the prompt creates a chapter
    if request.method == "POST":
        # follows the OpenAI streaming tutorial.
        def g(chapter_num: int):
            data = request.json # from the POST request
            query = data.get('query') # from the POST request
            # API call
            openai_stream = llm.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}],
                temperature=0.1,
                stream=True,
            )
            # streaming
            text = ""
            for chunk in openai_stream:
                if chunk.choices[0].delta.content is not None:
                    text += chunk.choices[0].delta.content
                    yield chunk.choices[0].delta.content

            # model update
            story_manager.set_chapter(number=chapter_num, text=text)
            app.logger.info(f"Story().chapter:\n number: {story_manager.get_chapter(chapter_num).number}\n text: {story_manager.get_chapter(chapter_num).text}")
            story_manager.set_prompt(chapter_num, query)
            
            # produce the summary
            prompt = f"Please summarize the following text:\n{text}"
            chapter_summarized = llm.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.7
            ).choices[0].message.content

            # model update
            story_manager.chapters[chapter_num].summary = chapter_summarized

            app.logger.info(f"Story().summary:\n number: {story_manager.get_chapter(chapter_num).number}\n text: {story_manager.get_chapter(chapter_num).summary}")

            #produce the characters and traits
            characters = extract_characters( story_manager.chapters[chapter_num].text)
            #
            for name,traits in characters.items():  
                story_manager.set_character(name, chapter_num, traits)

            app.logger.info(f"characters {story_manager.characters}")

        return Response(stream_with_context(g(chapter_num)), content_type='text/event-stream')
    

    #get the chapter
    if request.method == "GET":
        # check if chapter exists 

        chapter_text= story_manager.get_chapter(1).text
        #
        app.logger.info(f"/chapter: {chapter_text}")
        return jsonify(chapter_text)
        
        # if(story_manager.number_chapters <= chapter_num):
        #     #print("here")
        #     return Response(status = 404)

        # #gets a chapter 
        # chapter_text= story_manager.chapter(chapter_num).text
        # #
        # app.logger.info(f"/chapter: {chapter_text}")
        # return jsonify(chapter_text)
        




# Route to regenerate an existing chapter
# @app.route('/chapter/<int:chapter>', methods=['POST'])
# def regenerate_chapter(chapter: int):
#     data = request.json
#     prompt = data.get('prompt')
#     print(prompt)
#     if not chapter_num or not prompt:
#         return jsonify({"error": "Chapter number and prompt are required"}), 400

#     return Response(stream_with_context(story_manager.regenerate_chapter(chapter_num, prompt)), content_type='text/plain')

# # Route to fetch a specific chapter  

@app.route('/characters', methods=['GET', 'PUT'])
def characters():
    if request.method == 'GET':
        # mess with the story object (our model)
        # get or set the character via story_manager
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

# Route to fetch a specific summary
@app.route('/summaries', methods=['GET'])
def summaries():
    summary_dict = story_manager.get_summaries()
    app.logger.info(f"/summaries: {summary_dict}")
    return jsonify(summary_dict)

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
@app.route('/chapters', methods=['GET'])
def chapters():
    return jsonify(story_manager.get_chapters())

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


def extract_characters(chapter_text: str):
        prompt = f"Extract the main characteristics of all the main characters from the following text:\n{chapter_text}. Each character should have only a maximum of five main characteristics. The characteristics should be written in this form - Character Name: Qualities."
        response = llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7
        ).choices[0].message 
        # spring of form character: trait, trait... .\n
        character_body = response.content
        character_lines = character_body.split('\n')
        # {character_name:[traits]}
        characters = {}

        for character_line in character_lines:
            # if the response is not in correct form
            if ':' in character_line:
                name, traits = character_line.split(':', 1)
                characters[name] = traits.split(', ')

        return characters




# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
