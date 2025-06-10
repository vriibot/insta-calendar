# Insta Calendar

Static website event calendar that mines from Instagram.

This is a personal project, but feel free to fork/use the code for whatever you like. I'm also happy to accept pull requests to improve parts of the project. However, the code is designed for my own specific use case, so generalization may be difficult.

## Usage

Place instagram usernames in the username.txt file, one per line.

## Configuration

```config.json``` contains options to control the start point of mining. If you delete the file it will autogenerate with defaults. On completion, it will automatically update with last run data.

|option|description|
|-|-|
|start_date| How far back to mine, if there exists no `last_run` data. Accepts an ISO format string, `null`, or `"default"`. If the value is null, it will mine until the beginning of an account. By default, the start point will be set to one month prior to the first run. |
| last_run | Stores the last run. You can overwrite this or set to null.

The API mines backwards from the most recent post, so setting an earlier start date while maintaining the last run does nothing.

# GitHub Action Automation

Go to Settings > Actions > General, scroll to Workflow permissions and set to "Read and write permissions" and "Allow GitHub Actions to create and approve pull requests"