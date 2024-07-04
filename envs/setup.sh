#!/bin/bash

eval "$(conda shell.bash hook)"

ENV_NAME="apollo"

if conda env list | grep -q "$ENV_NAME"; then
  echo "Conda environment '$ENV_NAME' already exists."
else
  echo "Creating conda environment '$ENV_NAME' from environment.yml..."
  conda env create -f envs/conda/environment.yml
  
  echo "Installing additional packages from requirements.txt..."
  conda run -n $ENV_NAME pip install -r envs/pip/requirements.txt
fi
