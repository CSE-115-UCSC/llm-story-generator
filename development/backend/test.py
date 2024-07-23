# Import Statements
import requests
import json
import time

# Base URL for the Flask app
base_url = "http://127.0.0.1:5000"

# Function to generate a chapter by sending a POST request
def generate_chapter(book_num, prompt, clear_previous=False):
    response = requests.post(
        f"{base_url}/generate_chapter",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"book_num": book_num, "prompt": prompt, "clear_previous": clear_previous}),
        stream=True  # Streaming response to handle large responses
    )

    print("\nGenerating Chapter Response:")
    if response.status_code == 200:
        # To print response chunks as they are received
        for chunk in response.iter_content(chunk_size=128):
            if chunk:
                print(chunk.decode('utf-8'), end='', flush=True)
    else:
        print(f"Failed to generate chapter. Status Code: {response.status_code}")
        if response.content:
            try:
                print(response.json())
            except requests.exceptions.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                print(response.text)
    return response

# Function to regenerate a chapter by sending a POST request
def regenerate_chapter(book_num, chapter_num):
    response = requests.post(
        f"{base_url}/regenerate_chapter",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"book_num": book_num, "chapter_num": chapter_num}),
        stream=True  # Streaming response to handle large responses
    )

    print(f"\nRegenerating Chapter {chapter_num} Response:")
    if response.status_code == 200:
        # To print response chunks as they are received
        for chunk in response.iter_content(chunk_size=128):
            if chunk:
                print(chunk.decode('utf-8'), end='', flush=True)
    else:
        print(f"Failed to regenerate chapter. Status Code: {response.status_code}")
        if response.content:
            try:
                print(response.json())
            except requests.exceptions.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                print(response.text)
    return response

# Function to fetch all chapters by sending a GET request
def get_chapters(book_num):
    response = requests.get(f"{base_url}/books/{book_num}/chapters")
    print("\nFetching Chapters Response:")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(response.text)
    return response

# Function to fetch all summaries by sending a GET request
def get_summaries(book_num):
    response = requests.get(f"{base_url}/books/{book_num}/summaries")
    print("\nFetching Summaries Response:")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            summaries = response.json().get("summaries", [])
            print("\nSummaries:")
            if summaries:
                for summary in summaries:
                    for chapter_key, summary_text in summary.items():
                        print(f"Chapter {chapter_key.split('_')[-1]}:\n{summary_text}\n")
            else:
                print("No summaries available.")
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(response.text)
    return response

# Function to fetch all character characteristics by sending a GET request
def get_characters(book_num):
    response = requests.get(f"{base_url}/books/{book_num}/characters")
    print("\nFetching Character Characteristics Response:")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(response.text)
    return response

# Prompts
book_num = "1"
prompts = [
    "Write the first chapter of a fictional story about a brave knight who saves a village from bandits and also finds her love interest in the village. Make it more than 1000 words, detailed and immersive.",
    "In the second chapter, the knight discovers a secret path with obstacles which leads to the town of bandits. Make it more than 1000 words, detailed and immersive.",
    "Write the third chapter where the knight faces the leader of the bandits and wins but the knight finds herself in a tricky situation when she sees her love interest kidnapped and during the battle the leader of the bandits kills her. Make it more than 1000 words, detailed and immersive."
]

# To generate the first chapter
print(f"\nGenerating Chapter 1...")
generate_chapter(book_num, prompts[0], clear_previous=True)

# Wait for 3 seconds
time.sleep(3)

# To generate the second chapter
print(f"\nGenerating Chapter 2...")
generate_chapter(book_num, prompts[1])

# Wait for 3 seconds
time.sleep(3)

# To regenerate the second chapter
print("\nRegenerating Chapter 2...")
regenerate_chapter(book_num, 2)

# Wait for 3 seconds
time.sleep(3)

# To generate the third chapter
print(f"\nGenerating Chapter 3...")
generate_chapter(book_num, prompts[2])

# Wait for 3 seconds
time.sleep(3)

# To fetch and display all chapters
chapters_response = get_chapters(book_num)
if chapters_response.status_code == 200:
    chapters = chapters_response.json().get("chapters", {})
    print("\nChapters History:")
    if isinstance(chapters, dict):
        for index, (title, content) in enumerate(chapters.items(), 1):
            print(f"\nChapter {index}:\n{content['chapter_text']}")
    elif isinstance(chapters, list):
        for index, content in enumerate(chapters, 1):
            print(f"\nChapter {index}:\n{content}")

# To fetch and display all summaries
get_summaries(book_num)

print("\nAll chapters generated and analyzed.")
