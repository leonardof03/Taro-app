import openai
import os

def analyze_code(code):
    response = openai.Completion.create(
      engine="code-davinci-002",
      prompt=f"Analyze this code: {code}",
      max_tokens=100
    )
    return response.choices[0].text.strip()

def main():
    # Exemplo de como você pode capturar o código de um PR
    # Aqui você precisaria implementar a lógica para extrair o código do PR
    code = "Example code from PR"
    analysis_result = analyze_code(code)
    print(f"Analysis Results: {analysis_definition}")

if __name__ == "__main__":
    main()
