class Chapter:
    def __init__(self, text: str, number: int = None):
        self.text = text
        self.number = number
        self.summary = ""
        self.prompt = ""

    def character(self, name: str):
        return self.characters[name]
    