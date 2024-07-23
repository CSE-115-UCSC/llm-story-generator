from typing import List

from model.prompt import Prompt
from model.chapter import Chapter
from model.character import Character

''' STORY OBJECT SINGLETON

Story<object> is a overarching class meant as an interface to models of stories. 
The RESTful API should use a single instance of this class per story. Any modification
to the model, like creating chapters, modifying character traits, etc should be accessed
via an instance of the Story object.

ONLY ONE STORY ALLOWED FOR RELEASE 1.0

'''
class Story:
    def __init__(self, name = None):
        self.name = name
        self.chapters = [Chapter(text="", number=0)] # list of Chapter<object>s
        self.prompts = [Prompt(0, "")] # list of Prompt<object>s
        self.characters = {} # list of Character<object>s
        self.number_chapters = len(self.chapters) # total number of chapters in the story.

    '''Getters for Objects themselves'''
    # return a prompt object
    def get_prompt(self, number: int):
        return self.prompts[number]

    # return a chapter object
    def get_chapter(self, number: int):
        return self.chapters[number]
    
     # return a character object
    def get_character(self, name: str):
        return self.characters[name]
    
    '''Getters for the Object text like character traits, chapter summaries, etc. USED BY OUR RESTFUL API!'''
    # return a list of all Chapter object TEXT!! That's the chapter content. 
    def get_chapters(self):
        if len(self.chapters)>0:
            return [chapter.text for chapter in self.chapters[1:]]
        else:
            return []

    # return a list of all Chapter object SUMMARIES!!
    def get_summaries(self):
        sum_dict = {}
        for chapter in self.chapters[1:]:
            sum_dict[chapter.number] = chapter.summary
        return sum_dict

    def get_characters(self):
        character_dict = {}
        for name,character in self.characters.items():
            character_dict[name] = character.get_traits()
        return character_dict

    '''Setters for Objects text like character traits, chapter summaries, etc. TODO: USE BY OUR RESTFUL API
    These are for POST and PUT'''
    def set_prompt(self, number: int, message: str):
        # add a new prompt
        p = Prompt(number, message)
        self.prompts.append(p)

    def set_chapter(self, number: int, text: str):
        # add a new chapter
        ch = Chapter(number=number, text=text)
        self.chapters.append(ch)
    
    # Can handle POST and PUT because we check for a character of the same name to modify before creating 
    # a new character. 
    # CANNOT HANDLE MANY CHARACTERS WITH THE SAME NAME! ("Billy" vs "Billy Jr" is fine, though.)
    def set_character(self, name: str, chapter_number: int, traits: List[str]):
        #check if character exists
        if name in self.characters:
            character_update = self.characters[name] 
        else:
            character_update = Character(name)
        character_update.set_traits(chapter_number, traits)
        self.characters[name]=character_update
