from dataclasses import dataclass, field

import openai
import os
import sys
import json
from pathlib import Path

@dataclass
class Cannoli:
    api_key: str= field(default=None)
    setup: dict = field(default=None)
    last_prompt: str = field(default='')
    response: dict = field(default=None)

    def __post_init__ (self):
        if not self.setup:
            self.load_default_settings()

        if not self.api_key:
            self.get_api_key()
        openai.api_key = self.api_key

    def load_default_settings(self):
        try:
            setup_filename = Path(__file__).resolve().parent / 'default_settings.json'
            with open(setup_filename, 'r', encoding='utf-8') as settings_file:
                self.setup = json.load(settings_file)
        except Exception:
            raise

    def get_api_key(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print('Error: OPENAI_API_KEY is missing. Please, include it in your initiatlization script.')
            sys.exit()

    def __parse_response(self, response):
        if response.get('error'):
            print(f"API Error - response['error']['message']: {response['error']['message']}")
            return None
        generated_text = response.choices[0].text.strip()
        return generated_text


    def api_request(self, prompt=None):
        if prompt: 
            self.last_prompt = '' if not self.setup.get('prompt') else self.setup.get('prompt') 
            self.setup['prompt'] = prompt
        print(self.setup)
        self.response = openai.Completion.create(**self.setup)
        return self.response

    def quick_question(self, prompt):
        self.api_request(prompt)
        return self.__parse_response(self.response)


def main():
    # making quick questions
    demo = Cannoli()
    ans = demo.quick_question("what is a cannoli?")
    print(ans)

    # accessing the full response
    print(demo.response)

    # accessing the last prompt
    demo.quick_question('who is gandalf?')
    print(demo.last_prompt)


if __name__ == "__main__":
    main()