import os
from github import Github, GithubException

import vertexai
from vertexai import agent_engines

vertexai.init(
    project="qwiklabs-gcp-03-cf7230a8ff67",               # Your project ID.
    location="us-central1",                # Your cloud region.
    staging_bucket="gs://qwiklabs-gcp-03-cf7230a8ff67",  # Your staging bucket.
)

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
            print(
                "Hint: You may have hit the rate limit for unauthenticated requests. Please set a GITHUB_TOKEN."
            )

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


from google.adk.agents import Agent
from vertexai.preview.reasoning_engines import AdkApp

agent = Agent(
    model="gemini-2.0-flash",
    name="github_list_issues_agent",
    tools=[list_issues],
)

app = AdkApp(agent=agent)

from vertexai import agent_engines

remote_agent = agent_engines.create(
    app,
    requirements=["google-cloud-aiplatform[agent_engines,adk]","PyGithub"],
)

#### LOCAL TESTING ####
for event in remote_agent.stream_query(
    user_id="test",
    message="What are the 3 latest issues open in GoogleCloudPlatform/kubernetes-engine-samples",
):
    print(event)

## get the name of the resource for remote call
remote_agent.resource_name

#### REMOTE TESTING ####

# import vertexai
# from vertexai import agent_engines

# vertexai.init(
#     project="qwiklabs-gcp-03-cf7230a8ff67",               # Your project ID.
#     location="us-central1",                # Your cloud region.
#     staging_bucket="gs://qwiklabs-gcp-03-cf7230a8ff67",  # Your staging bucket.
# )

# agent_engine = vertexai.agent_engines.get('projects/344068085949/locations/us-central1/reasoningEngines/2546108290115305472')
# for event in agent_engine.stream_query(
#     user_id="test",
#     message="What are the 3 latest issues open in GoogleCloudPlatform/kubernetes-engine-samples",
# ):
#     print(event)

#### curl ####

# https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/overview#rest
# does not work, API message format issue and no instructions to get create/get user session
# curl \
# -H "Authorization: Bearer $(gcloud auth print-access-token)" \
# -H "Content-Type: application/json" \
# https://us-central1-aiplatform.googleapis.com/v1/projects/qwiklabs-gcp-03-cf7230a8ff67/locations/us-central1/reasoningEngines/2546108290115305472

# curl \
# -H "Authorization: Bearer $(gcloud auth print-access-token)" \
# -H "Content-Type: application/json" \
# https://us-central1-aiplatform.googleapis.com/v1/projects/qwiklabs-gcp-03-cf7230a8ff67/locations/us-central1/reasoningEngines/2546108290115305472:query -d '{
#   "class_method": "stream_query",
#   "input": {
#     "input": "What are the 3 latest issues open in GoogleCloudPlatform/kubernetes-engine-samples"
#   }
# }'

# curl \
# -H "Authorization: Bearer $(gcloud auth print-access-token)" \
# -H "Content-Type: application/json" \
# https://us-central1-aiplatform.googleapis.com/v1/projects/qwiklabs-gcp-03-cf7230a8ff67/locations/us-central1/reasoningEngines/2546108290115305472:query -d '{
#   "class_method": "async_stream_query",
#   "user_id": "test",
#   "input": {
#     "input": "What are the 3 latest issues open in GoogleCloudPlatform/kubernetes-engine-samples"
#   }
# }'