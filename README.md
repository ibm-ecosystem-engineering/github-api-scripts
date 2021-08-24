# GitHub API Scripts

Set of Python scripts to help streamline your interactions with GitHub APIs.

## Organization

Usage:
```sh
usage: org.py [-h] -t TOKEN -o ORG [--team TEAM] [-r ROLE] [-f FILE] action
```

You will need a GitHub personnal access token with organization admin privileges to perform these actions. To create one:
- Navigate to https://github.com/settings/tokens/new
- Select `admin:org`
- Click `Generate token`

### Example

To invite a list of users in organization `{ORG_NAME}` :

```sh
python org.py add_team_members -t {GITHUB_TOKEN} -f {CSV_FILE_NAME} -o {ORG_NAME}
```

**NOTE**: The CSV file must contain `Email` and `Sr. No` columns, like:
```csv
Sr. No,Email,...
001,mail@example.com,...
002,mail@example.com,...
```

To invite all members of organization `{ORG_NAME}` in team `{TEAM_NAME}` :

```sh
python org.py add_team_members -t {GITHUB_TOKEN} -o {ORG_NAME} --team {TEAM_NAME}
```
