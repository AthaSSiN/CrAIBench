# Atharv updates

- Since the cryppto_trading task can run with all combinations of injection tasks, just run it with this command to run the entire benchmark.

```bash
$ python -m agentdojo.scripts.benchmark -s crypto_trading --model gpt-4o --defense spotlighting_with_delimiting --system-message-name default_defended --attack important_instructions -mi
```
Remove -mi to run with prompt injection instead of memory injection.
To pass a subset of user or injection tasks, use the following command:

```bash
$ python -m agentdojo.scripts.benchmark -s crypto_trading --model gpt-4o --defense spotlighting_with_delimiting --system-message-name default_defended --attack important_instructions -ut user_task_0 -ut user_task_1 -it injection_task_0 -it injection_task_1 -mi
```
etc.

For the chain benchmark, better to run the benchmark with the run_script.sh script, since it can run all combinations of user and injection tasks with correct combinations

Change the model, defense, system message, and attack in the run_script.sh script if required and you can change which tasks to run by editing this section

```bash
# If no user task provided
if [ ${#USER_TASKS[@]} -eq 0 ]; then
  if $MI_FLAG; then
    # Run all user tasks 0–31
    USER_TASKS=()
    for i in $(seq 0 31); do    
        USER_TASKS+=("user_task_$i")
    done
  else
    # Run only user tasks 0–24 (skip single-step tasks 25–31)
    USER_TASKS=()
    for i in $(seq 0 24); do
      USER_TASKS+=("user_task_$i")
    done
  fi
fi
```

The results of the benchmark are saved in the runs/ directory.

<center>

# AgentDojo: Benchmarking the Capabilities and Adversarial Robustness of LLM Agents

[Edoardo Debenedetti](https://edoardo.science)<sup>1</sup>, [Jie Zhang](https://zj-jayzhang.github.io)<sup>1</sup>, [Mislav Balunović](https://www.sri.inf.ethz.ch/people/mislav)<sup>1,2</sup>, [Luca Beurer-Kellner](https://www.sri.inf.ethz.ch/people/luca)<sup>1,2</sup>, [Marc Fischer](https://marcfischer.at)<sup>1,2</sup>, [Florian Tramèr](https://floriantramer.com)<sup>1</sup>

<sup>1</sup>ETH Zurich and <sup>2</sup>Invariant Labs

Read our paper [here](https://arxiv.org/abs/2406.13352).
</center>

## Quickstart

```bash
pip install agentdojo
```

> [!IMPORTANT]
> Note that the API of the package is still under development and might change in the future.

If you want to use the prompt injection detector, you need to install the `transformers` extra:

```bash
pip install "agentdojo[transformers]"
```

## Running the benchmark

The benchmark can be run with the [benchmark](src/agentdojo/scripts/benchmark.py) script. Documentation on how to use the script can be obtained with the `--help` flag.

For example, to run the `workspace` suite on the tasks 0 and 1, with `gpt-4o-2024-05-13` as the LLM, the tool filter as a defense, and the attack with tool knowlege, run the following command:

```bash
python -m agentdojo.scripts.benchmark -s workspace -ut user_task_0 \
    -ut user_task_1 --model gpt-4o-2024-05-13 \
    --defense tool_filter --attack tool_knowledge
```

To run the above, but on all suites and tasks, run the following:

```bash
python -m agentdojo.scripts.benchmark --model gpt-4o-2024-05-13 \
    --defense tool_filter --attack tool_knowledge
```

## Documentation of the Dojo

Take a look at our [documentation](https://agentdojo.spylab.ai/).

## Development set-up

Take a look at the [development set-up](https://agentdojo.spylab.ai/docs/development) docs.

## Citing

If you use AgentDojo in your research, please consider citing our paper:

```bibtex
@misc{debenedetti2024agentdojo,
      title={AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents},
      author={Edoardo Debenedetti and Jie Zhang and Mislav Balunović and Luca Beurer-Kellner and Marc Fischer and Florian Tramèr},
      year={2024},
      eprint={2406.13352},
      archivePrefix={arXiv},
      primaryClass={cs.CR}
}
```
