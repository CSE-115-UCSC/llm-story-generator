class Prompt:
    def __init__(self, number: int, text: str):
        self.text = text
        self.number = number

    def chapter(self):
        return self.number
    
    def message(self, summary: str, characters: dict):
        return f"Previously on the story: {summary}\n\nCharacters and their traits:\n{characters}\n\n{self.text}"
