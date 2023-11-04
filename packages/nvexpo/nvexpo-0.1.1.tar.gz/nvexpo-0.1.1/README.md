# NVEXPO - Non-Volatile EXPOrt

nxexpo it's a simple tool to define environment variables on-the-fly and persisting them between shell sessions.

## Dependencies
- Python 3.8

### Dependencies to build
- [Poetry](https://python-poetry.org/)

### Dependencies to develop
- [PoeThePoet](https://poethepoet.natn.io/)
- [Ruff](https://docs.astral.sh/ruff/)
- [MyPy](https://www.mypy-lang.org/)

## Installation
To install from the source follow the commands:
```Bash
$ poetry build
$ pip install dist/nvexpo*.whl
```

And add the follow line to your `.bashrc` file:
```Bash
eval "$(nvexpo init bash)"
```

## Basic usage
The usage it's too simple. If you want to create a new env var into the current bash session use the command:
```Bash
$ nx weird_variable=101
```

Then, you can close the current terminal or terminate the bash session, and when you start a new one, your env vars will still be there :sparkles:.
```Bash
$ echo $weird_variable
101
```

### Unset variables
To unset variables you need to use flag `--unset`:
```Bash
$ nx var1="hello world"
$ echo $var1
hello world
$ nx --unset var1
$ echo $var1

$ works!!
```

## Why?
The main motivation for creating this tool was that in my work I like to have the Git branch I'm working on in `$branch`, but it's annoying to have to create it every time I restart or close the terminal I was working on.  
I could add it to `.bashrc` directly, but I would have to do it every time I have to work on a new branch and it wasn't comfortable.  
So now instead of having to type:
```Bash
branch="super_useful_change"
```
I have to write:
```Bash
nx branch="super_useful_change"
```
and that's it, no matter how many times I restart, my variable will be there.
