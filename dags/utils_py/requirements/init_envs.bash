#!/bin/bash

# init conda
echo "init conda..."
conda init bash

# create env
echo "createt env..."
conda create --name broker_info_solo python=3.11

# activate env
echo "activate env broker_info_solo..."
conda activate broker_info_solo bash

# install requirements.txt
echo "install requirements.txt..."
pip install -r ./utils_py/requirements/requirements.txt

echo "Все команды выполнены."
