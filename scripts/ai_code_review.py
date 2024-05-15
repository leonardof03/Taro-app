import openai

def main():
    # Substitua pela sua chave de API real
    openai.api_key = "sk-proj-MEU8923wdVOM8vADDdMmT3BlbkFJmC9vtQZjPM2fb4lXj0UI"

    code_snippet = """
    # Exemplo de código Python
    def calculate_factorial(n):
        if n == 0:
            return 1
        else:
            return n * calculate_factorial(n-1)
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.0-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de IA especializado em revisão de código. Por favor, analise o código fornecido e sugira melhorias."},
                {"role": "user", "content": code_snippet}
            ]
        )
        print("Revisão e sugestões de melhoria:")
        print(response['choices'][0]['message']['content'])
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
