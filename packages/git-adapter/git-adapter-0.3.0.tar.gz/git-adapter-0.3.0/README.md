*Git-Adapter*: A Python interface to the Git command line.

[[_TOC_]]

# Overview

*Git-Adapter* provides Python bindings to the Git command line (and also
to other command-line applications).
It is useful when you know exactly what Git commands you would call from
the shell prompt or in a shell script.

Calling a `git` command returns a `str` generator representing the lines
of output (at least in the default, greedy API, see below).

Note that in `git` commands and command-line flags, hyphens are replaced
by underscores.
Also, Python reserved keywords have to be escaped with a trailing
underscore.
E.g.

```python
    git.cherry_pick(commit)
    for line in git.grep("keyword", ignore_case=True, break_=True):
        print(line)
```

corresponds to

```sh
    git cherry-pick $commit
    git grep --ignore-case --break keyword
```

in the shell.


## Example

```python
    git = Git.clone_repo("git@git.host:test-repo")
    log_lines: Iterator[str] = git.log(first_parent=True, max_count=20, author="me")

    # Process output from a git command:
    for file_ in git.ls_files():
        print("Git file:", file_)
    
    with open("greeting.txt", "w") as fh:
        fh.write("Hello world\n")
    git.commit("greeting.txt", m="Greet the world.", author="me")
    
    origin = git.remote().first_line()
    branch = git.current_branch()  # not an original git command
    git.push(origin, branch)

    # Python reserved keywords have to be escaped with a trailing
    # underscore:
    matches = git.grep("keyword", break_=True, heading=True)

    # Catch errors
    try:
        git.fetch("non-existing-origin").first_line()
    except CmdError as e:
        print("Got error {} when running {}".format(e.returncode, e.cmd_line))
        print("Error message:\n  {}".format("\n  ".join(e.error_lines)))
```


## The `Git` class

The *Git* class has a few specific commands, like `git.hard_reset()` or
`git.current_branch()`; any other method call '`git.<CMD>(…)`' is converted
to a system call '`git CMD …`', e.g.

```python
    from git_adapter.git import Git
    git = Git(".")  # Create a (greedy) Git object
    git.log()       ↦ git log
    files: Iterator[str] = git.ls_files()
                    ↦ git ls-files
    git.commit(m="T'was brillig.", author="me")
                    ↦ git commit -m "T'was brillig." --author=me
    log_lines: Iterator[str] = git.log(first_parent=True, max_count=20, author="me")
                    ↦ git log --first-parent --max-count=20 --author=me
    git.worktree.add(PATH, BRANCH)
                    ↦ git worktree add PATH BRANCH
```

There are actually two versions of the API, which we call greedy and a lazy.

 - A greedy command immediately runs and consumes all its output before
   the call finishes.
   - Constructing a command runs it until the process exits.
   - The Git object returned from the constructor is an iterator over the
     lines of output from the command.
   
 - A lazy command is initiated at construction time and immediately starts
   to relay any output it receives.
   - Constructing a command starts to run it, but stops after the first
     line of output. To run it to the end, one has to call its `run()`
     method.
   - The `lines()` method provides an iterator over the lines of output
     from the command.
     
The examples above were written for the greedy API.
In the lazy API, the last set of examples becomes:

```python
    from git_adapter.git import Git
    git = Git(".").lazy  # Create a LazyGit object
    git.log().run()       ↦ git log
    files: Iterator[str] = git.ls_files().lines()
                          ↦ git ls-files
    git.commit(m="T'was brillig.", author="me").run()
                    ↦ git commit -m "T'was brillig." --author=me
    log_lines: Iterator[str] = git.log(first_parent=True, max_count=20, author="me").lines()
                    ↦ git log --first-parent --max-count=20 --author=me
    git.worktree.add(PATH, BRANCH).run()
                    ↦ git worktree add PATH BRANCH
```

As one can see, translating between the two APIs is straight-forward:

| Greedy                                             | Lazy                                                     |
|:---------------------------------------------------|:---------------------------------------------------------|
| `greedy_git = Git(*args, **kwargs)`                | `lazy_git = Git(*args, **kwargs).lazy`                   |
| `greedy_git.command(*args, **kwargs)`              | `lazy_git.command(*args, **kwargs).run()`                |
| `for line in greedy_git.command(*args, **kwargs):` | `for line in lazy_git.command(*args, **kwargs).lines():` |
| `greedy_git.command(*args, **kwargs).first_line()` | `lazy_git.command(*args, **kwargs).first_line()`         |


So, iterating over the output from a git is written as

```python
    files = list(greedy_git.ls_files())
    files = list(lazy_git.ls_files().lines())
```

For git commands that produce a lot of output, the greedy idiom

```python
    git = Git(sandbox=".")  # greedy API
    for line in git.rev_list(objects=True, all=True).lines():
        # It may take a long time ere we start processing the first line
        if "Makefile" in line:
            print(line, end="")
            break  # has already consumed all lines of output

```

