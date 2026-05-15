#!/bin/bash
# Reusable git workflow functions for AI workflows

# Create a branch with the specified prefix and GitHub run ID
# Usage: create_branch <prefix>
create_branch() {
    local prefix="$1"
    local branch="${prefix}/${GITHUB_RUN_ID}"
    git checkout -b "$branch"
    echo "BRANCH=$branch" >> $GITHUB_ENV
}

# Configure git user for AI commits
configure_git() {
    git config user.name "Ardent AI"
    git config user.email "ardent-ai@users.noreply.github.com"
}

# Check if there are staged changes
# Returns 0 if there are changes, 1 if no changes
has_changes() {
    git diff --cached --quiet
    return $?
}

# Stage all files, commit with message, and push to branch
# Usage: commit_and_push <branch_name> <commit_message>
commit_and_push() {
    local branch_name="$1"
    local commit_message="$2"
    
    git add .
    if has_changes; then
        echo "NO_CHANGES=true" >> $GITHUB_ENV
        return 0
    fi
    git commit -m "$commit_message" || echo "No changes to commit"
    git push origin "$branch_name"
}

# Create a pull request using gh CLI
# Usage: create_pr <branch_name> <title> <body>
create_pr() {
    local branch_name="$1"
    local title="$2"
    local body="${3:-}"
    
    if [ -n "$body" ]; then
        gh pr create \
            --base main \
            --head "$branch_name" \
            --title "$title" \
            --body "$body"
    else
        gh pr create \
            --base main \
            --head "$branch_name" \
            --title "$title"
    fi
}
