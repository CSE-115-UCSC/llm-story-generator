# Class to handle summaries
class Summary:
    def __init__(self):
        # Initializing an empty list to store summaries
        self.summaries = []

    # To add a summary of a chapter
    def add(self, chapter, chapter_num):
        # To summarize the chapter text
        summary = self.summarize_text(chapter)
        # To create a formatted summary with the chapter title
        chapter_title = f"Chapter {chapter_num}: {chapter.splitlines()[0]}"
        formatted_summary = f"{chapter_title}\n{summary}"
        self.summaries.append(formatted_summary)

    # To get all summaries
    def get_all(self):
        formatted_summaries = []
        for idx, summary in enumerate(self.summaries):
            # To format the summaries without initial chapter titles
            chapter_title = f"Chapter {idx + 1}"
            formatted_summary = re.sub(r'Chapter \d+: .*?(\n|$)', '', summary).strip()
            formatted_summaries.append(f"Chapter {idx + 1}:\n{formatted_summary}")
        return formatted_summaries

    # Static method to summarize a given text using OpenAI API
    @staticmethod
    def summarize_text(text):
        # Prompt for summarizing the text
        prompt = f"Please summarize the following text:\n{text}"
        summary = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7
        ).choices[0].message['content'].strip()
        return summary

