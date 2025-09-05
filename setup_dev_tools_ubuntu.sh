#!/bin/bash

# Ubuntu Developer Tools Setup Script
# This script installs essential development tools on Ubuntu

set -e  # Exit on any error

echo "🚀 Setting up Ubuntu Developer Tools..."

# Update package list
echo "📦 Updating package list..."
sudo apt update

# Essential system tools
echo "🔧 Installing essential system tools..."
sudo apt install -y \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    tree \
    unzip \
    zip \
    jq \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Git configuration (you'll need to set these manually)
echo "📝 Git configuration needed:"
echo "Run these commands after installation:"
echo "git config --global user.name 'Your Name'"
echo "git config --global user.email 'your.email@example.com'"

# Python development tools
echo "🐍 Installing Python development tools..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools

# Node.js (using NodeSource repository for latest LTS)
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Docker
echo "🐳 Installing Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add current user to docker group
sudo usermod -aG docker $USER

# VS Code (optional - uncomment if needed)
# echo "💻 Installing VS Code..."
# wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
# sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
# sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
# sudo apt update
# sudo apt install -y code

# Additional useful tools
echo "🛠️ Installing additional useful tools..."
sudo apt install -y \
    tmux \
    screen \
    neofetch \
    bat \
    fd-find \
    ripgrep \
    fzf \
    zsh \
    powerline \
    fonts-powerline

# Install Oh My Zsh (optional)
echo "🎨 Setting up Oh My Zsh..."
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Install useful Python packages globally
echo "📚 Installing useful Python packages..."
pip3 install --user \
    pipenv \
    virtualenv \
    black \
    flake8 \
    pytest \
    requests \
    numpy \
    pandas

# Install useful Node.js packages globally
echo "📦 Installing useful Node.js packages..."
npm install -g \
    npm \
    yarn \
    nodemon \
    typescript \
    ts-node \
    eslint \
    prettier

# Create useful aliases
echo "⚡ Setting up useful aliases..."
cat >> ~/.bashrc << 'EOF'

# Custom aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias h='history'
alias c='clear'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias ps='ps aux'
alias top='htop'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# Docker aliases
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias di='docker images'
alias dex='docker exec -it'

EOF

# Add aliases to zsh if it exists
if [ -f ~/.zshrc ]; then
    cat >> ~/.zshrc << 'EOF'

# Custom aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias h='history'
alias c='clear'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias ps='ps aux'
alias top='htop'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# Docker aliases
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias di='docker images'
alias dex='docker exec -it'

EOF
fi

echo ""
echo "✅ Developer tools setup complete!"
echo ""
echo "📋 What was installed:"
echo "  • Essential tools: git, curl, wget, vim, nano, htop, tree, jq"
echo "  • Build tools: build-essential, software-properties-common"
echo "  • Python: python3, pip, venv, dev tools"
echo "  • Node.js: Latest LTS version with npm"
echo "  • Docker: Docker CE with compose plugin"
echo "  • Additional tools: tmux, screen, neofetch, bat, fd, ripgrep, fzf"
echo "  • Shell: zsh with Oh My Zsh"
echo "  • Python packages: pipenv, virtualenv, black, flake8, pytest, etc."
echo "  • Node.js packages: yarn, nodemon, typescript, eslint, prettier"
echo "  • Useful aliases for git, docker, and common commands"
echo ""
echo "🔄 Next steps:"
echo "  1. Restart your terminal or run: source ~/.bashrc"
echo "  2. Configure git: git config --global user.name 'Your Name'"
echo "  3. Configure git: git config --global user.email 'your.email@example.com'"
echo "  4. Log out and back in to use Docker without sudo"
echo "  5. Optional: Install VS Code by uncommenting the VS Code section in this script"
echo ""
echo "🎉 Happy coding!"
