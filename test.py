import requests
import json
import time

# Base URL for the backend server
base_url = "http://127.0.0.1:5000"

# To generate a chapter
def generate_chapter(prompt, clear_previous=False):
    # To send a POST request to the backend to generate a chapter
    response = requests.post(
        f"{base_url}/generate_chapter",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"prompt": prompt, "clear_previous": clear_previous}),
        stream=True
    )

    # To print the response
    print("\nGenerating Chapter Response:")
    if response.status_code == 200:
        # To stream the response and print each chunk as it is received
        for chunk in response.iter_content(chunk_size=128):
            if chunk:
                print(chunk.decode('utf-8'), end='', flush=True)
    else:
        # To print an error message if the request fails
        print(f"Failed to generate chapter. Status Code: {response.status_code}")
        if response.content:
            try:
                print(response.json())
            except requests.exceptions.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                print(response.text)
    return response

# To regenerate a chapter
def regenerate_chapter(chapter_num, prompt, max_tokens=4096):
    # To send a POST request to the backend to regenerate a chapter
    response = requests.post(
        f"{base_url}/regenerate_chapter",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"chapter_num": chapter_num, "prompt": prompt, "max_tokens": max_tokens}),
        stream=True
    )

    # To print the response
    print(f"\nRegenerating Chapter {chapter_num} Response:")
    if response.status_code == 200:
        # To stream the response and print each chunk as it is received
        for chunk in response.iter_content(chunk_size=128):
            if chunk:
                print(chunk.decode('utf-8'), end='', flush=True)
    else:
        # To print an error message if the request fails
        print(f"Failed to regenerate chapter. Status Code: {response.status_code}")
        if response.content:
            try:
                print(response.json())
            except requests.exceptions.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                print(response.text)
    return response

# To fetch all chapters
def get_chapters():
    # To send a GET request to fetch all chapters
    response = requests.get(f"{base_url}/chapters")
    print("\nFetching Chapters Response:")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(response.text)
    return response

# To fetch all summaries
def get_summaries():
    # To send a GET request to fetch all summaries
    response = requests.get(f"{base_url}/summaries")
    print("\nFetching Summaries Response:")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(response.text)
    return response

# To fetch all character characteristics
def get_characters():
    # To send a GET request to fetch all character characteristics
    response = requests.get(f"{base_url}/characters")
    print("\nFetching Character Characteristics Response:")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(response.text)
    return response

# Prompts for generating chapters
prompts = [
    "Write the first chapter of a fictional story about a brave knight who saves a village from bandits and also finds her love interest in the village. Make it more than 1000 words, detailed and immersive.",
    "In the second chapter, the knight discovers a secret path with obstacles which leads to the town of bandits. Make it more than 1000 words, detailed and immersive.",
    "Write the third chapter where the knight faces the leader of the bandits and wins but the knight finds himself in a tricky situation when he sees his love interest kidnapped and during the battle the leader of the bandits kills her. Make it more than 1000 words, detailed and immersive."
]

# To generate the first chapter
print(f"\nGenerating Chapter 1...")
generate_chapter(prompts[0], clear_previous=True)

# Wait for 3 seconds
time.sleep(3)

# To generate the second chapter
print(f"\nGenerating Chapter 2...")
generate_chapter(prompts[1])

# Wait for 3 seconds
time.sleep(3)

# To regenerate the second chapter
print("\nRegenerating Chapter 2...")
regenerate_chapter(2, prompts[1], max_tokens=4096)

# Wait for 3 seconds
time.sleep(3)

# To generate the third chapter
print(f"\nGenerating Chapter 3...")
generate_chapter(prompts[2])

# Wait for 3 seconds
time.sleep(3)

# To fetch and print all chapters
chapters_response = get_chapters()
if chapters_response.status_code == 200:
    chapters = chapters_response.json().get("chapters", {})
    print("\nChapters History:")
    for title, content in chapters.items():
        print(f"\n{title}:\n{content}")

# To fetch and print all summaries
summaries_response = get_summaries()
if summaries_response.status_code == 200:
    summaries = summaries_response.json().get("summaries", [])
    print("\nSummaries:")
    for summary in summaries:
        print(f"\n{summary}")

print("\nAll chapters generated and analyzed.")
