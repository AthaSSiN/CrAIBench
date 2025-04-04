#!/bin/bash

# Define injection task mapping per user task
declare -A injection_map
# TRANSFER
injection_map[0]="injection_task_0 injection_task_1"
injection_map[1]="injection_task_0 injection_task_1"
injection_map[2]="injection_task_0 injection_task_1"
injection_map[3]="injection_task_0 injection_task_1"
injection_map[25]="injection_task_0 injection_task_1"

# BRIDGE
injection_map[4]="injection_task_2 injection_task_3"
injection_map[5]="injection_task_2 injection_task_3"
injection_map[6]="injection_task_2 injection_task_3"
injection_map[26]="injection_task_2 injection_task_3"

# STAKE - deposit
injection_map[7]="injection_task_4 injection_task_5"
injection_map[8]="injection_task_4 injection_task_5"
injection_map[9]="injection_task_4 injection_task_5"
injection_map[10]="injection_task_4 injection_task_5"
injection_map[27]="injection_task_4 injection_task_5"

# STAKE - withdraw
injection_map[11]="injection_task_6 injection_task_7"
injection_map[12]="injection_task_6 injection_task_7"
injection_map[13]="injection_task_6 injection_task_7"
injection_map[14]="injection_task_6 injection_task_7"
injection_map[28]="injection_task_6 injection_task_7"

# STAKE - claim
injection_map[15]="injection_task_8 injection_task_9"
injection_map[16]="injection_task_8 injection_task_9"
injection_map[17]="injection_task_8 injection_task_9"
injection_map[18]="injection_task_8 injection_task_9"
injection_map[29]="injection_task_8 injection_task_9"

# DEPLOY TOKEN
injection_map[19]="injection_task_10 injection_task_11"
injection_map[20]="injection_task_10 injection_task_11"
injection_map[30]="injection_task_10 injection_task_11"

# AIRDROP
injection_map[21]="injection_task_12 injection_task_13"
injection_map[22]="injection_task_12 injection_task_13"
injection_map[23]="injection_task_12 injection_task_13"
injection_map[24]="injection_task_12 injection_task_13"
injection_map[31]="injection_task_12 injection_task_13"

# Default values
MODEL="gpt-4o"
DEFENSE="spotlighting_with_delimiting"
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

# If no user task provided
if [ ${#USER_TASKS[@]} -eq 0 ]; then
  if $MI_FLAG; then
    # Run all user tasks 0–31
    USER_TASKS=()
    for i in $(seq 19 31); do
      USER_TASKS+=("user_task_$i")
    done
  else
    # Run only user tasks 0–24 (skip single-step tasks 25–31)
    USER_TASKS=()
    for i in $(seq 4 24); do
      USER_TASKS+=("user_task_$i")
    done
  fi
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
    IFS=' ' read -r -a ITS <<< "${injection_map[$USER_TASK_NUM]}"
    for IT in "${ITS[@]}"; do
      CMD="$SCRIPT -s chain -ut $UT -it $IT --model $MODEL --defense $DEFENSE --system-message-name $SYSTEM_MSG --attack $ATTACK ${OTHER_ARGS[*]}"
      echo "Running: $CMD"
      eval $CMD
    done
  fi
done
