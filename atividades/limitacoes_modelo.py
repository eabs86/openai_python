from dotenv import dotenv_values

import openai

env = dotenv_values(".env")

API_KEY = env["API_KEY_OPENAI"]

print(API_KEY)

openai.api_key = API_KEY

# O modelo pode passar também por "alucinações" quando a entrada é uma mistura do que é 
# verdade com o que é mentira.

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

# Neste caso Boie é uma empresa real, porém o produto não é

PROMPT = """
Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie
"""
response = get_completion(PROMPT)
print(response)

# O retorno desse prompt é um texto bem realista, como se o produto existisse.

# Para evitar isso recomenda-se colocar no prompt para que ele bus por informações relevantes antes,
# e que responda as peguntas feitas no prompt com base em informações relevantes.

#Exemplo:

prompt = """
Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie. Before you tell me something, check if the product exists or not.
Give relevant information about the product if it exists. If not, give me an output 'the product does not exist'
"""
response = get_completion(prompt)
print(response)
# A resposta: I'm sorry, but the product AeroGlide UltraSlim Smart Toothbrush by Boie does not exist.