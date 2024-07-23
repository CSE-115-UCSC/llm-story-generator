# Class to handle prompt enhancement
class Prompt:
    def __init__(self, number: int, text: str):
        self.user_text = text
        self.number = number

    def text(self):
        return self.text
    
    def chapter(self):
        return self.number
    
    def message(self, summary: str, characters: dict):
        return f"Previously on the story: {summary}\n\nCharacters and their traits:\n{characters}\n\n{self.user_text}"

    # @staticmethod
    # def enhance(prompt, summaries, characteristics):
    #     # If there are summaries available, enhance the prompt with previous chapter's summary and character traits
    #     if summaries:
    #         # To compile the previous character traits
    #         prev_char_traits = "\n".join([f"{char}: {traits}" for char, traits in characteristics.items()])
    #         # To enhance the prompt with previous chapter's summary and character traits
    #         prompt = f"Previously on the story: {summaries[-1].split(': ', 1)[-1]}\n\nCharacters and their traits:\n{prev_char_traits}\n\n{prompt}"
        
    #     # To further enhance the prompt with additional instructions for detailed and immersive story generation
    #     enhanced_prompt = (
    #         "Start the chapter with a proper introduction, setting the scene, and introducing the main characters. "
    #         "Include vivid descriptions of the environment, emotions, and actions to make the story detailed and immersive. "
    #         "Ensure the chapter is more than 1000 words."
    #         f"\n\n{prompt}"
    #     )
    #     return enhanced_prompt