import openai
import os

def main():
    # Acessa a chave da API do ambiente
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Olá, como posso converter Celsius para Fahrenheit?"}
    ]
)

        print(response.choices[0].text.strip())
    except Exception as e:
        print(f"Erro ao acessar a API da OpenAI: {str(e)}")

if __name__ == "__main__":
    main()
