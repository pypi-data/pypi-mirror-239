import sys
from cannoli import Cannoli 

n = 50
prompt=f"""Generate a list of {n} sentences about a restaurant's quality. 
        There should be an equal number of positive and negative sentences. 
        Don't enumerate the sentences.
        Add a '1' for positive and a '0' for negative at the end of the each sentence.
        Format: sentence|number""",

setup = {
    "engine": "gpt-3.5-turbo-instruct",
    "max_tokens": 50*n,
    "temperature": 0.7
}

def generate_reviews(prompt):
    fake_data = Cannoli(setup=setup)
    return fake_data.quick_question(prompt)

def save_reviews(reviews):
    if not reviews:
        print('Error')
    else:
        with open('datasets/reviews.dsv', 'w', encoding='utf-8') as freview:
            freview.write(reviews)
        print("Done.")

reviews = generate_reviews(prompt)
save_reviews(reviews)


