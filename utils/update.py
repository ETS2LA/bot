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

def get_last_commit(repo_name: str = "ets2la"):
    try:
        repo = git.Repo(download_folder + "/" + repo_name)
    except git.exc.InvalidGitRepositoryError:
        return None
    
    return list(repo.iter_commits())[0]

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
        repo = git.Repo.clone_from(urls[repo_name], download_folder + "/" + repo_name, multi_options=["--depth=20 --single-branch"] if repo_name == "ets2la" else [])
        
    pull_result = repo.remotes.origin.pull()
    # pull_result is a list of FetchInfo objects now.  We need to check if
    # any changes were actually merged.
    for fetch_info in pull_result:
        if fetch_info.flags & git.FetchInfo.NEW_HEAD:
            # If the head moved locally, that indicates some changes have been applied
            return True
        if fetch_info.flags & git.FetchInfo.FAST_FORWARD:
            # A fast-forward merge is a pull
           return True
    return False
