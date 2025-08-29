import utils.variables as variables
from utils.classes import Asset

import logging
import git.exc
import logging
import git
import os

logger = logging.getLogger()

def get_url_for_hash(hash: str, asset: Asset):
    return f"{asset.url}/commit/{hash}"

def get_last_commit(asset: Asset) -> git.Commit:
    try:
        repo = git.Repo(asset.path)
    except git.exc.InvalidGitRepositoryError:
        return None
    
    return list(repo.iter_commits())[0]

def get_commit_by_hash(hash: str, asset: Asset) -> git.Commit:
    try:
        repo = git.Repo(asset.path)
    except git.exc.InvalidGitRepositoryError:
        return None

    return repo.commit(hash)

def get_commits_for(asset: Asset):
    try:
        repo = git.Repo(asset.path)
    except git.exc.InvalidGitRepositoryError:
        return []
    
    commits = list(repo.iter_commits())
    return commits

async def update_repo(asset: Asset):
    if not os.path.exists(asset.path):
        os.makedirs(asset.path)

    try:
        repo = git.Repo(asset.path)
    except git.exc.InvalidGitRepositoryError:
        logger.info(f"Cloning {asset.name}...")
        repo = git.Repo.clone_from(asset.url, asset.path, multi_options=[asset.clone_options] if asset.clone_options else None)
        logger.info(f"Cloned {asset.name}")
        
    pull_result = repo.remotes.origin.pull()
    # pull_result is a list of FetchInfo objects now. We need to check if
    # any changes were actually merged.
    for fetch_info in pull_result:
        if fetch_info.flags & git.FetchInfo.NEW_HEAD:
            # If the head moved locally, that indicates some changes have been applied
            logger.info(f"An update has been applied to {asset.name} (New Head)")
            return True
        if fetch_info.flags & git.FetchInfo.FAST_FORWARD:
            # A fast-forward merge is a pull
            logger.info(f"An update has been applied to {asset.name} (Fast Forward)")
            return True
    return False