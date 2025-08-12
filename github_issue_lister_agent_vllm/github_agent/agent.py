import os
from github import Github, GithubException
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Endpoint URL provided by your vLLM deployment
api_base_url = "https://vllm-gemma-3-1b/v1"

# Model name as recognized by *your* vLLM endpoint configuration
model_name_at_endpoint = "hosted_vllm/google/gemma-3-1b-it" # Example from vllm_test.py

def list_issues(repo_name: str, limit: int) -> dict:

    github_token = os.getenv("GITHUB_TOKEN")
    g = Github(github_token)

    try:
        repo = g.get_repo(repo_name)
        issues = repo.get_issues(state="open")
        
        print(f"Listing the first {limit} open issues for {repo_name}:")
        
        issue_list = list(issues[:limit])
        if not issue_list:
            print("No open issues found.")
            return {"status": "empty", "issue_list": []}

        issue_titles = []
        for issue in issue_list:
            issue_titles.append(f" #{issue.number} - {issue.title}")

        return {"status": "success", "issue_titles": issue_titles}

    except GithubException as e:
        print(f"An error occurred while communicating with GitHub: {e.data}")
        if e.status == 401:
            print("Hint: A valid GITHUB_TOKEN is required for private repositories.")
        elif e.status == 403:
            print("Hint: You may have hit the rate limit for unauthenticated requests. Please set a GITHUB_TOKEN.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

agent_vllm = LlmAgent(
    model=LiteLlm(
        model=model_name_at_endpoint,
        api_base=api_base_url,
        # Pass authentication headers if needed
        extra_headers=auth_headers
        # Alternatively, if endpoint uses an API key:
        # api_key="YOUR_ENDPOINT_API_KEY"
    ),
    name="vllm_agent",
    instruction="You are a helpful assistant running on a self-hosted vLLM endpoint.",
    # ... other agent parameters
    tools=[list_issues]
)