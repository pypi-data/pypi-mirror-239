import datetime
import requests


class CodingNet:
    def __init__(self, token, team_id) -> None:
        self.token = token
        self.url = f"https://{team_id}.coding.net/open-api"

    def perform_commit_check(self, check_date):
        repos = self.get_repo_list()
        for repo in repos:
            commits = self.get_repo_commits(repo["Id"], check_date)
            if len(commits) == 0:
                continue
            print(f"Repo name: {repo['Name']}")
            print(f"Repo url: {repo['WebUrl']}")
            for commit in commits:
                date = datetime.datetime.fromtimestamp(commit["CommitDate"] / 1000)
                print(f"Commit author: {commit['AuthorName']}")
                print(f"Commit message: {commit['ShortMessage'].strip()}")
                print(f"Commit time: {date}\n")

    def get_repo_list(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        data = {
            "Action": "DescribeTeamDepotInfoList",
            "ProjectName": "",
            "PageNumber": 1,
            "PageSize": 500,
        }
        response = requests.post(url=self.url, headers=headers, json=data)
        data = response.json()
        return data["Response"]["DepotData"]["Depots"]

    def get_repo_commits(self, id, date):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        data = {
            "Action": "DescribeGitCommits",
            "DepotId": id,
            "PageNumber": 1,
            "PageSize": 100,
            "Ref": "master",
            "Path": "",
            "StartDate": date,
            "EndDate": date,
        }
        response = requests.post(url=self.url, headers=headers, json=data)
        data = response.json()
        return data["Response"]["Commits"]
