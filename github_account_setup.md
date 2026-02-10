# Managing Multiple GitHub Accounts

## Overview

This guide shows how to set up and switch between multiple GitHub accounts on the same machine.

## Method 1: Per-Repository Configuration (Recommended)

### Setup Different Accounts for Different Repos

Each repository can use a different GitHub account without changing global settings.

```bash
# Navigate to your repository
cd /path/to/jam-wifi-control

# Set account for THIS repository only
git config user.name "Adam Vegh"
git config user.email "adam@example.com"  # Your adamvegh email

# Verify
git config user.name
git config user.email
```

### For Your Other Repos (Different Account)

```bash
# In another repository
cd /path/to/other/repo

# Set different account
git config user.name "Your Other Name"
git config user.email "other@example.com"
```

## Method 2: SSH Keys for Multiple Accounts

### Step 1: Generate SSH Keys for Each Account

```bash
# Generate key for adamvegh account
ssh-keygen -t ed25519 -C "adam@example.com" -f ~/.ssh/id_ed25519_adamvegh

# Generate key for other account
ssh-keygen -t ed25519 -C "other@example.com" -f ~/.ssh/id_ed25519_other
```

### Step 2: Add SSH Keys to SSH Agent

```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add keys
ssh-add ~/.ssh/id_ed25519_adamvegh
ssh-add ~/.ssh/id_ed25519_other
```

### Step 3: Add SSH Keys to GitHub Accounts

For each account:

1. Copy public key:
   ```bash
   cat ~/.ssh/id_ed25519_adamvegh.pub
   # Copy the output
   ```

2. Go to GitHub.com → Settings → SSH and GPG keys → New SSH key
3. Paste the public key
4. Repeat for each account

### Step 4: Configure SSH Config

Create/edit `~/.ssh/config`:

```bash
# Account 1: adamvegh
Host github-adamvegh
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_adamvegh
  IdentitiesOnly yes

# Account 2: other account
Host github-other
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_other
  IdentitiesOnly yes
```

### Step 5: Use Correct Host When Cloning/Adding Remote

```bash
# For adamvegh account
git remote add origin git@github-adamvegh:adamvegh/jam-wifi-control.git

# For other account
git remote add origin git@github-other:otheraccount/repo-name.git
```

## Method 3: Personal Access Tokens (HTTPS)

### Step 1: Create Personal Access Tokens

For each GitHub account:

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (full control)
4. Copy the token (you won't see it again!)

### Step 2: Use Token When Pushing

```bash
# Clone with HTTPS
git clone https://github.com/adamvegh/jam-wifi-control.git

# When pushing, you'll be prompted for credentials
Username: adamvegh
Password: <paste-your-personal-access-token>

# Or set remote URL with token (less secure, token visible)
git remote set-url origin https://adamvegh:<TOKEN>@github.com/adamvegh/jam-wifi-control.git
```

### Step 3: Use Git Credential Manager (Recommended for HTTPS)

```bash
# Configure credential helper
git config --global credential.helper osxkeychain  # macOS
git config --global credential.helper manager      # Windows
git config --global credential.helper store        # Linux

# First push will prompt for token, then it's saved
```

## Method 4: Helper Script (Easy Switching)

Create a script to quickly switch accounts:

```bash
#!/bin/bash
# ~/.local/bin/git-account-switch

case "$1" in
  adamvegh)
    git config user.name "Adam Vegh"
    git config user.email "adam@example.com"
    echo "✅ Switched to adamvegh account"
    ;;
  work)
    git config user.name "Work Name"
    git config user.email "work@company.com"
    echo "✅ Switched to work account"
    ;;
  personal)
    git config user.name "Personal Name"
    git config user.email "personal@example.com"
    echo "✅ Switched to personal account"
    ;;
  *)
    echo "Usage: git-account-switch [adamvegh|work|personal]"
    echo "Current config:"
    echo "  Name:  $(git config user.name)"
    echo "  Email: $(git config user.email)"
    ;;
esac
```

Make it executable:
```bash
chmod +x ~/.local/bin/git-account-switch
```

Usage:
```bash
cd /path/to/jam-wifi-control
git-account-switch adamvegh
```

## Recommended Setup for This Project

### 1. Use SSH with Multiple Keys (Most Secure)

```bash
# Generate SSH key for adamvegh
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519_adamvegh

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519_adamvegh

# Copy public key and add to GitHub
cat ~/.ssh/id_ed25519_adamvegh.pub
# Add this to github.com/settings/keys
```

### 2. Configure SSH Config

Add to `~/.ssh/config`:
```
Host github-adamvegh
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_adamvegh
  IdentitiesOnly yes
```

### 3. Set Repository Config

```bash
cd /path/to/jam-wifi-control

# Set user for this repo
git config user.name "Adam Vegh"
git config user.email "your-adamvegh-email@example.com"

# Set remote with SSH
git remote add origin git@github-adamvegh:adamvegh/jam-wifi-control.git
```

### 4. Push to GitHub

```bash
git push -u origin main
```

## Quick Reference

### Check Current Account

```bash
# In any repository
git config user.name
git config user.email

# Check global config
git config --global user.name
git config --global user.email
```

### Switch Account for Current Repo

```bash
git config user.name "New Name"
git config user.email "new@example.com"
```

### List All Git Configs

```bash
# Repository-specific
git config --list --local

# Global
git config --list --global
```

## Troubleshooting

### "Permission denied" when pushing

**Issue:** Using wrong SSH key

**Fix:**
```bash
# Test SSH connection
ssh -T git@github-adamvegh

# Should see: "Hi adamvegh! You've successfully authenticated"
```

### "Could not read from remote repository"

**Issue:** Wrong remote URL

**Fix:**
```bash
# Check current remote
git remote -v

# Update to correct host
git remote set-url origin git@github-adamvegh:adamvegh/jam-wifi-control.git
```

### Commits showing wrong author

**Issue:** Global config overriding local

**Fix:**
```bash
# Set local config (overrides global)
git config user.name "Adam Vegh"
git config user.email "adam@example.com"

# Amend last commit with new author
git commit --amend --reset-author --no-edit
```

## Best Practices

1. ✅ **Use SSH keys** - More secure than passwords/tokens
2. ✅ **Per-repo config** - Set user per repository, not globally
3. ✅ **Different emails** - Each account should have unique email
4. ✅ **Test before pushing** - Use `ssh -T git@github-adamvegh` to verify
5. ✅ **Document your accounts** - Keep list of which repos use which account

## Summary

**For this jam-wifi-control project:**

```bash
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your-email" -f ~/.ssh/id_ed25519_adamvegh

# 2. Add to GitHub (github.com/settings/keys)
cat ~/.ssh/id_ed25519_adamvegh.pub

# 3. Configure this repo
cd /path/to/jam-wifi-control
git config user.name "Adam Vegh"
git config user.email "your-email@example.com"

# 4. Set remote
git remote add origin git@github-adamvegh:adamvegh/jam-wifi-control.git

# 5. Push
git push -u origin main
```

Done! This repo will always use the adamvegh account. Other repos can use different accounts.
