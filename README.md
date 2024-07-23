
# LLM Story Generator

The LLM Story Generator is a web application designed to assist writers by generating story chapters based on user prompts, displaying previous chapters, providing summaries, and detailing character traits. This tool leverages a Large Language Model (LLM) to enhance the writing process, making it more efficient and creative.

## Features

### Prompt Input and Chapter Display
1. **Prompt Field and Button**
   - A user interface component where writers can input their prompts.
   - A button to submit the prompt.

2. **Calling LLM API with Prompt**
   - Integration with the LLM API to process the prompt and generate a story chapter.

3. **Main Section with Historical Prompt-Response List**
   - A section displaying the list of prompts and their corresponding generated chapters.

4. **Prompt-Response List Element**
   - Each element in the list contains the prompt with the generated response displayed below it.

### Viewing Previous Chapters
1. **Chapter Section with Drop-Down List**
   - A section that displays a drop-down list of all generated chapters.

2. **Chapter Drop-Down List Elements**
   - Each element in the drop-down list shows the first few sentences of the chapter with a "load more" button to expand and read the full chapter.

3. **Chapters Model in Python**
   - A backend model to represent chapters, making it easier to manage and retrieve chapter information.

### Visual Cues and Real-Time Feedback
1. **Unified MUI Theme**
   - A cohesive theme based on the frontend design guidelines to ensure a consistent user experience.

2. **Real-Time Text Animation**
   - Animated text display that simulates typing to provide visual feedback that the application is processing the prompt.

3. **Streaming API for Chapter Generation**
   - An API that streams the generated text in real-time, enhancing the responsiveness of the application.

### Chapter Summaries and Character Personas
1. **Chapter Summary and Character Personas Split Screen**
   - A split-screen view that allows writers to see the chapter summary and character personas alongside the full chapter.

2. **Chapter Summary Generation**
   - Automatic generation of chapter summaries based on the chapter content.

3. **Character Trait Management**
   - A section to manage character traits, with an API call to populate character traits and a regenerate button for updates.

### Summaries of Each Chapter
1. **Summary Section with Statement List**
   - A section that displays a list of summary statements for each chapter.

2. **Summary List Elements**
   - Each element contains a fact or event with a correct/incorrect button for validation.

3. **GET Summary Resource**
   - An API resource to fetch summaries and hydrate the UI with summary data.

4. **Summary Object in Backend**
   - A backend object to represent and manage chapter summaries.

### Story Prompt and Real-Time Chapter Display
1. **Prompt Text Field with Real-Time Display**
   - A text field at the bottom of the interface for entering prompts, with real-time display of generated text above it.

2. **Event Stream for Text Chunks**
   - A streaming connection that sends text chunks to the client in real-time as the LLM processes the prompt.

3. **Backend Processing and Chapter Object Management**
   - The server processes the prompt, generates the chapter, and immediately generates the chapter summary, managing these objects within the story manager.

### Quick View of Characters and Traits
1. **Character and Trait Drop-Down Menu**
   - A menu to view characters and their traits, linked to the relevant chapters.

2. **Character Trait Updates and Regeneration**
   - Options to update character traits with correct/incorrect buttons and regenerate the chapter based on these updates.

### Viewing Generated Chapters
1. **Chapter Drop-Down Menu**
   - A menu to view generated chapters with an option to expand and read the full text.

2. **API for Chapter Retrieval**
   - An API function to fetch and display all generated chapters, ensuring the latest content is available.

## Usage

1. **Enter a Prompt**
   - Type your story prompt into the input field at the bottom of the screen and press the submit button.

2. **View Generated Chapters**
   - Generated chapters will appear in the main section above the prompt field.

3. **Navigate Previous Chapters**
   - Use the chapter drop-down menu to navigate and read previous chapters.

4. **View Summaries and Character Traits**
   - Use the split-screen view to see chapter summaries and character personas alongside the full chapter.

5. **Validate and Update Information**
   - Use the correct/incorrect buttons to validate summaries and character traits, and regenerate content as needed.

## Acknowledgements

- Special thanks to Professor Richard K. Jullig, CSE 115A Teaching Staff and Mr. Golam Md Muktadir who made this project possible.
