import openai

def main():
    # Substitua pela sua chave de API real
    openai.api_key = "YOUR_OPENAI_API_KEY"

    code_snippet = """
    # Exemplo de código Python
    def calculate_factorial(n):
        if n == 0:
            return 1
        else:
            return n * calculate_factorial(n-1)
    """

    try:
        response = openai.Completion.create(
            model="gpt-4.0-turbo",
            prompt=f"Revisar o seguinte código Python e sugerir melhorias:\n\n{code_snippet}",
            max_tokens=150
        )
        print("Revisão e sugestões de melhoria:")
        print(response['choices'][0]['text'])
    except Exception as e:
        print(f"Erro ao acessar a API da OpenAI: {e}")

if __name__ == "__main__":
    main()
