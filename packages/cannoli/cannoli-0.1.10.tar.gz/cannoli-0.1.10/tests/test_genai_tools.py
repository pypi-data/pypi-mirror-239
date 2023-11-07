import pytest
from cannoli.cannoli import *

def test_check_default_values():
    default_values = {
        "engine": "text-davinci-003",
        "prompt": "Your are my personal assistant. Answer me the best as you can.",
        "max_tokens": 300,
        "temperature": 0.7
    }    
    cannoli = Cannoli()
    assert cannoli.setup == default_values  


def test_get_api_key():
    cannoli = Cannoli()
    assert len(cannoli.api_key)>0


def test_quick_question():
    cannoli = Cannoli()
    prompt = "answer me in one word, which country cannoli is?"
    assert cannoli.quick_question(prompt) == "Italy"