import os
import re
import pytest
import requests
import yaml
from script2stlite.functions import get_value_of_max_key

ST版本_DIR = "stlite_versions"

def test_top_version_urls_are_valid():
    """
    Checks that the URL for the highest version in each YAML file
    in the stlite_versions directory is a valid and reachable URL.
    """
    version_files = [f for f in os.listdir(ST版本_DIR) if f.endswith(".yaml")]
    assert len(version_files) > 0, "No version files found in stlite_versions"

    for filename in version_files:
        filepath = os.path.join(ST版本_DIR, filename)
        with open(filepath, "r") as f:
            versions = yaml.safe_load(f)

        top_value = get_value_of_max_key(versions)

        # Extract URL from string if necessary
        match = re.search(r'https?://[^\s"]+', top_value)
        if match:
            top_url = match.group(0)
        else:
            top_url = top_value

        try:
            # Use a HEAD request to be efficient
            response = requests.head(top_url, timeout=20, allow_redirects=True)
            response.raise_for_status()  # Raises an exception for 4xx/5xx status codes
        except requests.exceptions.RequestException as e:
            pytest.fail(f"URL check failed for {top_url} in {filename}: {e}")
