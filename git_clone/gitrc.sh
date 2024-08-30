#!/bin/bash

# Check if GitHub username and repository name are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <GitHub Username> <Repository Name> [<Local Path>]"
  exit 1
fi

# Assign variables
GITHUB_USERNAME=$1
REPO_NAME=$2
LOCAL_PATH=${3:-$(pwd)}

# Create the local directory for the repository if it doesn't exist
mkdir -p "$LOCAL_PATH/$REPO_NAME"

# Change to the local directory
cd "$LOCAL_PATH/$REPO_NAME" || { echo "Failed to change directory to $LOCAL_PATH/$REPO_NAME"; exit 1; }

# Initialize a new Git repository
git init

# Create a README file
echo "# $REPO_NAME" > README.md

# Add README to the repository
git add README.md
git commit -m "Initial commit with README"

# Create the remote repository using GitHub CLI
gh repo create "$GITHUB_USERNAME/$REPO_NAME" --public --source=. --remote=origin --push

# Print success message
echo "Repository $REPO_NAME created locally at $LOCAL_PATH/$REPO_NAME and on GitHub under $GITHUB_USERNAME."
