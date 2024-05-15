import os
import requests

# Chaves de API configuradas diretamente no código
github_token = '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'
openai_api_key = 'sk-proj-MEU8923wdVOM8vADDdMmT3BlbkFJmC9vtQZjPM2fb4lXj0UI'
pull_index = os.getenv('PULL_REQUEST_ID')  # Presumindo que o ID do pull request ainda seja fornecido por variável de ambiente
repo_name = "leonardof03/taro-app"

def get_headers(auth_token, content_type='application/json'):
    return {'Authorization': f'token {auth_token}', 'Content-Type': content_type}

def get_pull_request_changes():
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pull_index}/files"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}, {response.text}")
        return []

def review_code_with_chatgpt(code_changes):
    prompt = "Review the following code changes and provide comments:\n\n" + code_changes
    headers = get_headers(openai_api_key, 'application/json')
    data = {"model": "gpt-3.5-turbo", "prompt": prompt, "max_tokens": 150}
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json=data)
    if response.ok:
        return response.json()['choices'][0]['text']
    else:
        print(f"Failed to generate review: HTTP {response.status_code}, {response.text}")
        return "Error generating review."

def post_comment_to_pull_request(comment):
    url = f"https://api.github.com/repos/{repo_name}/issues/{pull_index}/comments"
    headers = get_headers(githubtn_code_review.ymloken)
    data = {'body': comment}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment posted successfully")
    else:
        print(f"Failed to post comment: HTTP {response.status_code}, {response.text}")

if __name__ == "__main__":
    changes = get_pull_request_changes()
    if changes:
        code_snippets = '\n'.join([file['patch'] for file in changes if 'patch' in file])
        review_comment = review_code_with_chatgpt(code_snippets)
        post_comment_to_pull_request(review_comment)
    else:
  print("No changes to review")
