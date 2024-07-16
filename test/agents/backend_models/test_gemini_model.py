import pytest

from crab import MessageType, action
from crab.agents.backend_models.gemini_model import GeminiModel

# TODO: Add mock data

@pytest.fixture
def gemini_model_text():
    return GeminiModel(
        model="gemini-1.5-pro-latest",
        parameters={"max_tokens": 3000},
        history_messages_len=1,
    )


@action
def add(a: int, b: int):
    """Add up two integers.

    Args:
        a: An addend
        b: Another addend
    """
    return a + b

@pytest.mark.skip(reason="Mock data to be added")
def test_text_chat(gemini_model_text):
    message = ("Hello!", MessageType.TEXT)
    output = gemini_model_text.chat(message)
    assert output.message
    assert output.action_list is None
    # assert gemini_model_text.token_usage > 0

    # Send another message to check accumulated tokens and history length
    message2 = ("Give me five!", MessageType.TEXT)
    output = gemini_model_text.chat(message2)
    # assert gemini_model_text.token_usage > 0
    assert output.message
    assert len(gemini_model_text.chat_history) == 2

    # Send another message to check accumulated tokens and chat history
    output = gemini_model_text.chat(message2)
    assert output.message
    assert len(gemini_model_text.chat_history) == 3


@pytest.mark.skip(reason="Mock data to be added")
def test_action_chat(gemini_model_text):
    gemini_model_text.reset("You are a helpful assistant.", [add])
    message = (
        "I had 10 dollars. Miss Polaris gave me 15 dollars. How many money do I have now.",
        0,
    )
    output = gemini_model_text.chat(message)
    assert output.message is None
    assert len(output.action_list) == 1
    assert output.action_list[0].arguments == {"a": 10, "b": 15}
    assert output.action_list[0].name == "add"
