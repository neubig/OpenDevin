"""A module to assist getting a string responses from the agent on CLI.

Example command line:
$ python eval/catch_responses.py --agent MonologueAgent --task "Find question 1 from the second assignment in CMU Undergraduate Advanced Data Analysis's Spring 2019 semester." --opendevin-dir $HOME/Documents/GitHub/OpenDevin-microagent
"""

import os
import json
import random
import argparse
from typing import Any


def get_agent_responses(
    agent: str, task: str, opendevin_dir: str, llm_model: str
) -> list[dict[str, Any]]:
    # save the current working directory
    cwd = os.getcwd()
    #try:
    # cd to the opendevin directory
    os.chdir(opendevin_dir)
    # get a random string to use as the workspace and log file
    rand_str = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
    workspace_dir = f"./workspace_{rand_str}"
    # run the command (this is an ugly way of doing things, forgive me for my sins)
    try:
        task = task.replace('"', '\\"')
        command_str = (
            f"LLM_MODEL={llm_model} poetry run python ./opendevin/core/main.py "
            f'-i 10 -t "{task}" -c "{agent}" -d "./{workspace_dir}"'
        )
        # run the agent
        os.system(command_str)
        # find the most recent sub directory in the `logs/llm` directory
        log_dir = "./logs/llm"
        sub_dirs = [
            d for d in os.listdir(log_dir) if os.path.isdir(os.path.join(log_dir, d))
        ]
        sub_dirs.sort()
        most_recent_dir = sub_dirs[-1]
        # concatenate all dictionaries in the logs directory to a JSON list
        log_files = os.listdir(f"{log_dir}/{most_recent_dir}")
        log_files = [x for x in log_files if x.startswith("response")]
        log_files.sort()
        responses_list = []
        for log_file in log_files:
            with open(f"{log_dir}/{most_recent_dir}/{log_file}", "r") as f:
                file_str = f.read()
                file_str = file_str[file_str.find("{") : file_str.rfind("}") + 1]
                responses_list.append(json.loads(file_str))
        return responses_list
    finally:
        # remove the workspace dir
        os.system(f"rm -rf {workspace_dir}")
        # cd back to the original working directory
        os.chdir(cwd)


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Get agent responses")
    parser.add_argument("--agent", type=str, help="Agent name",default="MicroManagerAgent")
    parser.add_argument("--task", type=str, help="Task description")
    parser.add_argument("--opendevin-dir", type=str, help="Opendevin directory",default="/Users/jp/Documents/GitHub/OpenDevin-microagent")
    parser.add_argument(
        "--llm-model", type=str, default="gpt-4-turbo", help="LLM model name"
    )#gpt-4-turbo together_ai/META-LLAMA/LLAMA-3-70B-CHAT-HF
    args = parser.parse_args()
    # Call get_agent_responses function
    responses = get_agent_responses(
        args.agent, args.task, args.opendevin_dir, args.llm_model
    )
    print(json.dumps(responses, indent=2))
    with open("responses.json", "w") as f:
        json.dump(responses, f, indent=2)


if __name__ == "__main__":
    main()