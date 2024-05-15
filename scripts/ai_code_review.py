import os
import openai
import requests

# Obter variáveis de ambiente
github_token = os.getenv('GITHUB_TOKEN').strip()  # Remover possíveis espaços em branco e novas linhas
repository = os.getenv('REPOSITORY')
pull_request_number = os.getenv('PULL_REQUEST_NUMBER')

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY').strip()  # Remover possíveis espaços em branco e novas linhas

# Função para obter os arquivos modificados no pull request
def get_pull_request_files():
    url = f"https://api.github.com/repos/{repository}/pulls/{pull_request_number}/files"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Função para adicionar um comentário ao pull request
def post_pull_request_comment(comment):
    url = f"https://api.github.com/repos/{repository}/issues/{pull_request_number}/comments"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

# Função para analisar código com OpenAI
def analyze_code_with_openai(code):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Revise o seguinte código e sugira melhorias:\n\n{code}\n\nSugestões:",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Função principal
def main():
    try:
        files = get_pull_request_files()
        for file in files:
            if file['status'] == 'modified' or file['status'] == 'added':
                file_path = file['filename']
                patch = file.get('patch', '')
                if patch:
                    analysis = analyze_code_with_openai(patch)
                    comment = f"### Análise de AI para `{file_path}`\n\n{analysis}"
                    post_pull_request_comment(comment)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
