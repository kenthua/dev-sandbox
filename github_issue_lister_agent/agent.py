import os
from github import Github, GithubException
from google.adk.agents import Agent


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

root_agent = Agent(
    name="github_issue_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent that lists issues in the repository specifeid by the user"
    ),
    instruction=(
        "You are a helpful agent who will help the user list issues in their specified github repository"
    ),
    tools=[list_issues],
)