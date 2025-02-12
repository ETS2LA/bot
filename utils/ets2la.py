import git
import os

download_folder = "assets/ets2la"
download_folder = os.path.join(os.getcwd(), download_folder)

def get_url_for_hash(hash: str):
    return f"https://github.com/ETS2LA/Euro-Truck-Simulator-2-Lane-Assist/commit/{hash}"

def get_ets2la_commits():
    try:
        repo = git.Repo(download_folder)
    except git.exc.InvalidGitRepositoryError:
        return []
    
    commits = list(repo.iter_commits())
    return commits

async def update_ets2la():
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    try:
        repo = git.Repo(download_folder)
    except git.exc.InvalidGitRepositoryError:
        print("Cloning repository")
        repo = git.Repo.clone_from("https://github.com/ETS2LA/Euro-Truck-Simulator-2-Lane-Assist", download_folder, multi_options=["--depth=20 --branch=rewrite --single-branch"])
        
    repo.remotes.origin.pull()
    
    return None