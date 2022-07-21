#!/bin/bash
BRANCH=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match)
echo "CHANGELOG"
echo ----------------------
git tag -l | sort -u -r | while read TAG ; do
    echo
    if [ $NEXT ];then
        echo [$NEXT]
    else
        echo "[Current]"
    fi
    GIT_PAGER=cat git log --no-merges --format=" * [%cd] (%an) - %s" $TAG..$NEXT | grep -v ".*ange.*og"
    NEXT=$TAG
done
FIRST=$(git tag -l | head -1)
echo
echo [$FIRST]
#echo [${BRANCH}]
GIT_PAGER=cat git log --no-merges --format=" * [%cd] (%an) - %s" ${FIRST} | grep -v ".*ange.*og"
