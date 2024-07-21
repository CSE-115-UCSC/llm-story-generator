from typing import List

# Class to handle character extraction and storage
class Character:
    def __init__(self, name: str):
        # Initializing an empty dictionary to store character traits
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
    

    # # To extract character traits from a chapter
    # def extract(self, chapter):
    #     # Prompt for extracting character traits from the text
    #     prompt = f"Extract the main characteristics of all the main characters from the following text:\n{chapter}. Each character should have only a maximum of five main characteristics. The characteristics should be written in this form - Character Name: Qualities."
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": prompt}
    #         ],
    #         max_tokens=300,
    #         n=1,
    #         stop=None,
    #         temperature=0.7
    #     ).choices[0].message['content'].strip()
        
    #     # To process the response to extract character traits
    #     lines = response.split('\n')
    #     chapter_characteristics = {}
    #     for line in lines:
    #         if ':' in line:
    #             char, characs = line.split(':', 1)
    #             char = char.strip()
    #             characs = [charac.strip() for charac in characs.split(',')]
    #             characs = list(dict.fromkeys(characs))
    #             if char and characs:
    #                 characs = [charac for charac in characs if charac]
    #                 if characs:
    #                     chapter_characteristics[char] = ', '.join(characs[:5])
    #                     if char in self.characteristics:
    #                         self.characteristics[char] = ', '.join(
    #                             list(dict.fromkeys(self.characteristics[char].split(', ') + characs))[:5]
    #                         )
    #                     else:
    #                         self.characteristics[char] = ', '.join(characs[:5])
    #     return chapter_characteristics

    # # To get all character traits
    # def get_all(self):
    #     return {char: characs for char, characs in self.characteristics.items() if characs}
