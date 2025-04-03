#!/bin/bash

# Define injection task mapping per user task
declare -A injection_map
injection_map[0]="injection_task_10"
injection_map[1]="injection_task_10"
injection_map[2]="injection_task_2"
injection_map[3]="injection_task_3"
injection_map[4]="injection_task_4 injection_task_6"
injection_map[5]="injection_task_5 injection_task_7"
injection_map[6]="injection_task_8"
injection_map[7]="injection_task_9"

# Default values
MODEL="gpt-4o"
DEFENSE="spotlighting_with_datamarking"
SYSTEM_MSG="default_defended"
ATTACK="important_instructions"
SCRIPT="python -m agentdojo.scripts.benchmark"

# Parse flags
MI_FLAG=false
USER_TASKS=()
OTHER_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -ut|--user-task)
      USER_TASKS+=("$2")
      shift 2
      ;;
    -mi)
      MI_FLAG=true
      shift
      ;;
    *)
      OTHER_ARGS+=("$1")
      shift
      ;;
  esac
done

# If no user task provided, run all user tasks 0–7
if [ ${#USER_TASKS[@]} -eq 0 ]; then
  USER_TASKS=("user_task_0" "user_task_1" "user_task_2" "user_task_3" "user_task_4" "user_task_5" "user_task_6" "user_task_7")
  RUN_ALL=true
else
  RUN_ALL=false
fi

# Loop through user tasks
for UT in "${USER_TASKS[@]}"; do
  USER_TASK_NUM="${UT##*_}"

  if $MI_FLAG; then
    IFS=' ' read -r -a ITS <<< "${injection_map[$USER_TASK_NUM]}"
    for IT in "${ITS[@]}"; do
      CMD="$SCRIPT -s chain -ut $UT -it $IT --model $MODEL --defense $DEFENSE --system-message-name $SYSTEM_MSG --attack $ATTACK -mi ${OTHER_ARGS[*]}"
      echo "Running: $CMD"
      eval $CMD
    done
  else
    if [[ "$USER_TASK_NUM" == "0" || "$USER_TASK_NUM" == "1" ]]; then
      CMD="$SCRIPT -s chain -ut $UT --model $MODEL --defense $DEFENSE --system-message-name $SYSTEM_MSG --attack $ATTACK ${OTHER_ARGS[*]}"
      echo "Running: $CMD"
      eval $CMD
    else
      echo "Skipping $UT: -mi flag not provided and this task requires specific injection mapping"
    fi
  fi
done
