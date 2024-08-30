#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 <sub_repo_url> <remote_repo_url> <folder_name>"
    echo "  <sub_repo_url> should be the URL of the repository you want to clone."
    echo "  <remote_repo_url> should be the URL of the repository where you want to push the cloned repository."
    echo "  <folder_name> is the name of the folder in the remote repository where the cloned repo will be placed."
    exit 1
}

# Check if exactly three arguments are provided
if [ "$#" -ne 3 ]; then
    usage
fi

# Assign arguments to variables
sub_repo_url=$1
remote_repo_url=$2
folder_name=$3

# Extract the repository name from the URL
repo_name=$(basename "$sub_repo_url" .git)
temp_dir=$(mktemp -d)

# Function to clone a repository
clone_repo() {
    local repo_url=$1
    local target_dir=$2
    echo "Cloning $repo_url into $target_dir"
    git clone "$repo_url" "$target_dir"
}

# Function to push a repository to a new remote
push_to_remote() {
    local repo_dir=$1
    local remote_url=$2
    local target_folder=$3

    echo "Pushing $repo_dir to $remote_url into folder $target_folder"
    
    # Clone the target repository to a temporary directory
    temp_target_dir=$(mktemp -d)
    git clone "$remote_url" "$temp_target_dir"
    
    cd "$temp_target_dir" || exit
    
    # Create the folder for the moved repository
    mkdir -p "$target_folder"
    
    # Remove any existing content in the target folder
    rm -rf "$target_folder/*"
    
    # Copy the cloned repository into the new folder
    cp -r "$repo_dir"/* "$target_folder/"
    
    # Add and commit the changes
    git add "$target_folder"
    git commit -m "Add $repo_name repository into $target_folder"
    
    # Detect the default branch name in the remote repository
    default_branch=$(git remote show origin | awk '/HEAD branch/ {print $NF}')
    
    # If default branch is not detected, use 'master'
    if [ -z "$default_branch" ]; then
        default_branch="master"
    fi
    
    # Push changes to the remote repository
    git push -u origin "$default_branch"
    
    # Clean up temporary target directory
    cd ..
    rm -rf "$temp_target_dir"
}

# Clone the sub-repository into a temporary directory
clone_repo "$sub_repo_url" "$temp_dir/$repo_name"

# Push the cloned repository to the specified remote repository
push_to_remote "$temp_dir/$repo_name" "$remote_repo_url" "$folder_name"

# Clean up the temporary directory
rm -rf "$temp_dir"

echo "The repository has been cloned, moved into $folder_name, and pushed successfully."
