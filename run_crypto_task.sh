#!/bin/bash

models=("gpt-4o" "gpt-4o-mini-2024-07-18" "claude-3-5-sonnet-20240620" "claude-3-7-sonnet-20250219")
system_messages=("default_defended" "default" "blockchain")

for model in "${models[@]}"; do
    for system_message in "${system_messages[@]}"; do

        for i in {0..95}; do
            # skip for default with gpt-4o
            if [[ "$model" == "gpt-4o" && "$system_message" == "default" ]]; then
                break
            fi

            echo "Running basic prompt for model: $model and system message: $system_message"
            python -m agentdojo.scripts.benchmark -s crypto_trading --model $model -ut user_task_$i --system-message-name $system_message
        done

        # skip default_defended and blockchain for claude models and gpt-4o
        if [[ "$model" == "claude-3-5-sonnet-20240620" || "$model" == "claude-3-7-sonnet-20250219" || "$model" == "gpt-4o" ]]; then
            if [[ "$system_message" == "default_defended" || "$system_message" == "blockchain" ]]; then
                continue
            fi
        fi

        for i in {0..95}; do
            echo "Running attack for model: $model and system message: $system_message"
            python -m agentdojo.scripts.benchmark -s crypto_trading --model $model -ut user_task_$i --defense spotlighting_with_delimiting --system-message-name $system_message --attack important_instructions -mi
            python -m agentdojo.scripts.benchmark -s crypto_trading --model $model -ut user_task_$i --defense spotlighting_with_delimiting --system-message-name $system_message --attack important_instructions
            
        done
    done
done