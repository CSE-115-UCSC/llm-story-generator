from typing import List

class Character:
    def __init__(self, name: str):
        # chapters are key, value pairs, where the key is the chapter number (int), and the value is a list of traits ['', '', '']
        # example: { 1: ["timid", "neurotic", "shell-shocked"], 42: ["courageous", "hopefult", "excited"]}
        self.chapters = {}
        self.name = name

    def set_traits(self, chapter_number: int, traits: List[str]):
        self.chapters[chapter_number] = traits

    def get_traits(self):
        return self.chapters
    
    def get_trait(self,chapter_number):
        return self.chapters[chapter_number]

    def name(self):
        return self.name
    