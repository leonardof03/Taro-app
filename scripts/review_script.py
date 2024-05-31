import os
import requests
import base64
import time

github_token = os.getenv('GITHUB_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
repo_name = "leonardof03/Taro-app"

def get_headers(auth_token, is_openai=False):
    if is_openai:
        return {'Authorization': f'Bearer {auth_token}', 'Content-Type': 'application/json'}
    else:
        return {'Authorization': f'token {auth_token}', 'Accept': 'application/vnd.github.v3+json'}

def get_repository_files():
    url = f"https://api.github.com/repos/{repo_name}/git/trees/main?recursive=1"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)
    if response.ok:
        return [file['path'] for file in response.json().get('tree', []) if file['type'] == 'blob']
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}, {response.text}")
        return []

def get_file_content(file_path):
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)
    if response.ok:
        content = response.json().get('content', '')
        try:
            return base64.b64decode(content).decode('utf-8')
        except UnicodeDecodeError:
            return base64.b64decode(content).decode('latin-1')
    else:
        print(f"Failed to fetch file content: HTTP {response.status_code}, {response.text}")
        return ''

def analyze_and_fix_code_with_chatgpt(code_changes):
    max_tokens = 4096
    chunk_size = max_tokens - 1000
    analysis_comments = []
    
    for i in range(0, len(code_changes), chunk_size):
        chunk = code_changes[i:i + chunk_size]
        prompt = "Please analyze this repository and provide a rating from 1 to 5, where 1 indicates a poorly executed project and 5 indicates a well-executed project. Identify the programming languages used and provide a brief description of the project." + chunk
        headers = get_headers(openai_api_key, is_openai=True)
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "system", "content": "You are a code reviewer."},
                         {"role": "user", "content": prompt}]
        }
        response = None
        for attempt in range(5):  # Retry up to 5 times with exponential backoff
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            if response.ok:
                analysis_comments.append(response.json()['choices'][0]['message']['content'])
                break
            else:
                print(f"Attempt {attempt + 1} failed: HTTP {response.status_code}, {response.text}")
                if response.status_code == 429:
                    time.sleep((2 ** attempt) + 1)  # Exponential backoff
                else:
                    break
    
    return "\n\n".join(analysis_comments)

def post_issues(comment, github_token, repo_name):
    url = f"https://api.github.com/repos/{repo_name}/issues"
    headers = get_headers(github_token)
    
    max_length = 65536
    comment_parts = [comment[i:i + max_length] for i in range(0, len(comment), max_length)]
    
    for i, part in enumerate(comment_parts):
        data = {'title': f'AI Code Analysis Part {i+1}', 'body': part}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Issue part {i+1} posted successfully")
        else:
            print(f"Failed to post issue part {i+1}: HTTP {response.status_code}, {response.text}")

if __name__ == "__main__":
    if not github_token or not openai_api_key:
        print("Error: Missing GitHub token or OpenAI API key.")
    else:
        files = get_repository_files()
        if files:
            batch_size = 5
            for start in range(0, len(files), batch_size):
                batch_files = files[start:start + batch_size]
                code_snippets = ''
                for file in batch_files:
                    content = get_file_content(file)
                    if content:
                        code_snippets += f"File: {file}\n{content}\n\n"
                analysis_comment = analyze_and_fix_code_with_chatgpt(code_snippets)
                if analysis_comment:
                    post_issues(analysis_comment, github_token, repo_name)
                time.sleep(10)  # Small delay to avoid hitting rate limits
        else:
            print("No files to review or failed to fetch files.")
