import os
import requests
import base64

# Defining the GitHub token and details of the repository
github_token = os.getenv('GITHUB_TOKEN')
openai_api_key = os.getenv('OPENAI_API_KEY')
repo_name = "leonardof03/taro-app"

# Configure headers for HTTP requests
def get_headers(auth_token, is_openai=False):
    if is_openai:
        return {'Authorization': f'Bearer {auth_token}', 'Content-Type': 'application/json'}
    else:
        return {'Authorization': f'token {auth_token}', 'Accept': 'application/vnd.github.v3+json'}

# Get the list of files in the repository
def get_repository_files():
    url = f"https://api.github.com/repos/{repo_name}/git/trees/main?recursive=1"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)
    if response.ok:
        return [file['path'] for file in response.json().get('tree', []) if file['type'] == 'blob']
    else:
        print(f"Failed to fetch data: HTTP {response.status_code}, {response.text}")
        return []

# Get the content of a file
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

# Review the code using the OpenAI model
def review_code_with_chatgpt(code_changes):
    max_tokens = 4096
    chunk_size = max_tokens - 1000  # Adjust to ensure we don't exceed token limits
    review_comments = []
    
    for i in range(0, len(code_changes), chunk_size):
        chunk = code_changes[i:i + chunk_size]
        prompt = "Review the following code and provide comments:\n\n" + chunk
        headers = get_headers(openai_api_key, is_openai=True)
        data = {
            "model": "gpt-4",
            "messages": [{"role": "system", "content": "You are a code reviewer."},
                         {"role": "user", "content": prompt}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        if response.ok:
            review_comments.append(response.json()['choices'][0]['message']['content'])
        else:
            print(f"Failed to generate review for chunk {i//chunk_size + 1}: HTTP {response.status_code}, {response.text}")
            break
    
    return "\n\n".join(review_comments)

# Post a comment on the repository with the evaluation
def post_comment_to_repository(comment):
    url = f"https://api.github.com/repos/{repo_name}/issues"
    headers = get_headers(github_token)
    data = {'title': 'AI Code Review', 'body': comment}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment posted successfully")
    else:
        print(f"Failed to post comment: HTTP {response.status_code}, {response.text}")

# Main execution block
if __name__ == "__main__":
    if not github_token or not openai_api_key:
        print("Error: Missing GitHub token or OpenAI API key.")
    else:
        files = get_repository_files()
        if files:
            code_snippets = ''
            for file in files[:5]:  # Limiting to the first 5 files to avoid exceeding the quota
                content = get_file_content(file)
                if content:
                    code_snippets += f"File: {file}\n{content}\n\n"
            review_comment = review_code_with_chatgpt(code_snippets)
            if review_comment:
                post_comment_to_repository(review_comment)
        else:
            print("No files to review or failed to fetch files.")
