from dotenv import dotenv_values
from IPython.display import display, Markdown, Latex, HTML, JSON
from redlines import Redlines

import openai

env = dotenv_values(".env")

API_KEY = env["API_KEY_OPENAI"]

print(API_KEY)

openai.api_key = API_KEY
# Exploraremos como usar modelos de linguagem grandes para tarefas de transformação de texto,
# como tradução de idiomas, verificação ortográfica e gramatical, ajuste de tom e conversão de formato.

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

#Tradução de idiomas

PROMPT = """
Translate the following English text to Spanish: \ 
```Hi, I would like to order a blender```
"""
response = get_completion(PROMPT)
print(response)

# Verificação de idioma

PROMPT = """
Tell me which language this is: 
```Combien coûte le lampadaire?```
"""
response = get_completion(PROMPT)
print(response)

#Tradução em múltiplos idiomas

PROMPT = """
Translate the following  text to French and Spanish
and English pirate: \
```I want to order a basketball```
"""
response = get_completion(PROMPT)
print(response)

#Tradução formal e informal

PROMPT = """
Translate the following text to Spanish in both the \
formal and informal forms: 
'Would you like to order a pillow?'
"""
response = get_completion(PROMPT)
print(response)

#Tradutor universal
# Imagine que você é responsável pela TI em uma grande empresa multinacional de comércio eletrônico.
# Os usuários estão enviando mensagens para você com problemas de TI em todos os seus idiomas nativos.
# Sua equipe é de todo o mundo e fala apenas seus idiomas nativos.
# Você precisa de um tradutor universal!

user_messages = [
  "La performance du système est plus lente que d'habitude.",  # System performance is slower than normal         
  "Mi monitor tiene píxeles que no se iluminan.",              # My monitor has pixels that are not lighting
  "Il mio mouse non funziona",                                 # My mouse is not working
  "Mój klawisz Ctrl jest zepsuty",                             # My keyboard has a broken control key
  "我的屏幕在闪烁"                                               # My screen is flashing
]

for issue in user_messages:
    prompt = f"Tell me what language this is: ```{issue}```"
    lang = get_completion(prompt)
    print(f"Original message ({lang}): {issue}")

    prompt = f"""
    Translate the following  text to English \
    and Korean: ```{issue}```
    """
    response = get_completion(prompt)
    print(response, "\n")
    
# Mudança de tom

PROMPT = """
Translate the following from slang to a business letter: 
'Dude, This is Joe, check out this spec on this standing lamp.'
"""
response = get_completion(PROMPT)
print(response)


# Conversão de formatos
# É preciso informar no promt a descrição do formato das entradas e saídas.

data_json = { "resturant employees" :[
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
]}

PROMPT = f"""
Translate the following python dictionary from JSON to an HTML \
table with column headers and title: {data_json}
"""
response = get_completion(PROMPT)
print(response)
display(HTML(response))

#Verificação Ortográfica/Gramática

#Aqui estão alguns exemplos de problemas comuns de gramática e ortografia e a resposta do LLM.

#Para sinalizar ao LLM que você deseja revisar seu texto, você instrui o modelo
# a 'revisar' ou 'revisar e corrigir'.

text = [ 
  "The girl with the black and white puppies have a ball.",  # The girl has a ball.
  "Yolanda has her notebook.", # ok
  "Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
  "Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
  "Your going to need you’re notebook.",  # Homonyms
  "That medicine effects my ability to sleep. Have you heard of the butterfly affect?", # Homonyms
  "This phrase is to cherck chatGPT for speling abilitty"  # spelling
]
for t in text:
    PROMPT = f"""Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```{t}```"""
    response = get_completion(PROMPT)
    print(response)


text = """
Got this for my daughter for her birthday cuz she keeps taking \
mine from my room.  Yes, adults also like pandas too.  She takes \
it everywhere with her, and it's super soft and cute.  One of the \
ears is a bit lower than the other, and I don't think that was \
designed to be asymmetrical. It's a bit small for what I paid for it \
though. I think there might be other options that are bigger for \
the same price.  It arrived a day earlier than expected, so I got \
to play with it myself before I gave it to my daughter.
"""
PROMPT = f"proofread and correct this review: ```{text}```"
response = get_completion(PROMPT)
print(response)

#Para mostrar as diferenças em vermelho, e os erros cortados
diff = Redlines(text,response)
display(Markdown(diff.output_markdown))

PROMPT = f"""
proofread and correct this review. Make it more compelling. 
Ensure it follows APA style guide and targets an advanced reader. 
Output in markdown format.
Text: ```{text}```
"""
response = get_completion(PROMPT)
display(Markdown(response))
