import dotenv
from openai import OpenAI

"""
Interface for Large Language Models

The current supported LLM option is OpenAI. This API interface is called by our
RESTful API server. This class also contains the prompts that we researched produced the 
best results.
"""
class LLM():
    def __init__(self):
        dotenv.load_dotenv()
        self.llm = OpenAI()

    # This function must always stream chunks of text via generator function to enable
    # our RESTful API to stream data. This is so that our RESTful API clients can get 
    # immedaite feedback without waiting 3 seconds for the texxt to generate. 
    def write_chapter(self, query):
        openai_stream = self.llm.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            temperature=0.1,
            stream=True,
        )
        for chunk in openai_stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def identify_characters_and_traits(self, chapter_text: str):
        prompt = f"Extract the main characteristics of all the main characters from the following text:\n{chapter_text}. Each character should have only a maximum of five main characteristics. The characteristics should be written in this form - Character Name: Qualities."
        response = self.llm.chat.completions.create(
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
        character_body = response.content
        character_lines = character_body.split('\n')
        
        characters = {} # {character_name:[traits]}
        for character_line in character_lines:
            if ':' in character_line: # sometimes llms don't give data like "Character: trait1, trait2, trait3.""
                name, traits = character_line.split(':', 1)
                characters[name] = traits.split(', ')

        return characters

    def summarize(self, chapter_content: str):
        prompt = f"Please summarize the following text:\n{chapter_content}"
        summary = self.llm.chat.completions.create(
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

        return summary
