import requests


def get_github_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_repository_contributors(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def display_repository_info(repositories):
    if repositories:
        print("GitHub Repositories:")
        for repo in repositories:
            print(f"Name: {repo['name']}")
            print(f"Description: {repo['description'] or 'N/A'}")
            print(f"URL: {repo['html_url']}")
            print(f"Language: {repo['language'] or 'N/A'}")
            print(f"Stars: {repo['stargazers_count']}")

            contributors = get_repository_contributors(repo['owner']['login'], repo['name'])
            if contributors:
                print("Contributors:")
                for contributor in contributors:
                    print(f"- {contributor['login']} ({contributor['contributions']} contributions)")
            else:
                print("Unable to fetch contributors.")

            print("----------")
    else:
        print("Unable to fetch GitHub repositories.")


if __name__ == "__main__":
    # Replace 'Username' with your actual GitHub username
    github_username = 'Usernname'

    repositories = get_github_repositories(github_username)
    display_repository_info(repositories)
