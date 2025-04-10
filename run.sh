#!/bin/bash

# iterate through all the models as a list
models=("claude-3-5-sonnet-20240620" "claude-3-7-sonnet-20250219" "gpt-4o-mini-2024-07-18" "gpt-4o")
system_messages=("default_defended" "default" "blockchain")

for model in "${models[@]}"; do
    for system_message in "${system_messages[@]}"; do
        echo "Running for model: $model and system message: $system_message"
        ./run_script_dao.sh --model $model --system-message-name $system_message -mi
    done
done
