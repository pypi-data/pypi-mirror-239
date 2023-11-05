# Team Commit Checker

This is a command-line application that check team members' git commits in coding.net.

## Installation

To install `team_commit_checker`, run this command in your terminal:

```bash
pip install team_commit_checker
```

This is the preferred method to install team_commit_checker, as it will always install the most recent stable release.

If you have Poetry installed and prefer to use it for installation, run:

```bash
poetry add team_commit_checker
```

## Usage
Once installed, you can run the application with the following command:

```bash
team-commit-checker
```

The program will prompt you to enter the book title and then retrieve the book information to generate promotional content.

## Configuration
Before the first run, make sure to create a config.ini file in `~/.team_commit_checker/config.ini` with the following structure:

```ini
[CODING]
TOKEN = your_access_token_in_coding_net
TEAM_ID = your_team_id_in_coding_net
```

Replace your_access_token_in_coding_net and your_team_id_in_coding_net with your actual values.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
