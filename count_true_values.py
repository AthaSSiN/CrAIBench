import os
import json

# Define the base directory
base_dir = '/home/shared/agents/agentdojo/runs/gpt-4o-spotlighting_with_delimiting/chain'

# Initialize counters
utility_true_count_pi = 0
security_true_count_pi = 0
utility_true_count_mi = 0
security_true_count_mi = 0

total_mi_tasks = 0
total_pi_tasks = 0

# Iterate through user_task directories
for task_num in range(80):
    task_dir = os.path.join(base_dir, f'user_task_{task_num}/important_instructions')
    if os.path.exists(task_dir):
        # Iterate through specific JSON files in the directory
        for file_name in os.listdir(task_dir):
            if file_name.endswith('memory_injection.json'):
                total_mi_tasks += 1
                file_path = os.path.join(task_dir, file_name)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                            if data.get('utility') is True:
                                utility_true_count_mi += 1
                            if data.get('security') is True:
                                security_true_count_mi += 1
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file: {file_path}")

            elif file_name.endswith('.json'):
                total_pi_tasks += 1
                file_path = os.path.join(task_dir, file_name)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                            if data.get('utility') is True:
                                utility_true_count_pi += 1
                            if data.get('security') is True:
                                security_true_count_pi += 1
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON in file: {file_path}")

# Print the results
print(f"Total 'utility' true count for prompt injection: {utility_true_count_pi}")
print(f"Total 'security' true count for prompt injection: {security_true_count_pi}") 
print(f"Total 'utility' true count for memory injection: {utility_true_count_mi}")
print(f"Total 'security' true count for memory injection: {security_true_count_mi}") \
    
print("Total tasks: ", total_mi_tasks + total_pi_tasks)  
print("Total MI tasks: ", total_mi_tasks)
print("Total PI tasks: ", total_pi_tasks)