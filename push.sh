#!/bin/bash
#
# Pull, commit everything, and push this repo.
# This project uses main, not master.
#
#   ./push.sh
#   ./push.sh "commit message"

set -euo pipefail

cd "$(dirname "$0")"

echo "Checking for newer files online first"
git pull --no-rebase

git add --all .

if git diff --cached --quiet; then
	echo "Nothing to commit."
	git push -u origin main
	exit 0
fi

if [ "$#" -gt 0 ]; then
	input="$*"
else
	echo "####################################"
	echo "Write your commit comment!"
	echo "####################################"
	read -r input
fi

if [ -z "$input" ]; then
	echo "Commit comment is empty. Stopped."
	exit 1
fi

git commit -m "$input"
git push -u origin main

echo "################################################################"
echo "###################    Git Push Done      ######################"
echo "################################################################"
