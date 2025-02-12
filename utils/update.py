import git
import os

download_folder = "assets"
download_folder = os.path.join(os.getcwd(), download_folder)

urls = {
    "ets2la": "https://github.com/ETS2LA/Euro-Truck-Simulator-2-Lane-Assist",
    "translations": "https://github.com/ETS2LA/translations"
}

def get_url_for_hash(hash: str, repo: str = "ets2la"):
    url = urls[repo]
    return f"{url}/commit/{hash}"

def get_commits_for(repo_name: str = "ets2la"):
    try:
        repo = git.Repo(download_folder + "/" + repo_name)
    except git.exc.InvalidGitRepositoryError:
        return []
    
    commits = list(repo.iter_commits())
    return commits

async def update_repo(repo_name: str = "ets2la"):
    if not os.path.exists(download_folder + "/" + repo_name):
        os.makedirs(download_folder + "/" + repo_name)

    try:
        repo = git.Repo(download_folder + "/" + repo_name)
    except git.exc.InvalidGitRepositoryError:
        print("Cloning repository")
        repo = git.Repo.clone_from(urls[repo_name], download_folder + "/" + repo_name, multi_options=["--depth=20 --branch=rewrite --single-branch"] if repo_name == "ets2la" else [])
        
    repo.remotes.origin.pull()
    
    return None