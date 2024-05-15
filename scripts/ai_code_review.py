import openai
import os

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")

    try:
        response = openai.Completion.create(
          engine="davinci",
          prompt="Translate the following English text to French: Hello, how are you?",
          max_tokens=60
        )
        print(response.choices[0].text.strip())
    except Exception as e:
        print(f"Erro ao acessar a API da OpenAI: {str(e)}")

if __name__ == "__main__":
    main()
