import openai
import os

def main():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": "Olá, como posso converter Celsius para Fahrenheit?"}
        ]
    )
    print(response)

if __name__ == "__main__":
    main()

