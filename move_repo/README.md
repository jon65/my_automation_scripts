Git Repository Cloner and Pusher
This script clones a Git repository from a given URL and pushes its contents into a specified folder of a target Git repository.

Features
Clones a repository from a provided URL.
Creates a new folder in a target repository and moves the cloned repository's contents into it.
Handles different default branch names in the remote repository.
Cleans up temporary files after the operation.
Prerequisites
Git must be installed on your system.
You need to have access rights to both the source and target repositories.
Usage
To use the script, run:

bash
Copy code
./git_move_rp.sh <sub_repo_url> <remote_repo_url> <folder_name>
<sub_repo_url>: The URL of the repository you want to clone (e.g., https://github.com/user/source-repo.git).
<remote_repo_url>: The URL of the target repository where the contents will be pushed (e.g., https://github.com/user/target-repo.git).
<folder_name>: The name of the folder in the target repository where the cloned repository will be placed.
Example
bash
Copy code
./git_move_rp.sh https://github.com/example/source-repo.git https://github.com/example/target-repo.git myfolder
In this example, the source-repo repository will be cloned and its contents will be pushed into the myfolder directory of the target-repo repository.

Script Details
Cloning:

The script clones the repository specified by <sub_repo_url> into a temporary directory.
Pushing:

The script clones the target repository specified by <remote_repo_url> into another temporary directory.
Creates a new folder inside the target repository.
Copies the contents from the cloned source repository into this new folder.
Commits the changes and pushes them to the target repository.
Branch Handling:

The script detects the default branch of the target repository and pushes changes to that branch. If the default branch is not detected, it defaults to master.
Cleanup:

Temporary directories are removed after the operation is complete.
Troubleshooting
Error: src refspec main does not match any: This indicates that the branch main does not exist in your local repository. Ensure that the default branch name is correctly detected, or check if the remote repository uses a different default branch name.

Error: Permission denied: Ensure that you have the necessary permissions to access and push to both the source and target repositories.

