import os

from dotenv import load_dotenv
from openai import OpenAI

# Carrega as configurações do arquivo .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY não configurada!")

client = OpenAI(api_key=api_key)

resposta = client.responses.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    instructions="Você é um professor de segurança da informação.",
    input="Explique em duas frases o que é SQL Injection.",
    max_output_tokens=150
)

print(resposta.output_text)