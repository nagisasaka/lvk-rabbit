#!/usr/bin/env bash
set -euo pipefail
: "${GH_TOKEN:?GitHub Actions token is required}"
: "${GH_REPO:?Repository is required}"
: "${RELEASE_TAG:?Release tag is required}"
[[ "$RELEASE_TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]
[[ "$RELEASE_TAG" == "v$(cat VERSION)" ]]
archive="dist/lvk-rabbit-${RELEASE_TAG}.zip"
notes="releases/${RELEASE_TAG}.txt"

if draft=$(gh release view "$RELEASE_TAG" --repo "$GH_REPO" --json isDraft --jq '.isDraft'); then
  if [[ "$draft" != true ]]; then
    # A successful rerun verifies published bytes instead of overwriting them.
    check_dir=$(mktemp -d)
    trap 'rm -rf "$check_dir"' EXIT
    gh release download "$RELEASE_TAG" --repo "$GH_REPO" --dir "$check_dir" \
      --pattern "lvk-rabbit-${RELEASE_TAG}.zip" --pattern SHA256SUMS.txt
    cmp "$archive" "$check_dir/lvk-rabbit-${RELEASE_TAG}.zip"
    cmp dist/SHA256SUMS.txt "$check_dir/SHA256SUMS.txt"
    echo "Published assets already match; no changes made."
    exit 0
  fi
  gh release upload "$RELEASE_TAG" "$archive" dist/SHA256SUMS.txt --repo "$GH_REPO" --clobber
  gh release edit "$RELEASE_TAG" --repo "$GH_REPO" --title "LVK Rabbit ${RELEASE_TAG}" --notes-file "$notes"
else
  gh release create "$RELEASE_TAG" "$archive" dist/SHA256SUMS.txt \
    --repo "$GH_REPO" --verify-tag --draft --title "LVK Rabbit ${RELEASE_TAG}" --notes-file "$notes"
fi
# Assets are attached before publication, including when immutable releases are enabled.
gh release edit "$RELEASE_TAG" --repo "$GH_REPO" --draft=false --latest
url=$(gh release view "$RELEASE_TAG" --repo "$GH_REPO" --json url --jq '.url')
printf 'Published [%s](%s) with the Pet ZIP and SHA256SUMS.txt.\n' "$RELEASE_TAG" "$url" >> "$GITHUB_STEP_SUMMARY"
