import os
import json
import pandas as pd

# Define the models and system messages
models = ["gpt-4o", "gpt-4o-mini-2024-07-18", "claude-3-5-sonnet-20240620", "claude-3-7-sonnet-20250219"]
system_messages = ["default_defended", "default", "blockchain"]
task_suits = ["chain", "crypto_trading"]

# Initialize counters for results
results = {model: {msg: {suit: {"harder": {"utility_no_injection": 0, "utility_pi": 0, "attack_success_pi": 0, "utility_mi": 0, "attack_success_mi": 0, "total_pi": 0, "total_mi": 0}, "easier": {"utility_no_injection": 0, "utility_mi": 0, "attack_success_mi": 0, "total_mi": 0}} for suit in task_suits} for msg in system_messages} for model in models}

# Define task ranges
harder_tasks = {"chain": range(25), "crypto_trading": range(80)}
easier_tasks = {"chain": range(25, 32), "crypto_trading": range(80, 96)}

# Iterate through models, system messages, and task suits
for model in models:
    for msg in system_messages:
        for suit in task_suits:
            model_dir = f'/home/shared/agents/agentdojo/runs/{model}'
            
            # Process harder tasks
            for task_num in harder_tasks[suit]:
                base_dir = os.path.join(model_dir, msg, suit)
                task_dir = os.path.join(base_dir, f'user_task_{task_num}/none')
                if os.path.exists(task_dir):
                    for file_name in os.listdir(task_dir):
                        if file_name.endswith('.json'):
                            file_path = os.path.join(task_dir, file_name)
                            if os.path.exists(file_path):
                                with open(file_path, 'r') as file:
                                    try:
                                        data = json.load(file)
                                        if data.get('utility') is True:
                                            results[model][msg][suit]["harder"]["utility_no_injection"] += 1
                                    except json.JSONDecodeError:
                                        print(f"Error decoding JSON in file: {file_path}")

                # Adjust base_dir for memory injection tasks when model is 'gpt-4o' and system_message is 'default_defended'
                if model == "gpt-4o" and msg == "default_defended":
                    base_dir = os.path.join(model_dir + '-spotlighting_with_delimiting', 'default_defended_es', suit)
                else:
                    base_dir = os.path.join(model_dir + '-spotlighting_with_delimiting', msg, suit)
                
                task_dir = os.path.join(base_dir, f'user_task_{task_num}/important_instructions')
                if os.path.exists(task_dir):
                    for file_name in os.listdir(task_dir):
                        if file_name.endswith('memory_injection.json'):
                            results[model][msg][suit]["harder"]["total_mi"] += 1
                            file_path = os.path.join(task_dir, file_name)
                            if os.path.exists(file_path):
                                with open(file_path, 'r') as file:
                                    try:
                                        data = json.load(file)
                                        if data.get('utility') is True:
                                            results[model][msg][suit]["harder"]["utility_mi"] += 1
                                        if data.get('security') is True:
                                            results[model][msg][suit]["harder"]["attack_success_mi"] += 1
                                    except json.JSONDecodeError:
                                        print(f"Error decoding JSON in file: {file_path}")

                        elif file_name.endswith('.json'):
                            results[model][msg][suit]["harder"]["total_pi"] += 1
                            file_path = os.path.join(task_dir, file_name)
                            if os.path.exists(file_path):
                                with open(file_path, 'r') as file:
                                    try:
                                        data = json.load(file)
                                        if data.get('utility') is True:
                                            results[model][msg][suit]["harder"]["utility_pi"] += 1
                                        if data.get('security') is True:
                                            results[model][msg][suit]["harder"]["attack_success_pi"] += 1
                                    except json.JSONDecodeError:
                                        print(f"Error decoding JSON in file: {file_path}")

            # Process easier tasks
            for task_num in easier_tasks[suit]:
                base_dir = os.path.join(model_dir, msg, suit)
                task_dir = os.path.join(base_dir, f'user_task_{task_num}/none')
                if os.path.exists(task_dir):
                    for file_name in os.listdir(task_dir):
                        if file_name.endswith('.json'):
                            file_path = os.path.join(task_dir, file_name)
                            if os.path.exists(file_path):
                                with open(file_path, 'r') as file:
                                    try:
                                        data = json.load(file)
                                        if data.get('utility') is True:
                                            results[model][msg][suit]["easier"]["utility_no_injection"] += 1
                                    except json.JSONDecodeError:
                                        print(f"Error decoding JSON in file: {file_path}")

                # Adjust base_dir for memory injection tasks when model is 'gpt-4o' and system_message is 'default_defended'
                if model == "gpt-4o" and msg == "default_defended":
                    base_dir = os.path.join(model_dir + '-spotlighting_with_delimiting', 'default_defended_es', suit)
                else:
                    base_dir = os.path.join(model_dir + '-spotlighting_with_delimiting', msg, suit)
                
                task_dir = os.path.join(base_dir, f'user_task_{task_num}/important_instructions')
                if os.path.exists(task_dir):
                    for file_name in os.listdir(task_dir):
                        if file_name.endswith('memory_injection.json'):
                            results[model][msg][suit]["easier"]["total_mi"] += 1
                            file_path = os.path.join(task_dir, file_name)
                            if os.path.exists(file_path):
                                with open(file_path, 'r') as file:
                                    try:
                                        data = json.load(file)
                                        if data.get('utility') is True:
                                            results[model][msg][suit]["easier"]["utility_mi"] += 1
                                        if data.get('security') is True:
                                            results[model][msg][suit]["easier"]["attack_success_mi"] += 1
                                    except json.JSONDecodeError:
                                        print(f"Error decoding JSON in file: {file_path}")

# Function to convert results to DataFrame
def results_to_dataframe(results, task_type):
    data = []
    for model in results:
        for msg in results[model]:
            for suit in results[model][msg]:
                entry = {
                    "Model": model,
                    "System Message": msg,
                    "Task Suit": suit,
                    "Task Type": task_type,
                    "Utility No Injection": results[model][msg][suit][task_type]["utility_no_injection"],
                    "Utility PI": results[model][msg][suit][task_type].get("utility_pi", 0),
                    # "Attack Success PI": results[model][msg][suit][task_type].get("attack_success_pi", 0),
                    "ASR PI": 0 if results[model][msg][suit][task_type].get("total_pi", 0) == 0 else results[model][msg][suit][task_type].get("attack_success_pi", 0) / results[model][msg][suit][task_type].get("total_pi", 0),   
                    "Total PI": results[model][msg][suit][task_type].get("total_pi", 0),
                    "Utility MI": results[model][msg][suit][task_type]["utility_mi"],
                    # "Attack Success MI": results[model][msg][suit][task_type]["attack_success_mi"],
                    "ASR MI": 0 if results[model][msg][suit][task_type].get("total_mi", 0) == 0 else results[model][msg][suit][task_type].get("attack_success_mi", 0) / results[model][msg][suit][task_type].get("total_mi", 0),
                    "Total MI": results[model][msg][suit][task_type]["total_mi"],
                }
                data.append(entry)
    return pd.DataFrame(data)

# Convert results to DataFrames
harder_df = results_to_dataframe(results, "harder")
easier_df = results_to_dataframe(results, "easier")

# Print the DataFrames
print("Harder Tasks Results:")
print(harder_df.to_string(index=False))

print("\nEasier Tasks Results:")
print(easier_df.to_string(index=False))  

# Save the DataFrames to CSV files
harder_df.to_csv('harder_tasks_results.csv', index=False)
easier_df.to_csv('easier_tasks_results.csv', index=False)