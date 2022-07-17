#!/bin/bash

DEST="git@github.com:gotunixcode/workflow.git"
BRANCH=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match)

if [[ "${BRANCH}" != "main" ]]; then
    echo "Current branch: ${BRANCH}"
    echo "You can only mirror the main branch"
    exit 1
else
    echo "Pushing repo to ${DEST}"
    git push --mirror ${DEST}
    if [ $? -eq 0 ]; then
        echo "Completed successfully"
        exit 0
    else
        echo "Failure to push to ${DEST}"
        exit 1
    fi
fi
