#!/bin/bash

On_Red='\033[41m'
On_Green='\033[42m'
Color_Off='\033[0m'
BWhite='\033[1;37m'

printf ${BWhite}

if [ $# -eq 0 ];
then
  echo "please provide an IP address"
  echo "EXAMPLE: ./SSHTelnetDetect.sh 192.168.1.1"
  exit 1
elif [ $2 ];
then
  echo "Too many arguments: $@"
  echo "EXAMPLE: ./SSHTelnetDetect.sh 192.168.1.1"
  exit 1
elif ! [[ $1 =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]];
then
  echo "incorrect IP address format"
  echo "EXAMPLE: ./SSHTelnetDetect.sh 192.168.1.1"
  exit 1
fi

if (which nmap | grep -q 'nmap')
then
  echo "SCANNING FOR SSH AND TELNET ON $1"
else
  echo "please install nmap on this machine and try again"
fi



nmap -p- -sV $1 >> tmp.txt
if grep -iq 'ssh\|telnet' tmp.txt; then
  printf "${On_Red}FAILED${Color_Off}\n"
  printf ${BWhite}
  while IFS= read -r line; do echo $line | grep -i 'ssh\|telnet'; done < tmp.txt
else
  printf "${On_Green}PASS${Color_Off}\n"
fi
rm tmp.txt
