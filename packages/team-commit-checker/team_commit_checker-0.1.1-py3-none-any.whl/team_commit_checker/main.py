from PyInquirer import prompt
from team_commit_checker.coding_net import CodingNet
import configparser
import os


def read_config(config_path="~/.team_commit_checker/config.ini"):
    """Read and return the token and team_id from the configuration file."""
    config_path = os.path.expanduser(config_path)
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            "The configuration file 'config.ini' was not found. Ensure it's in the correct path."
        )

    config = configparser.ConfigParser()
    config.read(config_path)

    if "CODING" not in config:
        raise KeyError("The 'CODING' section is missing in the configuration file.")

    if "TOKEN" not in config["CODING"] or "TEAM_ID" not in config["CODING"]:
        raise KeyError("Essential keys are missing in the configuration file.")

    return config["CODING"]["TOKEN"], config["CODING"]["TEAM_ID"]


def display_main_menu():
    questions = [
        {
            "type": "list",
            "name": "main_menu",
            "message": "What do you want to do?",
            "choices": ["List Repos", "Check Commits", "Exit"],
        },
    ]
    answers = prompt(questions)
    return answers["main_menu"]


def display_date_menu():
    questions = [
        {
            "type": "input",
            "name": "date",
            "message": "What date do you like to check",
        },
    ]
    answers = prompt(questions)
    return answers["date"]


def main():
    token, team_id = read_config()
    coding_net = CodingNet(token, team_id)

    while True:
        # Display main menu to the user
        choice = display_main_menu()
        if choice == "List Repos":
            repos = coding_net.get_repo_list()
            for repo in repos:
                print(f"Repo name: {repo['Name']}")
                print(f"Repo url: {repo['WebUrl']}\n")

        elif choice == "Check Commits":
            date = display_date_menu()
            coding_net.perform_commit_check(date)

        elif choice == "Exit":
            break


if __name__ == "__main__":
    main()
