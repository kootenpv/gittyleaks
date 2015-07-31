#!/bin/bash

# Run like: gittyleaks username reponame
# e.g. gittyleaks kootenpv yagmail
# working example: gittyleaks smartczy weather_py

USERNAME=$1
REPO=$2
git clone https://github.com/$USERNAME/$REPO.git
cd $REPO
echo "----------------------------------------------------------------------------------------------"
echo "Bot Detective at work ..."
echo "----------------------------------------------------------------------------------------------"
rm -f $REPO_$USERNAME_output.txt

# trying to find simple var assignment regex
git rev-list --all | xargs git grep -i "[ ._-]api[ ]*=[ ]*['\"]" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]key[ ]*=[ ]*['\"]" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]user[ ]*=[ ]*['\"]" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]username[ ]*=[ ]*['\"]" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]pw[ ]*=[ ]*['\"]" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]pass[ ]*=[ ]*['\"]" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]password[ ]*=[ ]*['\"]" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]email[ ]*=[ ]*['\"][^@]+@" >> $REPO_$USERNAME_output.txt
git rev-list --all | xargs git grep -i "[ ._-]mail[ ]*=[ ]*['\"][^@]+@" >> $REPO_$USERNAME_output.txt

# trying to find json style var assignments
# <to be made>
git rev-list --all | xargs git grep -i "[ ._-]['\"]key['\"][ ]*:[ ]*['\"][^@]+@" >> $REPO_$USERNAME_output.txt

# trying to find non-string style var assignments
# <to be made>
git rev-list --all | xargs git grep -i "key[ ]*=[a-zA-Z]*" >> $REPO_$USERNAME_output.txt


# Display
cat $REPO_$USERNAME_output.txt | grep -i --color=always "(api\|key\|user\|pw\|pass\|mail)" 
