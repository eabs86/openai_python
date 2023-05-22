from dotenv import dotenv_values

import openai

env = dotenv_values(".env")

API_KEY = env["API_KEY_OPENAI"]

print(API_KEY)

openai.api_key = API_KEY

# Nesta segunda atividade será dado um tempo para o modelo "pensar".
# Ou seja, os prompts não serão tão detalhados quanto o da primeira atividade.


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


#Tática 1: Especificar os passos necessários para completar uma tarefa.
text = """
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.

"""

# example 1
prompt_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following \
keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```
"""
response = get_completion(prompt_1)

print("Completion for prompt 1:")

print(response)


#Pedindo ao modelo para que a saída seja em um formato específico.
prompt_2 = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""
response = get_completion(prompt_2)
print("\nCompletion for prompt 2:")
print(response)

#Tática 2: Instruir o modelo para que ele ofereça uma solução definida por ele
#           antes de apresentar uma conclusão.

prompt = """
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need \
 help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \ 
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
response = get_completion(prompt)
print(response)

# Deve-se salientar que a solução do estudante no prompt acima não está correta.

# Nós podemos consertar isso instruingo o modelo para trabalhar com sua própria solução primeiramente.

prompt = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution \
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
"""
response = get_completion(prompt)
print(response)
