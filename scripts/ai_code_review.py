import os
import openai
import requests

def main():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    my_github_token = os.getenv('MY_GITHUB_TOKEN')

    # Usando a API da OpenAI
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Translate the following English text to French: 'Hello, world!'",
        max_tokens=60,
        api_key=openai_api_key
    )
    print("Response from OpenAI:", response)

    # Usando a API do GitHub
    headers = {"Authorization": f"Bearer {my_github_token}"}
    repo_response = requests.get("https://api.github.com/user/repos", headers=headers)
    print("Response from GitHub API:", repo_response.json())

if __name__ == "__main__":
    main()
