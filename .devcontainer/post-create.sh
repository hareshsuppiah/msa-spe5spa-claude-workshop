#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Python libraries"
pip install --quiet pandas matplotlib seaborn python-telegram-bot python-dotenv

echo "==> Installing R libraries"
R --quiet -e "install.packages(c('tidyverse','jsonlite'), repos='https://cloud.r-project.org')" >/dev/null

echo "==> Installing Typst (for standardised PDF reports)"
curl -fsSL https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz -o /tmp/typst.tar.xz
sudo tar -xJf /tmp/typst.tar.xz -C /opt
sudo ln -sf /opt/typst-x86_64-unknown-linux-musl/typst /usr/local/bin/typst
rm /tmp/typst.tar.xz
typst --version

echo "==> Installing Claude Code CLI"
curl -fsSL https://claude.ai/install.sh | bash || true

echo "==> Done. Run 'claude' to start Claude Code, or open any module README to begin."
