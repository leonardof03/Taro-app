import os
import requests

# Definindo o token do GitHub e detalhes do pull request
github_token = os.getenv('GITHUB_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')  # Certifique-se de definir esta variável de ambiente no seu workflow
pull_index = os.getenv('PULL_REQUEST_ID')
repo_name = "leonardof03/taro-app"

# Configura os headers para uso nas requisições HTTP
def get_headers(auth_token, is_openai=False):
    if is_openai:
        return {'Authorization': f'Bearer {auth_token}', 'Content-Type': 'application/json'}
    else:
        return {'Authorization': f'token {auth_token}', 'Accept': 'application/vnd.github.v3+json'}

# Obtém as alterações do pull request especificado
def get_pull_request_changes():
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pull_index}/files"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}, {response.text}")
        return []

# Avalia o código usando o modelo da OpenAI
def review_code_with_chatgpt(code_changes):
    prompt = "Review the following code changes and provide comments:\n\n" + code_changes
    headers = get_headers(openai_api_key, is_openai=True)
    data = {"model": "gpt-4o", "prompt": prompt, "max_tokens": 150}
    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
    if response.ok:
        return response.json()['choices'][0]['text']
    else:
        print(f"Failed to generate review: HTTP {response.status_code}, {response.text}")
        return "Error generating review."

# Posta um comentário no pull request com a avaliação
def post_comment_to_pull_request(comment):
    url = f"https://api.github.com/repos/{repo_name}/issues/{pull_index}/comments"
    headers = get_headers(github_token)

_token)
    data = {'body': comment}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment posted successfully")
    else:
        print(f"Failed to post comment: HTTP {response.status_code}, {response.text}")

# Main execution block
if __name__ == "__main__":
    if not github_token or not openai_api_key or not pull_index:
        print("Error: Missing GitHub token, OpenAI API key, or pull request ID.")
    else:
        changes = get_pull_request_changes()
        if changes:
            code_snippets = '\n'.join([file['patch'] for file in changes if 'patch' in file])
            review_comment = review_code_with_chatgpt(code_snippets)
            post_comment_to_pull_request(review_comment)
        else:
ente print("No changes to review or failed to fetch changes.")
