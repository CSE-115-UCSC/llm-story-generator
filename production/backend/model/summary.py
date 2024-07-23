import re

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
