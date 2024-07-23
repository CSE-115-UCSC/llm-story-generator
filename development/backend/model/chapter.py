#import openai

#openai.api_key = "x"

class Chapter:
    def __init__(self, text: str, number: int = None):
        self.text = text
        self.number = number
        self.summary = ""

    def character(self, name: str):
        return self.characters[name]
    

    # # To generate a chapter using OpenAI API
    # def generate(self, prompt, max_tokens=4096):
    #     # Call OpenAI API to generate a response
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": prompt}
    #         ],
    #         max_tokens=max_tokens,
    #         n=1,
    #         stop=None,
    #         temperature=0.7,
    #         stream=True
    #     )
    #     return response

    # # To add a new chapter to the list
    # def add(self, chapter):
    #     self.chapters.append(chapter)

    # # To get all chapters, formatted without initial chapter titles
    # def get_all(self):
    #     formatted_chapters = {f"Chapter {idx + 1}": re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip() for idx, chapter in enumerate(self.chapters)}
    #     return formatted_chapters
