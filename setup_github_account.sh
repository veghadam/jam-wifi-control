#!/bin/bash
# Setup GitHub account for this repository

echo "======================================================================"
echo "GitHub Account Setup for jam-wifi-control"
echo "======================================================================"
echo

# Get current config
CURRENT_NAME=$(git config user.name 2>/dev/null)
CURRENT_EMAIL=$(git config user.email 2>/dev/null)

if [ -n "$CURRENT_NAME" ]; then
    echo "Current repository configuration:"
    echo "  Name:  $CURRENT_NAME"
    echo "  Email: $CURRENT_EMAIL"
    echo
fi

# Prompt for account details
echo "Enter your GitHub account details for THIS repository:"
echo

read -p "GitHub Username (e.g., adamvegh): " USERNAME
read -p "Your Name: " NAME
read -p "Your Email: " EMAIL

# Set repository config
git config user.name "$NAME"
git config user.email "$EMAIL"

echo
echo "✅ Repository configured!"
echo "  Name:  $(git config user.name)"
echo "  Email: $(git config user.email)"
echo

# Check if SSH key exists
SSH_KEY="$HOME/.ssh/id_ed25519_$USERNAME"

if [ ! -f "$SSH_KEY" ]; then
    echo "======================================================================"
    echo "SSH Key Setup"
    echo "======================================================================"
    echo
    echo "Would you like to create an SSH key for this account?"
    read -p "(yes/no): " CREATE_KEY

    if [ "$CREATE_KEY" = "yes" ] || [ "$CREATE_KEY" = "y" ]; then
        ssh-keygen -t ed25519 -C "$EMAIL" -f "$SSH_KEY"

        echo
        echo "✅ SSH key created at: $SSH_KEY"
        echo

        # Add to SSH agent
        eval "$(ssh-agent -s)"
        ssh-add "$SSH_KEY"

        echo
        echo "======================================================================"
        echo "Add this public key to GitHub:"
        echo "======================================================================"
        echo
        echo "1. Copy this key:"
        echo
        cat "${SSH_KEY}.pub"
        echo
        echo "2. Go to: https://github.com/settings/keys"
        echo "3. Click 'New SSH key'"
        echo "4. Paste the key above"
        echo

        read -p "Press Enter when you've added the key to GitHub..."

        # Test SSH connection
        echo
        echo "Testing SSH connection..."
        ssh -T git@github.com 2>&1 | head -1

        # Add SSH config
        SSH_CONFIG="$HOME/.ssh/config"
        if ! grep -q "Host github-$USERNAME" "$SSH_CONFIG" 2>/dev/null; then
            echo
            echo "Would you like to add SSH config for easy usage?"
            read -p "(yes/no): " ADD_CONFIG

            if [ "$ADD_CONFIG" = "yes" ] || [ "$ADD_CONFIG" = "y" ]; then
                echo "" >> "$SSH_CONFIG"
                echo "# Account: $USERNAME" >> "$SSH_CONFIG"
                echo "Host github-$USERNAME" >> "$SSH_CONFIG"
                echo "  HostName github.com" >> "$SSH_CONFIG"
                echo "  User git" >> "$SSH_CONFIG"
                echo "  IdentityFile $SSH_KEY" >> "$SSH_CONFIG"
                echo "  IdentitiesOnly yes" >> "$SSH_CONFIG"

                echo "✅ SSH config added"
                echo
                echo "Use this remote URL:"
                echo "  git@github-$USERNAME:$USERNAME/jam-wifi-control.git"
            fi
        fi
    fi
else
    echo "✅ SSH key already exists: $SSH_KEY"
fi

echo
echo "======================================================================"
echo "Next Steps"
echo "======================================================================"
echo

# Check if remote exists
if git remote get-url origin 2>/dev/null; then
    echo "Current remote:"
    git remote -v
    echo
    echo "To update remote to use your account:"
    echo "  git remote set-url origin git@github-$USERNAME:$USERNAME/jam-wifi-control.git"
else
    echo "To add remote:"
    if [ -f "$SSH_KEY" ] && grep -q "Host github-$USERNAME" "$HOME/.ssh/config" 2>/dev/null; then
        echo "  git remote add origin git@github-$USERNAME:$USERNAME/jam-wifi-control.git"
    else
        echo "  git remote add origin https://github.com/$USERNAME/jam-wifi-control.git"
    fi
fi

echo
echo "To push to GitHub:"
echo "  git push -u origin main"
echo

echo "======================================================================"
echo "✅ Setup complete!"
echo "======================================================================"
