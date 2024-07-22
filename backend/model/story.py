from typing import List

from model.prompt import Prompt
from model.chapter import Chapter
from model.character import Character

class Story:
    def __init__(self, name = None):
        self.name = name
        self.chapters = [Chapter(text="", number=0)]
        self.prompts = [None]
        self.characters = {}
        self.number_chapters = len(self.chapters)

    # return a prompt object
    def get_prompt(self, number: int):
        return self.prompts[number]

    # return a chapter object
    def get_chapter(self, number: int):
        return self.chapters[number]
    
    #return all chapters
    def get_chapters(self):
        if len(self.chapters)>0:
            return [chapter.text for chapter in self.chapters[1:]]
        else:
            return []

    def get_summaries(self):
        sum_dict = {}
        for chapter in self.chapters[1:]:
            sum_dict[chapter.number] = chapter.summary
        return sum_dict
    
    # return a character object
    def get_character(self, name: str):
        return self.characters[name]

    def get_characters(self):
        character_dict = {}

        for name,character in self.characters.items():
            character_dict[name] = character.get_traits()

        return character_dict


    def set_prompt(self, number: int, message: str):
        # add a new prompt
        p = Prompt(number, message)
        self.prompts.append(p)

    def set_chapter(self, number: int, text: str):
        # add a new chapter
        ch = Chapter(number=number, text=text)
        self.chapters.append(ch)
    
    def set_character(self, name: str, chapter_number: int, traits: List[str]):
        #check if character exists 
        if name in self.characters:
            character_update = self.characters[name] 
        else:
            character_update = Character(name)

        character_update.set_traits(chapter_number, traits)

        self.characters[name]=character_update



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
