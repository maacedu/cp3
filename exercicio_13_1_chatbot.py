
import os

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
modelo = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not api_key:
    print("API key não configurada.")
    print("Configure OPENAI_API_KEY no arquivo .env.")
    raise SystemExit

client = OpenAI(api_key=api_key)

# Histórico da conversa
historico = []

instrucoes = """
Você é um assistente de segurança da informação.

Responda em português brasileiro.
Explique os conceitos de maneira simples.
Seja objetivo e didático.
Não invente informações.
Não execute comandos nem ações externas.
"""


print("=== CHATBOT DE SEGURANÇA ===")
print("Digite /sair para encerrar.\n")

while True:

    pergunta = input("Você: ").strip()

    if pergunta.lower() == "/sair":
        print("Assistente: Até logo!")
        break

    if not pergunta:
        print("Digite uma pergunta.")
        continue

    # Adiciona a pergunta ao histórico
    historico.append({
        "role": "user",
        "content": pergunta
    })

    try:

        resposta = client.responses.create(
            model=modelo,
            instructions=instrucoes,
            input=historico,
            max_output_tokens=400,
            store=False
        )

        texto = resposta.output_text.strip()

        print("\nAssistente:", texto, "\n")

        # Guarda a resposta para o próximo turno
        historico.append({
            "role": "assistant",
            "content": texto
        })

        # Limita o histórico para controlar o tamanho
        if len(historico) > 20:
            historico = historico[-20:]

    except OpenAIError as erro:

        print("\nErro ao consultar a API:", erro)

        # Remove a pergunta que não recebeu resposta
        historico.pop()

    except KeyboardInterrupt:

        print("\nChatbot encerrado.")
        break
