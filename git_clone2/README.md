# Bash Script to Automate Creating a New Remote and Local Repository

This script automates the process of creating a new remote GitHub repository and a local repository at the same time.

## Make the Script Globally Accessible

### Move the Script to a Directory in Your PATH

For example, move the script to `/usr/local/bin`:

```bash
sudo mv create_github_repo.sh /usr/local/bin/create_github_repo
sudo chmod +x /usr/local/bin/create_github_repo
```


By removing the .sh extension, you can call the script simply as create_github_repo.

Make Sure the Script is Executable
```bash
sudo chmod +x /usr/local/bin/create_github_repo
```

Add ~/bin to Your PATH (Optional)
If you prefer to place the script in ~/bin, make sure ~/bin is in your PATH. Add the following line to your shell configuration file (e.g., ~/.bashrc, ~/.bash_profile, ~/.zshrc):

```bash
export PATH="$HOME/bin:$PATH"
```
Then, move the script to ~/bin:

```bash
mkdir -p ~/bin
mv create_github_repo.sh ~/bin/create_github_repo
chmod +x ~/bin/create_github_repo
```
Reload your shell configuration:
```bash
source ~/.bashrc  # or ~/.bash_profile or ~/.zshrc depending on your shell
