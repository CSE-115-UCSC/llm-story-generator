# Import Statements
import openai
from flask import Flask, request, jsonify, Response, stream_with_context
import re
import firebase_admin
from firebase_admin import credentials, db

# To initialize Firebase Admin SDK with the provided credentials
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://llm-story-generator-default-rtdb.firebaseio.com/'
})

# To set OpenAI API key for making requests to the OpenAI API
openai.api_key = "x"

# To initialize Flask app
app = Flask(__name__)

# Class to handle prompt enhancement
class Prompt:
    @staticmethod
    def enhance(prompt, summaries, characteristics):
        # If summaries are available, append the latest summary and character traits to the prompt
        if summaries:
            prev_char_traits = "\n".join([f"{char}: {traits}" for char, traits in characteristics.items()])
            prompt = f"Previously on the story: {summaries[-1].split(': ', 1)[-1]}\n\nCharacters and their traits:\n{prev_char_traits}\n\n{prompt}"
        # To enhance the prompt with additional instructions
        enhanced_prompt = (
            "Start the chapter with a proper introduction, setting the scene, and introducing the main characters. "
            "Include vivid descriptions of the environment, emotions, and actions to make the story detailed and immersive. "
            "Ensure the chapter is more than 1000 words."
            f"\n\n{prompt}"
        )
        return enhanced_prompt

# Class to handle chapters
class Chapter:
    def __init__(self):
        self.chapters = []

    # To generate chapter using OpenAI's API
    def generate(self, prompt, max_tokens=4096):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
            stream=True
        )
        return response

    # To add a chapter to the list
    def add(self, chapter):
        self.chapters.append(chapter)

    # To get all chapters
    def get_all(self):
        return self.chapters

    # To regenerate chapters up to a specified number
    def regenerate(self, chapter_num):
        self.chapters = self.chapters[:chapter_num - 1]

# Class to handle summaries
class Summary:
    def __init__(self):
        self.summaries = []

    # To add a summary to the list
    def add(self, chapter, chapter_num):
        summary = self.summarize_text(chapter)
        chapter_title = f"Chapter {chapter_num}: {chapter.splitlines()[0]}"
        formatted_summary = f"{chapter_title}\n{summary}"
        self.summaries.append(formatted_summary)

    # To get all summaries
    def get_all(self):
        return self.summaries

    # To regenerate summaries up to a specified number
    def regenerate(self, chapter_num):
        self.summaries = self.summaries[:chapter_num - 1]

    # To summarize a given text using OpenAI's API
    @staticmethod
    def summarize_text(text):
        prompt = f"Please summarize the following text:\n{text}"
        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7
        ).choices[0].message['content'].strip()
        return summary

# Class to handle character extraction and characteristics
class Character:
    def __init__(self):
        self.characteristics = {}

    # To extract main characteristics from a chapter using OpenAI's API
    def extract(self, chapter):
        prompt = f"Extract the main characteristics of all the main characters from the following text:\n{chapter}. Each character should have only a maximum of five main characteristics. The characteristics should be written in this form - Character Name: Qualities."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7
        ).choices[0].message['content'].strip()
        
        # To parse the response and update characteristics
        lines = response.split('\n')
        chapter_characteristics = {}
        for line in lines:
            if ':' in line:
                char, characs = line.split(':', 1)
                char = char.strip()
                characs = [charac.strip() for charac in characs.split(',')]
                characs = list(dict.fromkeys(characs))
                if char and characs:
                    characs = [charac for charac in characs if charac]
                    if characs:
                        chapter_characteristics[char] = ', '.join(characs[:5])
                        if char in self.characteristics:
                            self.characteristics[char] = ', '.join(
                                list(dict.fromkeys(self.characteristics[char].split(', ') + characs))[:5]
                            )
                        else:
                            self.characteristics[char] = ', '.join(characs[:5])
        return chapter_characteristics

    # To get all characteristics
    def get_all(self):
        return self.characteristics

    # To regenerate characteristics up to a specified number
    def regenerate(self, chapter_num):
        self.characteristics = {}

