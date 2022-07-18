#!/bin/bash

DEST="git@github.com:gotunixcode/workflow.git"

echo "Pushing repo to ${DEST}"
git push --mirror ${DEST}
if [ $? -eq 0 ]; then
    echo "Completed successfully"
    exit 0
else
    echo "Failure to push to ${DEST}"
    exit 1
fi
