from backend.model.story import Story
from backend.model.prompt import Prompt
from backend.model.character import Character
from backend.model.chapter import Chapter

def test_story_init():
    s = Story()
    assert isinstance(s, Story)

def test_add_prompt():
    s = Story()
    s.set_prompt(1, "This is a string for a prompt")

    assert isinstance(s.prompt(1), Prompt)

# set the prompt to something new and try to get the new prompt from within.
# def test_get_prompt():
#     s = Story()
#     s.set_prompt(1, "This is a string for a prompt")
#     s.set_prompt(2, "This is a string for a prompt")
#     s.set_prompt(3, "This is a string for a prompt")
#     s.set_prompt(4, "This is a string for a prompt")
#     s.set_prompt(1, "This is edited")

#     assert s.prompt(1).text == "This is edited"

def test_form_prompt():
    s = Story()
    s.set_prompt(1, "This is a string for a prompt")
    s.prompts[1].message("Bill finished eating", {"Bill": ["persuasive", "weird"]})