# Class to manage the story, including chapters, summaries, and characteristics
class StoryManager:
    def __init__(self):
        self.chapter = Chapter()
        self.summary = Summary()
        self.character = Character()

    # To generate a chapter with streaming response
    def generate_chapter_streaming(self, book_num, prompt, clear_previous=False):
        ref = db.reference(f'Book_{book_num}')

        if clear_previous:
            ref.child('chapters').delete()

            self.chapter = Chapter()
            self.summary = Summary()
            self.character = Character()

        enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
        response = self.chapter.generate(enhanced_prompt)

        def generate():
            chapter = ""
            for chunk in response:
                chunk_text = chunk['choices'][0]['delta'].get('content', '')
                chapter += chunk_text
                yield chunk_text

            chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
            self.chapter.add(chapter)
            chapter_num = len(self.chapter.chapters)
            chapter_key = f'chapter_{chapter_num}'

            summary = self.summary.summarize_text(chapter)
            self.summary.add(chapter, chapter_num)

            chapter_characteristics = self.character.extract(chapter)
            self.character.get_all()

            chapter_data = {
                'chapter_text': chapter,
                'summary': summary,
                'characteristics': chapter_characteristics,
                'prompt': prompt
            }

            ref.child('chapters').child(chapter_key).set(chapter_data)
            yield f"\n\nCharacter Characteristics (Chapter {chapter_num}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

        return generate()

    # To regenerate a chapter with streaming response
    def regenerate_chapter_streaming(self, book_num, chapter_num):
        self.chapter.regenerate(chapter_num)
        self.summary.regenerate(chapter_num)
        self.character.regenerate(chapter_num)
        
        ref = db.reference(f'Book_{book_num}/chapters/chapter_{chapter_num}')
        prompt = ref.child('prompt').get()

        enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
        response = self.chapter.generate(enhanced_prompt)

        def generate():
            chapter = ""
            for chunk in response:
                chunk_text = chunk['choices'][0]['delta'].get('content', '')
                chapter += chunk_text
                yield chunk_text

            chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
            self.chapter.add(chapter)
            chapter_key = f'chapter_{chapter_num}'

            summary = self.summary.summarize_text(chapter)
            self.summary.add(chapter, chapter_num)

            chapter_characteristics = self.character.extract(chapter)
            self.character.get_all()

            chapter_data = {
                'chapter_text': chapter,
                'summary': summary,
                'characteristics': chapter_characteristics,
                'prompt': prompt
            }

            ref.set(chapter_data)
            yield f"\n\nCharacter Characteristics (Chapter {chapter_num}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

        return generate()

# To initialize StoryManager
story_manager = StoryManager()

# Route to generate a chapter
@app.route('/generate_chapter', methods=['POST'])
def generate_chapter():
    data = request.json
    book_num = data.get('book_num')
    prompt = data.get('prompt')
    clear_previous = data.get('clear_previous', False)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    return Response(stream_with_context(story_manager.generate_chapter_streaming(book_num, prompt, clear_previous)), content_type='text/plain')

# Route to regenerate a chapter
@app.route('/regenerate_chapter', methods=['POST'])
def regenerate_chapter():
    data = request.json
    book_num = data.get('book_num')
    chapter_num = data.get('chapter_num')

    if not chapter_num or not isinstance(chapter_num, int) or chapter_num < 1:
        return jsonify({"error": "Valid chapter number is required"}), 400

    return Response(stream_with_context(story_manager.regenerate_chapter_streaming(book_num, chapter_num)), content_type='text/plain')

# Route to get all chapters of a book
@app.route('/books/<book_num>/chapters', methods=['GET'])
def get_chapters(book_num):
    ref = db.reference(f'Book_{book_num}/chapters')
    return jsonify({"chapters": ref.get()})

# Route to get all summaries of a book
@app.route('/books/<book_num>/summaries', methods=['GET'])
def get_summaries(book_num):
    ref = db.reference(f'Book_{book_num}/chapters')
    summaries = []
    chapters = ref.get()
    for chapter_key, chapter_data in chapters.items():
        summary = chapter_data.get('summary', 'No summary available')
        summaries.append({chapter_key: summary})
    return jsonify({"summaries": summaries})

# Route to get all character characteristics of a book
@app.route('/books/<book_num>/characters', methods=['GET'])
def get_characters(book_num):
    ref = db.reference(f'Book_{book_num}/characteristics')
    return jsonify({"characteristics": ref.get()})

# Route to clear all stored data
@app.route('/clear', methods=['POST'])
def clear_data():
    story_manager.__init__()
    ref = db.reference()
    ref.child('chapters').delete()
    ref.child('summaries').delete()
    ref.child('characteristics').delete()
    ref.child('prompts').delete()
    
    return jsonify({"status": "Cleared all stored data"})

# To run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
