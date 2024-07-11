# Import Statements
import openai
from flask import Flask, request, jsonify, Response, stream_with_context
import re

# OpenAI API key
openai.api_key = "x"

# Initializing the Flask application
app = Flask(__name__)

# Class to handle prompt enhancement
class Prompt:
    @staticmethod
    def enhance(prompt, summaries, characteristics):
        # If there are summaries available, enhance the prompt with previous chapter's summary and character traits
        if summaries:
            # To compile the previous character traits
            prev_char_traits = "\n".join([f"{char}: {traits}" for char, traits in characteristics.items()])
            # To enhance the prompt with previous chapter's summary and character traits
            prompt = f"Previously on the story: {summaries[-1].split(': ', 1)[-1]}\n\nCharacters and their traits:\n{prev_char_traits}\n\n{prompt}"
        
        # To further enhance the prompt with additional instructions for detailed and immersive story generation
        enhanced_prompt = (
            "Start the chapter with a proper introduction, setting the scene, and introducing the main characters. "
            "Include vivid descriptions of the environment, emotions, and actions to make the story detailed and immersive. "
            "Ensure the chapter is more than 1000 words."
            f"\n\n{prompt}"
        )
        return enhanced_prompt

# Class to handle chapter operations
class Chapter:
    def __init__(self):
        # Initializing an empty list to store chapters
        self.chapters = []

    # To generate a chapter using OpenAI API
    def generate(self, prompt, max_tokens=4096):
        # Call OpenAI API to generate a response
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

    # To add a new chapter to the list
    def add(self, chapter):
        self.chapters.append(chapter)

    # To get all chapters, formatted without initial chapter titles
    def get_all(self):
        formatted_chapters = {f"Chapter {idx + 1}": re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip() for idx, chapter in enumerate(self.chapters)}
        return formatted_chapters

# Class to handle summaries
class Summary:
    def __init__(self):
        # Initializing an empty list to store summaries
        self.summaries = []

    # To add a summary of a chapter
    def add(self, chapter, chapter_num):
        # To summarize the chapter text
        summary = self.summarize_text(chapter)
        # To create a formatted summary with the chapter title
        chapter_title = f"Chapter {chapter_num}: {chapter.splitlines()[0]}"
        formatted_summary = f"{chapter_title}\n{summary}"
        self.summaries.append(formatted_summary)

    # To get all summaries
    def get_all(self):
        formatted_summaries = []
        for idx, summary in enumerate(self.summaries):
            # To format the summaries without initial chapter titles
            chapter_title = f"Chapter {idx + 1}"
            formatted_summary = re.sub(r'Chapter \d+: .*?(\n|$)', '', summary).strip()
            formatted_summaries.append(f"Chapter {idx + 1}:\n{formatted_summary}")
        return formatted_summaries

    # Static method to summarize a given text using OpenAI API
    @staticmethod
    def summarize_text(text):
        # Prompt for summarizing the text
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

# Class to handle character extraction and storage
class Character:
    def __init__(self):
        # Initializing an empty dictionary to store character traits
        self.characteristics = {}

    # To extract character traits from a chapter
    def extract(self, chapter):
        # Prompt for extracting character traits from the text
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
        
        # To process the response to extract character traits
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

    # To get all character traits
    def get_all(self):
        return {char: characs for char, characs in self.characteristics.items() if characs}

# Class to manage the overall story including chapters, summaries, and characters
class StoryManager:
    def __init__(self):
        # Initializing instances for Chapter, Summary, and Character management
        self.chapter = Chapter()
        self.summary = Summary()
        self.character = Character()

    # To generate a chapter with streaming response
    def generate_chapter_streaming(self, prompt, clear_previous=False, max_tokens=4096):
        # To clear previous data if specified
        if clear_previous:
            self.chapter = Chapter()
            self.summary = Summary()
            self.character = Character()

        # To enhance the prompt with previous summaries and character traits
        enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
        response = self.chapter.generate(enhanced_prompt, max_tokens=max_tokens)

        def generate():
            chapter = ""
            for chunk in response:
                chunk_text = chunk['choices'][0]['delta'].get('content', '')
                chapter += chunk_text
                yield chunk_text

            chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
            self.chapter.add(chapter)

            self.summary.add(chapter, len(self.chapter.chapters))
            chapter_characteristics = self.character.extract(chapter)
            yield f"\n\nCharacter Characteristics (Chapter {len(self.chapter.chapters)}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

        return generate()

    # To regenerate a chapter with streaming response
    def regenerate_chapter(self, chapter_num, prompt, max_tokens=4096):
        if chapter_num > len(self.chapter.chapters):
            return {"error": "Chapter number out of range."}

        self.chapter.chapters = self.chapter.chapters[:chapter_num - 1]
        self.summary.summaries = self.summary.summaries[:chapter_num - 1]
        self.character.characteristics = {k: v for k, v in self.character.characteristics.items() if k.startswith(f"Chapter {chapter_num - 1}")}

        enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
        response = self.chapter.generate(enhanced_prompt, max_tokens=max_tokens)

        def regenerate():
            chapter = ""
            for chunk in response:
                chunk_text = chunk['choices'][0]['delta'].get('content', '')
                chapter += chunk_text
                yield chunk_text

            chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
            self.chapter.add(chapter)

            self.summary.add(chapter, chapter_num)
            chapter_characteristics = self.character.extract(chapter)
            yield f"\n\nCharacter Characteristics (Chapter {chapter_num}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

        return regenerate()

# Initializing the StoryManager instance
story_manager = StoryManager()

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
