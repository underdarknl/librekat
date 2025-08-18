#!/bin/bash

#GITHUB_TOKEN should be ${{ secrets.GITHUB_TOKEN }}
#DESTINATION_BRANCH should be ${{ github.ref }}

FILES=$(git diff --name-only)
for FILE in $FILES; do
    SHA=$(git rev-parse "$DESTINATION_BRANCH":"$FILE")
    CONTENT=$(base64 -i "$FILE" | tr -d '\n')
    gh api --method PUT /repos/:owner/:repo/contents/"$FILE" \
        --field message="Update $FILE" \
        --field content="$CONTENT" \
        --field branch="$DESTINATION_BRANCH" \
        --field sha="$SHA"
done
