from typing import List

from backend.model.prompt import Prompt
from backend.model.chapter import Chapter
from backend.model.character import Character

class Story:
    def __init__(self, name = None):
        self.name = name
        self.chapters = [None]
        self.prompts = [None]
        self.characters = [None]
        self.number_chapters = len(self.chapters) - 1

    # return a prompt object
    def prompt(self, number: int):
        return self.prompts[number]

    # return a chapter object
    def chapter(self, number: int):
        return self.chapters[number]
    
    # return a character object
    def character(self, number: int, name: str):
        return self.characters[number][name]
    
    def set_prompt(self, number: int, message: str):
        # add a new prompt 
        p = Prompt(number, message)
        self.prompts.append(p)

    def set_chapter(self, number: int, text: str):
        # add a new chapter
        ch = Chapter(number, text)
        self.chapters.append(ch)
    
    def set_character(self, number: int, name: str, traits: List[str]):
        # add a new character to the chapter number
        char = Character(name, traits)
        self.characters[number][name] = char

    # # To generate a chapter with streaming response
    # def generate_chapter_streaming(self, prompt, clear_previous=False, max_tokens=4096):
    #     # To clear previous data if specified
    #     if clear_previous:
    #         self.chapter = Chapter()
    #         self.summary = Summary()
    #         self.character = Character()

    #     # To enhance the prompt with previous summaries and character traits
    #     enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
    #     response = self.chapter.generate(enhanced_prompt, max_tokens=max_tokens)

    #     def generate():
    #         chapter = ""
    #         for chunk in response:
    #             chunk_text = chunk['choices'][0]['delta'].get('content', '')
    #             chapter += chunk_text
    #             yield chunk_text

    #         chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
    #         self.chapter.add(chapter)

    #         self.summary.add(chapter, len(self.chapter.chapters))
    #         chapter_characteristics = self.character.extract(chapter)
    #         yield f"\n\nCharacter Characteristics (Chapter {len(self.chapter.chapters)}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

    #     return generate()

    # # To regenerate a chapter with streaming response
    # def regenerate_chapter(self, chapter_num, prompt, max_tokens=4096):
    #     if chapter_num > len(self.chapter.chapters):
    #         return {"error": "Chapter number out of range."}

    #     self.chapter.chapters = self.chapter.chapters[:chapter_num - 1]
    #     self.summary.summaries = self.summary.summaries[:chapter_num - 1]
    #     self.character.characteristics = {k: v for k, v in self.character.characteristics.items() if k.startswith(f"Chapter {chapter_num - 1}")}

    #     enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
    #     response = self.chapter.generate(enhanced_prompt, max_tokens=max_tokens)

    #     def regenerate():
    #         chapter = ""
    #         for chunk in response:
    #             chunk_text = chunk['choices'][0]['delta'].get('content', '')
    #             chapter += chunk_text
    #             yield chunk_text

    #         chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
    #         self.chapter.add(chapter)

    #         self.summary.add(chapter, chapter_num)
    #         chapter_characteristics = self.character.extract(chapter)
    #         yield f"\n\nCharacter Characteristics (Chapter {chapter_num}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

    #     return regenerate()
