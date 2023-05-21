from dotenv import dotenv_values

import openai

env = dotenv_values(".env")

API_KEY = env["API_KEY_OPENAI"]

print(API_KEY)
