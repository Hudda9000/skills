#!/usr/bin/env bash
set -e

# Ensure npm token is available or handled via .npmrc as we did before
# The environment should already have NPM_TOKEN if the user set it up

echo "🚀 Starting release process..."

# 1. Bump version (patch)
echo "📦 Bumping version..."
npm version patch -m "chore: release %s"

# 2. Push changes and tags to git
echo "📤 Pushing to git..."
git push origin main --tags

# 3. Publish to npm
echo "🌐 Publishing to npm..."
npm publish --access public

echo "✅ Release successful! 🎉"
