from dataclasses import dataclass
import os

@dataclass
class Asset:
    name: str
    url: str
    clone_options: str
    path: str

    def __init__(self, name: str, url: str, root_path: str, clone_options: str = None) -> None:
        self.name = name
        self.url = url
        self.clone_options = clone_options
        self.path = os.path.join(root_path, name)

def get_asset_with_name(name: str, assets: list[Asset]):
    for asset in assets:
        if asset.name == name:
            return asset
    return None