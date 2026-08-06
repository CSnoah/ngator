# Application Brief

ngator = Aliasing of file paths.

# Purpose 

A terminal utility designed to simplify the traversal of long file paths. The application targets efficiency of developer workflow. The primary use case is navigation to a target directory directly to remove the burden of ample file path hops. The utility fzf is a standard for file path navigation however its use diminishes as the number of files served to it increases. This constricts is usability to project directory navigation. This is the gap that ngator aims to fill. Ngator at its core allows users to alias file paths. Serving as a bookmark for important files, it can be used in conjunction with fzf to navigate your entire file system.

# Inspiration

I use WSL for development and dislike saving projects in the WSL file system. This requires navigation to long file paths (ex. /mnt/c/Users/noahm/documents), which quickly becomes a ridiculously repetitive task. I wanted something simple, fast, and include basic auto complete. For a while I just did aliases in my .bashrc which if you can imagine scales wonderfully. Once I got the time, I scaled it to a project that could handle volume with a database. I'm sure projects that solve this same problem exist, but honestly, I would rather not deal with their bloated features and overcomplicated command system. This project aims to be exactly what it is, a file path aliasing utility, and nothing more. I wanted it to be fast, simple, and have basic alias auto complete. It may not seem like particularly impressive project, but it's the most useful piece of software I have built. I use it every day. I am always open to new ways to remove friction in my developer workflow. If you are aware of something that solves this problem better, let me know. I'd love to check it out!

# key principals
- simplicity
- single purpose
- speed
- auto complete

# Dependencies
- python3
- sqlite

# install
1. Clone repo
2. Put somewhere good for utilities (and won't be moving)
3. In the project directory run init.sh script: python3 init.sh
4. Done

# Command Reference

| Command | Aliases | Purpose |
| :------ | :------ | :------ |
| `goto <alias>` | `go`, `g`, or simply `ng <alias>` | Change the current directory to the specified alias. |
| `add <path> <alias>` | `a` | Add a new path alias. |
| `add -c <alias>` | `a -c`, `add --current <alias>` | Add the current working directory as an alias. |
| `delete <alias>` | `del` | Remove an existing alias. |
| `list` | `ls` | List all stored aliases. |
| `list -l` | `ls -l` | Display a detailed listing of stored aliases. |
| `set --tag <alias> <tag>` | — | Assign a tag to an alias. |
| `set --alias <old> <new>` | — | Rename an existing alias. |
| `set --scope <tag>` | — | Set the active tag scope. |
| `dlog -t` | `dlog --true` | Enable debug logging. |
| `dlog -f` | `dlog --false` | Disable debug logging. |

# Demo

- Checkout what it does before you try it!

<hr />

**ng ls**

<img width="725" height="201" alt="image" src="https://github.com/user-attachments/assets/3ecbcc7e-8c39-4f67-b5d8-ec96c572e652" />

<hr />

**ng add -c <alias>**

<img width="701" height="56" alt="image" src="https://github.com/user-attachments/assets/42884d87-9f51-432b-a69a-a3d94845466f" />

<hr />

**ng del <alias>**

<img width="660" height="50" alt="image" src="https://github.com/user-attachments/assets/1cdc47b4-5036-401a-b163-fcf17308e541" />

<hr />

**ng <alias>**

<img width="587" height="50" alt="image" src="https://github.com/user-attachments/assets/923e649a-ba4a-4622-90e0-5e8b4f3910b8" />

<hr />

# Development

I want the utility to be simple but there are still some features I would like to explore adding. If they make the utility feel too bloated, then I probably won't add them to main.

- fzf cli integration
- alias groups (scope)
  
# Architecture
### 1. shell_execution.sh
This is the very top of the stack and is what the parent process directly executes via binding in .bashrc when shell starts up.
This is the first file that terminal input commands funnel through and is the last file reached before viewing command output on the terminal.

Allows Application to accesses parent process via launching shell_execution in .bashrc

### 2. cmd_dispatch.py
This is the second file to receive user input. This is the core facilitator of the application. It receives user input as a Flag and directs the processed response as a broadcast Signal back to shell_execution.sh through stdout. It also uses exit code channels to convey internal application errors.

**output channels**

1. stdout -> cmd output
2. exit codes -> error logs

**Defines Input and Output Context**

Defines the input and output context used by the component.

| Context | Fields |
|---------|--------|
| `in_ctx` | `cmd_flag`<br>`cmd_args` |
| `out_ctx` | `broadcast` |
  
**Defines Actions mapping in_ctx to qy and env_req**

Maps input command flags to their corresponding handler functions.

| Command Flag | Action Function |
|--------------|-----------------|
| `in_ctx.Flags.ADD` | `qy.add_path` |
| `...` | `...` |


**Command Flow**

The dispatch function receives an in_ctx flag as an argument, determines a function to execute, and returns that functions output. The returned resutlt is then sent to shell_execution.sh via stdout.

| Flow | Description |
|------|-------------|
| `input(flag) → dispatch → cmd_parser → dispatch → (qy or env_req)` | Parses the input flag and routes execution to either the query handler (`qy`) or environment request handler (`env_req`). |
| `qy → db_requests.py → dispatch → shell_execution.sh → terminal output` | Executes query-related requests through database requests, dispatching to shell execution and returning terminal output. |
| `env_req → configures environment variables → no output` | Handles environment configuration changes without producing terminal output. |

### 3. resources/dispatch_context.py

- defines the classes - flags and signals

### 4. src/db_requests.py 

- handles db queries

## 5. src/cmd_parser 

- parses CLI with argparse

