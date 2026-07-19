#!/bin/bash

# Configuration
REPO_URL=$(git config --get remote.origin.url)
if [ -z "$REPO_URL" ]; then
    echo "Error: Could not detect origin git URL. Are you in a .git repository?"
    exit 1
fi

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Cloning skills from $REPO_URL..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR/repo" > /dev/null 2>&1 || { echo "Error: Git clone failed."; exit 1; }

# Define target paths - Using absolute path for Repo to be sure.
CURRENT_PWD=$(pwd)
PERSONAL_SKILLS_DIR="$HOME/.config/opencode/skills"
REPO_SKILLS_DIR="$CURRENT_PWD/.opencode/skills"

# Step 1: Ask for installation mode
echo "Select installation mode:"
options=("Personal (~/.config/opencode/skills)" "Repository (./.opencode/skills)")
select mode in "${options[@]}"; do
    case $mode in
        "Personal (~/.config/opencode/skills)")
            TARGET_DIR="$PERSONAL_SKILLS_DIR"
            break
            ;;
        "Repository (./.opencode/skills)")
            TARGET_DIR="$REPO_SKILLS_DIR"
            break
            ;;
        *) echo "Invalid option $REPLY";;
    esac
done

echo "Target directory set to: $TARGET_DIR"

# Step 2: List available skills
echo ""
echo "Available skills found in repository:"
SKILL_LIST=()

if [ ! -d "$TEMP_DIR/repo/skills" ]; then
    echo "Error: 'skills/' directory not found in the cloned repository."
    exit 1
fi

cd "$TEMP_DIR/repo/skills" || exit 1
for skill_dir in */; do
    skill_name=$(basename "$skill_dir")
    SKILL_LIST+=("$skill_name")
done

if [ ${#SKILL_LIST[@]} -eq 0 ]; then
    echo "No skills found in the repository."
    exit 1
fi

for i in "${!SKILL_LIST[@]}"; do
    printf "[%d] %s\n" "$i" "${SKILL_LIST[$i]}"
done

# Step 3: Select skills to install
echo ""
echo "Enter the numbers of the skills you want to install (separated by space), e'g., '0 2':"
read -r selected_indices

if [ -z "$selected_indices" ]; then
    echo "No skills selected. Exiting."
    exit 0
fi

# Step 4: Install selected skills
mkdir -p "$TARGET_DIR"

for idx in $selected_indices; do
    skill_name="${SKILL_LIST[$idx]}"
    if [ -n "$skill_name" ]; then
        echo "Installing skill: $skill_name -> $TARGET_DIR/$skill_name"
        cp -r "$TEMP_DIR/repo/skills/$skill_name" "$TARGET_DIR/"
    else
        echo "Invalid index: $idx. Skipping."
    fi
done

echo ""
echo "Installation complete!"
