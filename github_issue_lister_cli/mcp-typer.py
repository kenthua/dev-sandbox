import json
import os

import typer
from github import Github, GithubException


def list_issues(repo_name: str, limit: int) -> dict:
    """
    Lists open issues for a given GitHub repository.
    """
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
        error_message = f"An error occurred while communicating with GitHub: {e.data}"
        print(error_message)
        if e.status == 401:
            print("Hint: A valid GITHUB_TOKEN is required for private repositories.")
        elif e.status == 403:
            print(
                "Hint: You may have hit the rate limit for unauthenticated requests. Please set a GITHUB_TOKEN."
            )
        return {"status": "error", "message": error_message}

    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return {"status": "error", "message": error_message}


def main(
    repo_name: str = typer.Argument(..., help="The name of the repository in the format 'user/repo'."),
    limit: int = typer.Argument(..., help="The maximum number of issues to list."),
):
    """
    CLI application to list GitHub issues.
    """
    issues = list_issues(repo_name, limit)
    print(json.dumps(issues, indent=2))


if __name__ == "__main__":
    typer.run(main)