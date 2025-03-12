from dataclasses import dataclass
from typing import Final, Any
import asyncio
from aiohttp import ClientSession
from core.config import git_config, app_config
from datetime import datetime, timedelta
from collections import defaultdict

GITHUB_API_BASE_URL: Final[str] = "https://api.github.com"


@dataclass
class RepositoryAuthorCommitsNum:
    author: str
    commits_num: int


@dataclass
class Repository:
    name: str
    owner: str
    position: int
    stars: int
    watchers: int
    forks: int
    language: str
    authors_commits_num_today: list[RepositoryAuthorCommitsNum]


class GithubReposScrapper:
    def __init__(self, access_token: str, mcr: int, rps: int):
        self._session = ClientSession(
            headers={
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {access_token}",
            }
        )
        self._rps_delay = 1 / rps
        self._mcr = asyncio.Semaphore(mcr)

    async def _make_request(self, endpoint: str, method: str = "GET", params: dict[str, Any] | None = None) -> Any:
        await asyncio.sleep(self._rps_delay)
        async with self._mcr:
            async with self._session.request(method, f"{GITHUB_API_BASE_URL}/{endpoint}", params=params) as response:
                return await response.json()

    async def _get_top_repositories(self, limit: int = 100) -> list[dict[str, Any]]:
        """GitHub REST API: https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-repositories"""
        data = await self._make_request(
            endpoint="search/repositories",
            params={"q": "stars:>1", "sort": "stars", "order": "desc", "per_page": limit},
        )
        return data["items"]

    async def _get_repository_commits(self, owner: str, repo: str) -> list[dict[str, Any]]:
        """GitHub REST API: https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#list-commits"""
        since_date = (datetime.now() - timedelta(days=1)).isoformat()
        data = await self._make_request(
            endpoint=f"repos/{owner}/{repo}/commits",
            params={"since": since_date}
        )
        return data

    async def get_repositories(self) -> list[Repository]:
        repositories = await self._get_top_repositories()

        tasks = []
        for idx, repo in enumerate(repositories):
            tasks.append(self._get_commits_for_repository(repo, idx))

        results = await asyncio.gather(*tasks)
        return list(results)

    async def _get_commits_for_repository(self, repo_data: dict, position: int) -> Repository:
        owner = repo_data["owner"]["login"]
        repo_name = repo_data["name"]

        commits = await self._get_repository_commits(owner, repo_name)

        authors_commits = defaultdict(int)
        for commit in commits:
            author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
            authors_commits[author] += 1

        authors_commits_num_today = [
            RepositoryAuthorCommitsNum(author=author, commits_num=num)
            for author, num in authors_commits.items()
        ]

        return Repository(
            name=repo_name,
            owner=owner,
            position=position+1,
            stars=repo_data["stargazers_count"],
            watchers=repo_data["watchers_count"],
            forks=repo_data["forks_count"],
            language=repo_data["language"],
            authors_commits_num_today=authors_commits_num_today,
        )

    async def close(self):
        await self._session.close()


if __name__ == "__main__":
    async def main():
        scrapper = GithubReposScrapper(access_token=git_config.github_token,
                                       mcr=app_config.mcr,
                                       rps=app_config.rps
                                       )
        repositories = await scrapper.get_repositories()
        print(repositories)
        await scrapper.close()


    asyncio.run(main())
