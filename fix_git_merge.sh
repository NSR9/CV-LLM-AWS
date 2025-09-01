#!/bin/bash

# Git Merge Conflict Resolution Script
# This script helps resolve the "unrelated histories" issue

set -e

echo "🔧 Git Merge Conflict Resolution Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "Not in a git repository. Please run this script from the CV-LLM-AWS directory."
    exit 1
fi

echo ""
echo "Current situation:"
echo "=================="
git status --short
echo ""

echo "Available options to resolve the merge conflict:"
echo "================================================"
echo "1. Merge with unrelated histories (recommended if you want to keep local changes)"
echo "2. Reset to remote branch (will discard local changes)"
echo "3. Create a backup and start fresh"
echo "4. Manual resolution"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
    1)
        print_status "Attempting to merge with unrelated histories..."
        if git pull origin clean-dev --allow-unrelated-histories; then
            print_success "Successfully merged with unrelated histories!"
        else
            print_error "Merge failed. You may need to resolve conflicts manually."
            exit 1
        fi
        ;;
    2)
        print_warning "This will discard all local changes. Are you sure? (y/N)"
        read -p "" confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            print_status "Resetting to remote clean-dev branch..."
            git fetch origin clean-dev
            git reset --hard origin/clean-dev
            print_success "Reset completed successfully!"
        else
            print_status "Operation cancelled."
            exit 0
        fi
        ;;
    3)
        print_status "Creating backup of current state..."
        backup_dir="../CV-LLM-AWS-backup-$(date +%Y%m%d-%H%M%S)"
        cp -r . "$backup_dir"
        print_success "Backup created at: $backup_dir"
        
        print_status "Removing current repository and cloning fresh..."
        cd ..
        rm -rf CV-LLM-AWS
        git clone -b clean-dev https://github.com/NSR9/CV-LLM-AWS.git
        cd CV-LLM-AWS
        print_success "Fresh clone completed!"
        ;;
    4)
        print_status "Manual resolution mode..."
        echo ""
        echo "Current branch: $(git branch --show-current)"
        echo "Remote branches:"
        git branch -r
        echo ""
        echo "You can now manually resolve the conflict using:"
        echo "  git fetch origin clean-dev"
        echo "  git merge origin/clean-dev --allow-unrelated-histories"
        echo "  # Resolve any conflicts, then:"
        echo "  git add ."
        echo "  git commit -m 'Merge remote clean-dev branch'"
        exit 0
        ;;
    *)
        print_error "Invalid option. Please choose 1-4."
        exit 1
        ;;
esac

echo ""
print_success "Git conflict resolved!"
echo "Current status:"
git status --short
