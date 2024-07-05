import requests
import json
import time

base_url = "http://127.0.0.1:5000"

def generate_chapter(prompt, clear_previous=False):
    response = requests.post(
        f"{base_url}/generate_chapter",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"prompt": prompt, "clear_previous": clear_previous})
    )
    print("\nGenerating Chapter Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Content: {response.json() if response.content else 'No Content'}")
    return response

def get_chapters():
    response = requests.get(f"{base_url}/chapters")
    print("\nFetching Chapters Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Content: {response.json() if response.content else 'No Content'}")
    return response

def get_summaries():
    response = requests.get(f"{base_url}/summaries")
    print("\nFetching Summaries Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Content: {response.json() if response.content else 'No Content'}")
    return response

def get_characters():
    response = requests.get(f"{base_url}/characters")
    print("\nFetching Character Characteristics Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Content: {response.json() if response.content else 'No Content'}")
    return response

# Prompts for generating chapters about a knight's story
prompts = [
    "Write the first chapter of a fictional story about a brave knight who saves a village from bandits and also finds her love interest in the village. Make it more than 750 words.",
    "In the second chapter, The knight discovers a secret path with obstacles which goes to the town of bandits. Make it more than 750 words.",
    "Write the third chapter where the knight faces the leader of the bandits and wins but the knight finds himself in a tricky situation when he sees his love interest kidnapped and during the battle the leader of the bandits kills her. Make it more than 750 words."
]

# Generate and analyze chapters one by one
for i, prompt in enumerate(prompts):
    if i == 0:
        print(f"\nGenerating Chapter {i+1}...")
        generate_chapter(prompt, clear_previous=True)
    else:
        print(f"\nGenerating Chapter {i+1}...")
        generate_chapter(prompt)
    
    # Pause for a moment to allow the server to process the request
    time.sleep(1)

# Fetch and print history of chapters
chapters_response = get_chapters()
if chapters_response.status_code == 200:
    chapters = chapters_response.json().get("chapters", {})
    print("\nChapters History:")
    for title, content in chapters.items():
        print(f"\n{title}:\n{content}")

# Fetch and print summaries of chapters
summaries_response = get_summaries()
if summaries_response.status_code == 200:
    summaries = summaries_response.json().get("summaries", [])
    print("\nSummaries:")
    for summary in summaries:
        print(f"\n{summary}")

# Fetch and print character characteristics
characters_response = get_characters()
if characters_response.status_code == 200:
    characteristics = characters_response.json().get("characteristics", {})
    print("\nCharacter Characteristics:")
    for char, characs in characteristics.items():
        print(f"\n{char}: {characs}")

print("\nAll chapters generated and analyzed.")
