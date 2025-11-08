#!/bin/bash

command python3 --version > /dev/null 2>&1

if [[ $? != 0 ]]; then
        echo "installing python"
        sudo apt install python3 -y
fi


if [[ -d ".venv" ]]; then
        echo "Not needed to create virtual env"
else
         sudo apt install python3-venv -y
         python3 -m venv .venv
fi
command -v nginx > /dev/null 2>&1

if [[ $? == 1 ]]; then
        sudo apt install nginx -y
else
        sudo systemctl start nginx
fi

echo "activating virtual environment"
sudo chmod 770 .venv/bin/activate
source .venv/bin/activate

echo "finished activating virtual environment"

while IFS= read -r library;do
        if [[ ! -d ".venv/lib/python3.12/site-packages/$library"  ]]; then
                pip install "$library"
        fi
done < req_pip.txt

echo "all installed"

echo "Running app"
sudo systemctl start project

deactivate

echo "started nginx"
sudo systemctl start nginx