waits until all output has been read, while the lazy idiom

```python
    git = Git(sandbox=".").lazy  # lazy API
    for line in git.rev_list(objects=True, all=True).lines():
        # Starts immediately when the first line of output arrives
        if "Makefile" in line:
            print(line, end="")
            break  # interrupts the command
```
can process the output immediately and abort the git command if needed.


The syntax for retrieving just the first line of output looks the same for
both APIs:

```python
    head = git.rev_parse("HEAD").first_line()
```

The difference being that in the greedy API, the whole output is read
before its first line is returned, while the lazy API does only the work
needed.


Both APIs can be used together:

```python
    git = Git(sandbox=".")

    # We don't expect these commands to produce much output, so run them greedily:
    git.fetch(all=True)
    git.commit(m="T'was brillig.", author="me")

    # This, however, may generate lots of output and we want immediate results:
    for line in git.lazy.rev_list(objects=True, all=True).lines():
        if "Makefile" in line:
            print(line, end="")
            break  # interrupts the command

    # Another short command where it shouldn't matter much which API we use:
    git.merge("@{u}")
```


Note that in the command name and in the `kwargs`, underscores are mapped to
hyphens, so there currently is no way to call
`git strange_command --strange_option`, because git\_adapter would try to
call `git strange-command --strange-option` instead.


## The `Command` class

The `Command` class can be used pretty much like `Git` for other shell
commands:

```python
      Command(["touch"])("file1")                ↦ run 'touch file1'

      ip = Command(["ip"])
      all: Iterator[str] = ip.address.show()     ↦ ip address show
      lo: Iteratore[str] = ip.address.show("dev", "lo")  ↦ ip address show dev lo
      lo = ip.address.show.dev("lo")             ↦ ditto
      lo = ip.address.show.dev.lo()              ↦ ditto

      Command(["git"]).fetch(all=True)           ↦ run 'git fetch --all'
```

or

```python
      Command(["touch"])("file1").lazy.run()     ↦ run 'touch file1'

      ip = Command(["ip"]).lazy
      all = ip.address.show().lines()            ↦ ip address show
      lo = ip.address.show("dev", "lo").lines()  ↦ ip address show dev lo
      lo = ip.address.show.dev("lo").lines()     ↦ ditto
      lo = ip.address.show.dev.lo().lines()      ↦ ditto

      Command(["git"]).lazy.fetch(all=True).run()  ↦ run 'git fetch --all'
```



Again, the result provides a generator of `str` representing the lines of
output from the command.


## Logging

When using *Git-Adapter* from long-running scripts, the user may want to
get output from commands without long delays, but also all output being
logged to a file.
This can be achieved with the `FileLogger` class in *Git-Adapter*:

```python
    from git_adapter.git import Git, FileLogger, run_cmd
    
    # Run a long-running shell command, refreshing output each time a line is
    # printed:
    run_cmd(
        ["sh", "-c", "for i in $(seq 5); do echo $i; sleep 1; done"],
        verbose=True
        )
    
    # The same, but also log to a file:
    run_cmd(
        ["sh", "-c", "for i in $(seq 5); do echo $i; sleep 1; done"],
        logger=FileLogger(log_dir=".", log_file="cmd.log")
        )
    
    # Run a long-running git command, refreshing output each time a line is
    # printed:
    git = Git(".", verbose=True)
    import time, sys
    for ref in git.ls_remote():
        time.sleep(0.01)
        print(".", end="")
        sys.stdout.flush()
    print()
    
    # The same, but also log to a file:
    git = Git(".", FileLogger(log_dir=".", log_file="git.log"))
    import time, sys
    for ref in git.ls_remote():
        time.sleep(0.01)
        print(".", end="")
        sys.stdout.flush()
    print()
```

If you cannot open the log file when you create the `Git` object (e.g.
because you want to log to the directory that `git clone` will create), you
can use the `set_logger()` method later:

```python
    sandbox = "./sandbox"
    git = Git.clone_repo(repository_url, sandbox=sandbox)
    git.set_logger(FileLogger(sandbox, "git.log"))
```


# Alternatives

There are a number of ways to run `git` commands directly from Python:

- Using `subprocess`:

  ```python
      import subprocess
      subprocess.check_call(["git", "rev-parse", "HEAD"])
      subprocess.check_call(["git", "ls-files"])
  ```

- Using [GitPython](https://gitpython.readthedocs.io/en/stable/tutorial.html#using-git-directly):

  ```python
      from git import Repo
      git = Repo(".").git
      git.rev_parse('HEAD')
      git.ls_files()
  ```

- Using [sh](https://github.com/amoffat/sh) (as recommended in [this post](https://stackoverflow.com/a/8578096)):
   
  ```python 
      import sh
      git = sh.git
      print(git("rev-parse", "HEAD"))
      print(git("ls-files"))
  ```

*Git-Adapter* differs from these solutions in

-   Output handling
-   Logging


# Requirements

*Git-Adapter* currently requires Python 3.6.9 or later.
