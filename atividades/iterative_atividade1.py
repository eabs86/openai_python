from dotenv import dotenv_values

import openai

env = dotenv_values(".env")

API_KEY = env["API_KEY_OPENAI"]

print(API_KEY)

openai.api_key = API_KEY

#Nesta lição você analisará e refinará iterativamente seus prompts 
#para gerar uma cópia de marketing de uma ficha técnica do produto.

def get_completion(prompt, model="gpt-3.5-turbo"):
    
    """
    Given a prompt and an optional OpenAI model name, this function generates a
    chatbot response using the specified model. The chatbot response is based on
    the prompt and the degree of randomness specified by the temperature
    parameter. The function returns the chatbot's response as a string.
    
    :param prompt: A string representing the prompt for the chatbot.
    :param model: An optional string representing the name of the OpenAI model to
                  use. Defaults to "gpt-3.5-turbo".
                  
    :return: A string representing the chatbot's response to the given prompt.
    """
    messages = [{"role": "user", "content": prompt}]
    response_struct = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response_struct.choices[0].message["content"]

# Gerando uma descrição de produto de marketing a partir de uma ficha técnica do produto

fact_sheet_chair = """
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
"""

prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Technical specifications: ```{fact_sheet_chair}```
"""
response = get_completion(prompt)
print(response)
