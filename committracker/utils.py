import tempfile
import shutil
from git import Repo
import logging

def clone_remote_repo(url):
    temp_dir = tempfile.mkdtemp()
    try:
        Repo.clone_from(url, temp_dir)
        logging.info("Repository cloned successfully.")
        return temp_dir
    except Exception as e:
        logging.error(f"Cloning failed: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None
