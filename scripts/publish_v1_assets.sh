#!/usr/bin/env bash
# Add compatibility assets without replacing the original v2 release or files.
set -euo pipefail
: "${GH_TOKEN:?GitHub Actions token is required}"
: "${GH_REPO:?Repository is required}"
: "${RELEASE_TAG:?Compatibility tag is required}"
[[ "$RELEASE_TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+-v1$ ]]
target="v$(cat VERSION)"
[[ "$RELEASE_TAG" == "${target}-v1" ]]
[[ "$(gh release view "$target" --repo "$GH_REPO" --json isDraft --jq '.isDraft')" == false ]]
check_dir=$(mktemp -d)
trap 'rm -rf "$check_dir"' EXIT
# Verify that the existing release really contains this checkout's v2 artwork.
.release-venv/bin/python scripts/build_release.py --tag "$target" --output-dir "$check_dir/reference"
gh release download "$target" --repo "$GH_REPO" --dir "$check_dir" \
  --pattern "lvk-rabbit-${target}.zip" --pattern SHA256SUMS.txt
cmp "$check_dir/reference/lvk-rabbit-${target}.zip" "$check_dir/lvk-rabbit-${target}.zip"
cmp "$check_dir/reference/SHA256SUMS.txt" "$check_dir/SHA256SUMS.txt"
existing=$(gh release view "$target" --repo "$GH_REPO" --json assets --jq '.assets[].name')
for name in "lvk-rabbit-${target}-format-v1.zip" "lvk-rabbit-${target}-format-v1-petdex.zip" SHA256SUMS-v1.txt; do
  if grep -Fxq "$name" <<< "$existing"; then
    gh release download "$target" --repo "$GH_REPO" --dir "$check_dir" --pattern "$name"
    cmp "dist/$name" "$check_dir/$name"
  else
    gh release upload "$target" "dist/$name" --repo "$GH_REPO"
  fi
done
gh release edit "$target" --repo "$GH_REPO" --notes-file "releases/${target}.txt"
printf 'Added v1 compatibility packages to https://github.com/%s/releases/tag/%s; existing v2 assets preserved.\n' "$GH_REPO" "$target" >> "$GITHUB_STEP_SUMMARY"
