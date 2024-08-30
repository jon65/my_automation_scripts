#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 <sub_repo_url> <remote_repo_url>"
    echo "  <sub_repo_url> should be the URL of the repository you want to clone."
    echo "  <remote_repo_url> should be the URL of the repository where you want to push the cloned repository."
    exit 1
}

# Check if exactly two arguments are provided
if [ "$#" -ne 2 ]; then
    usage
fi

# Assign arguments to variables
sub_repo_url=$1
remote_repo_url=$2

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
    echo "Pushing $repo_dir to $remote_url"
    cd "$repo_dir" || exit
    git remote remove origin
    git remote add origin "$remote_url"
    git push -u origin master
}

# Clone the sub-repository into a temporary directory
clone_repo "$sub_repo_url" "$temp_dir/$repo_name"

# Push the cloned repository to the specified remote repository
push_to_remote "$temp_dir/$repo_name" "$remote_repo_url"

# Clean up the temporary directory
rm -rf "$temp_dir"

echo "The repository has been cloned and pushed successfully."
