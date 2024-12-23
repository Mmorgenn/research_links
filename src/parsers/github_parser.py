import requests
import collections
import asyncio
from collections import Counter
from aiohttp import ClientSession


url = "https://api.github.com/users/MMorgenn"
#user_data = requests.get(url).json()
#print(user_data)

USER_URL = "https://api.github.com/users/{}"
REPOS_URL = "https://api.github.com/users/{}/repos"


class GithubPars:

    def __init__(self, user: str) -> None:
        self.user = user

    @staticmethod
    def get_popular_repos(repos: list[dict[str, str]]) -> str | None:
        if not repos:
            return None
        sorted_repos = sorted(repos, key=lambda d: d["stargazers_count"])
        return sorted_repos[0].get("html_url")

    @staticmethod
    def get_popular_language(repos: list[dict[str, str]]) -> str | None:
        repos_url = [repos[i].get("languages_url", None) for i in range(len(repos))]
        languages_counter: Counter = Counter(dict())
        for url in repos_url:
            if not isinstance(url, str):
                continue
            data = requests.get(url)
            if data.status_code == 200:
                languages = data.json()
                languages = dict(zip(languages.keys(), [val / sum(languages.values()) for val in languages.values()]))
                languages_counter.update(languages)
            else:
                print(data.json())
        return languages_counter.most_common(1)[0][0]

    @staticmethod
    def get_company(user_profile: dict[str, str]) -> str | None:
        return user_profile.get("company")

    def get_info(self) -> dict[str, str | None] | None:
        data = requests.get(USER_URL.format(self.user))
        if data.status_code != 200:
            return None
        user_profile = data.json()
        repos_data = requests.get(REPOS_URL.format(self.user)).json()
        company = self.get_company(user_profile)
        language = self.get_popular_language(repos_data)
        popular_repos = self.get_popular_repos(repos_data)
        return {
            "company": company,
            "language": language,
            "popular_repos": popular_repos
        }
