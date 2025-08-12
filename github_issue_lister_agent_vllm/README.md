# GitHub Issue Lister Agent

This agent lists the open issues for a specified GitHub repository.

## Usage

1.  Install the dependencies:

    ```bash
    pip install -e .
    ```

2.  Run the agent:

    ```bash
    github-issue-lister <owner/repo> [--limit <number_of_issues>]
    ```

    For example:

    ```bash
    github-issue-lister "google/gemini-cli" --limit 5
    ```

    A `GITHUB_TOKEN` environment variable can be set for private repositories or to avoid rate limits.



curl -X POST -H "Authorization: Bearer $TOKEN" \
    $APP_URL/apps/github-issue-app/users/user_123/sessions/session_abc \
    -H "Content-Type: application/json" \
    -d '{"state": {"preferred_language": "English", "visit_count": 5}}'


curl -X POST -H "Authorization: Bearer $TOKEN" \
    $APP_URL/run_sse \
    -H "Content-Type: application/json" \
    -d '{
    "app_name": "github-issue-app",
    "user_id": "user_123",
    "session_id": "session_abc",
    "new_message": {
        "role": "user",
        "parts": [{
        "text": "list me the issues in GoogleCloudPlatform/kubernetes-engine-samples"
        }]
    },
    "streaming": false
    }'