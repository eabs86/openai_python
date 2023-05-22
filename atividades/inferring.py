from dotenv import dotenv_values

import openai

env = dotenv_values(".env")

API_KEY = env["API_KEY_OPENAI"]

print(API_KEY)

openai.api_key = API_KEY

#Nesta lição você inferirá sentimentos e tópicos de análises de produtos e artigos de notícias.


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


# Review de um produto

lamp_review = """
Needed a nice lamp for my bedroom, and this one had \
additional storage and not too high of a price point. \
Got it fast.  The string to our lamp broke during the \
transit and the company happily sent over a new one. \
Came within a few days as well. It was easy to put \
together.  I had a missing part, so I contacted their \
support and they very quickly got me the missing piece! \
Lumina seems to me to be a great company that cares \
about their customers and products!!
"""

# Verificar se a review tem sentimento positivo ou negativo.

PROMPT = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Review text: '''{lamp_review}'''
"""
response = get_completion(PROMPT)
print(response)

#Resposta: The sentiment of the product review is positive.

PROMPT = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text: '''{lamp_review}'''
"""
response = get_completion(PROMPT)
print(response)

#Resposta: positive


# Identificando tipos de emoções:

PROMPT = f"""
Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text: '''{lamp_review}'''
"""
response = get_completion(PROMPT)
print(response)
#Resposta: happy, satisfied, grateful, impressed, content


#Identificando Raiva

PROMPT = f"""
Is the writer of the following review expressing anger?\
The review is delimited with triple backticks. \
Give your answer as either yes or no.

Review text: '''{lamp_review}'''
"""
response = get_completion(PROMPT)
print(response)
#Resposta: No

# Extraindo infomações sobre o produto e a empresa a partir das reviews dos produtos:

PROMPT = f"""
Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
  
Review text: '''{lamp_review}'''
"""
response = get_completion(PROMPT)
print(response)

# Fazendo múltiplas tarefas de uma vez só

PROMPT = f"""
Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: '''{lamp_review}'''
"""
response = get_completion(PROMPT)
print(response)


# Inferindo um tópico
story = """
In a recent survey conducted by the government, 
public sector employees were asked to rate their level 
of satisfaction with the department they work at. 
The results revealed that NASA was the most popular 
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings, 
stating, "I'm not surprised that NASA came out on top. 
It's a great place to work with amazing people and 
incredible opportunities. I'm proud to be a part of 
such an innovative organization."

The results were also welcomed by NASA's management team, 
with Director Tom Johnson stating, "We are thrilled to 
hear that our employees are satisfied with their work at NASA. 
We have a talented and dedicated team who work tirelessly 
to achieve our goals, and it's fantastic to see that their 
hard work is paying off."

The survey also revealed that the 
Social Security Administration had the lowest satisfaction 
rating, with only 45% of employees indicating they were 
satisfied with their job. The government has pledged to 
address the concerns raised by employees in the survey and 
work towards improving job satisfaction across all departments.
"""

# A partir do texto dado anteriormente, inferir 5 tópicos
PROMPT = f"""
Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample: '''{story}'''
"""
response = get_completion(PROMPT)
print(response)
#Resposta: government survey, job satisfaction, NASA, Social Security Administration, employee concerns

response.split(sep=',')


# Fazer o alerta de notícias para determinados tópicos listados

topic_list = [
    "nasa", "local government", "engineering", 
    "employee satisfaction", "federal government"
]

PROMPT = f"""
Determine whether each item in the following list of \
topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as list with 0 or 1 for each topic.\

List of topics: {", ".join(topic_list)}

Text sample: '''{story}'''
"""
response = get_completion(PROMPT)
print(response)

#Esse tipo de estrutura não é a mais adequada. É melhor colocar em modo JSON a saída do prompt
# para facilitar a integração.
topic_dict = {i.split(': ')[0]: int(i.split(': ')[1]) for i in response.split(sep='\n')}
if topic_dict['nasa'] == 1:
    print("ALERT: New NASA story!")


#Solicitando em formato JSON
PROMPT = f"""
Determine whether each item in the following list of \
topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as list with 0 or 1 for each topic.\

List of topics: {", ".join(topic_list)}

Text sample: '''{story}'''

Give me the output in JSON format like: 'topic:occurence'

"""
response = get_completion(PROMPT)
print(response)

""" 
RESPOSTA:

1. nasa: 1
2. local government: 0
3. engineering: 0
4. employee satisfaction: 1
5. federal government: 1

Output in JSON format: 
{
"nasa": 1,
"local government": 0,
"engineering": 0,
"employee satisfaction": 1,
"federal government": 1
}

"""