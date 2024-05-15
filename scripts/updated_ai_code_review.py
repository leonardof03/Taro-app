import openai
import os

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Translate the following English text to French: Hello, how are you?"}]
        )
        print(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Erro ao acessar a API da OpenAI: {str(e)}")

if __name__ == "__main__":
    main()
