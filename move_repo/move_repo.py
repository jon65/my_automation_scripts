import os
import subprocess
import sys

def clone_repo(repo_url, target_dir):
    """Clone a repository into a specific directory."""
    if not os.path.exists(target_dir):
        print(f"Cloning {repo_url} into {target_dir}")
        subprocess.run(['git', 'clone', repo_url, target_dir], check=True)
    else:
        print(f"Directory {target_dir} already exists. Skipping clone.")

def add_subdir_to_repo(repo_path, subdir_name):
    """Add a subdirectory to the specified repository."""
    print(f"Adding {subdir_name} to {repo_path}")
    os.chdir(repo_path)
    subprocess.run(['git', 'add', subdir_name], check=True)
    subprocess.run(['git', 'commit', '-m', f'Add {subdir_name} subdirectory'], check=True)
    print(f"{subdir_name} has been added to {repo_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python clone_and_add_repos.py <parent_repo_path> <sub_repo_url> [<sub_repo_url2> ...]")
        sys.exit(1)

    parent_repo_path = sys.argv[1]
    sub_repo_urls = sys.argv[2:]

    if not os.path.isdir(parent_repo_path):
        print(f"Parent repository directory {parent_repo_path} does not exist.")
        sys.exit(1)

    for repo_url in sub_repo_urls:
        repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        target_dir = os.path.join(parent_repo_path, repo_name)
        clone_repo(repo_url, target_dir)
        add_subdir_to_repo(parent_repo_path, repo_name)

if __name__ == "__main__":
    main()
