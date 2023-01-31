#!/bin/bash

#RUN THIS SCRIPT FROM THE "/" DIRECTORY OF A DEVICE

On_Red='\033[41m'
On_Green='\033[42m'
Color_Off='\033[0m'
BWhite='\033[1;37m'

printf ${BWhite}

if ! [[ -f etc/passwd ]]
then
  printf "Couldn't find etc/passwd\n"
  printf "${On_Red}FAILED${Color_Off}\n"
  exit 1
fi

cat etc/passwd 2>/dev/null | grep -i "sh$" | cut -d ":" -f 1 >> tmp.txt

user1=$(echo -n -e '\x72\x6f\x6f\x74\x0a')
user2=$(echo -n -e '\x76\x69\x65\x77\x65\x72\x75\x73\x65\x72\x0a')
fail=0

while IFS= read -r line
do
  if ! ( [ $line == $user1 ] || [ $line == $user2 ] )
  then
    fail=1
    printf "$line\n"
  fi
done < tmp.txt

if (( $fail ))
then
  printf "${On_Red}FAILED${Color_Off}\n"
else
  printf "${On_Green}PASS${Color_Off}\n"
fi

rm tmp.txt

