# Class to manage the overall story including chapters, summaries, and characters
class StoryManager:
    def __init__(self):
        # Initializing instances for Chapter, Summary, and Character management
        self.chapter = Chapter()
        self.summary = Summary()
        self.character = Character()

    # To generate a chapter with streaming response
    def generate_chapter_streaming(self, prompt, clear_previous=False, max_tokens=4096):
        # To clear previous data if specified
        if clear_previous:
            self.chapter = Chapter()
            self.summary = Summary()
            self.character = Character()

        # To enhance the prompt with previous summaries and character traits
        enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
        response = self.chapter.generate(enhanced_prompt, max_tokens=max_tokens)

        def generate():
            chapter = ""
            for chunk in response:
                chunk_text = chunk['choices'][0]['delta'].get('content', '')
                chapter += chunk_text
                yield chunk_text

            chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
            self.chapter.add(chapter)

            self.summary.add(chapter, len(self.chapter.chapters))
            chapter_characteristics = self.character.extract(chapter)
            yield f"\n\nCharacter Characteristics (Chapter {len(self.chapter.chapters)}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

        return generate()

    # To regenerate a chapter with streaming response
    def regenerate_chapter(self, chapter_num, prompt, max_tokens=4096):
        if chapter_num > len(self.chapter.chapters):
            return {"error": "Chapter number out of range."}

        self.chapter.chapters = self.chapter.chapters[:chapter_num - 1]
        self.summary.summaries = self.summary.summaries[:chapter_num - 1]
        self.character.characteristics = {k: v for k, v in self.character.characteristics.items() if k.startswith(f"Chapter {chapter_num - 1}")}

        enhanced_prompt = Prompt.enhance(prompt, self.summary.summaries, self.character.characteristics)
        response = self.chapter.generate(enhanced_prompt, max_tokens=max_tokens)

        def regenerate():
            chapter = ""
            for chunk in response:
                chunk_text = chunk['choices'][0]['delta'].get('content', '')
                chapter += chunk_text
                yield chunk_text

            chapter = re.sub(r'Chapter \d+: .*?(\n|$)', '', chapter).strip()
            self.chapter.add(chapter)

            self.summary.add(chapter, chapter_num)
            chapter_characteristics = self.character.extract(chapter)
            yield f"\n\nCharacter Characteristics (Chapter {chapter_num}):\n" + "\n".join([f"{char}: {traits}" for char, traits in chapter_characteristics.items() if traits]) + "\n"

        return regenerate()
