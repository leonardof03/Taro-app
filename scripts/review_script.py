import os
import json
import requests

# Configuração das chaves de API
github_token = os.getenv('MY_GITHUB_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
pull_index = os.getenv('PULL_REQUEST_ID')

# URL do repositório e ID do pull request (ajustar conforme necessário)
repo_name = "leonardof03/taro-app"

# Função para obter as mudanças do pull request
def get_pull_request_changes():
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pull_index}/files"
    headers = {'Authorization': f'token {github_token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Função para enviar o código para revisão do ChatGPT
def review_code_with_chatgpt(code_changes):
    prompt = "Review the following code changes and provide comments:\n\n" + code_changes
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "prompt": prompt,
        "max_tokens": 150
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json=data)
    return response.json()['choices'][0]['text']

# Função para postar comentários no pull request
def post_comment_to_pull_request(comment):
    url = f"https://api.github.com/repos/{repo_name}/issues/{pull_index}/comments"
    headers = {
        'Authorization': f'token {github_token}',
        'Content-Type': 'application/json'
    }
    data = {'body': comment}
    response = requests.post(url, headers=headers, json=data)
    return response

# Execução do script
if __name__ == "__main__":
    changes = get_pull_request_changes()
    code_snippets = '\n'.join([file['patch'] for file in changes if file.get('patch')])
    review_comment = review_code_with_chatgpt(code_snippets)
    post_comment_to_pull_request(review_comment)
