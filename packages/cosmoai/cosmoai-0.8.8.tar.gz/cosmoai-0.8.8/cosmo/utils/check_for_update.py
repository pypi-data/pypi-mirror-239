import pkg_resources
import requests
from packaging import version


def check_for_update():
    # Fetch the latest version from the PyPI API
    response = requests.get(f"https://pypi.org/project/cosmoai/json")
    latest_version = response.json()["info"]["version"]

    # Get the current version using pkg_resources
    current_version = pkg_resources.get_distribution("CosmoAI").version

    return version.parse(latest_version) > version.parse(current_version)
