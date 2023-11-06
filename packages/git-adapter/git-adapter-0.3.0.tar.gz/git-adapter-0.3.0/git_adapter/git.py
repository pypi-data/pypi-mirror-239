#!/usr/bin/python3
# -*- coding: utf-8 -*-   vim: set fileencoding=utf-8 :

"""A Git repository on which we can run commands.

The Git class has a few specific commands, like git.hard_reset() or
git.current_branch(), defined below.

Any other method call 'git.<CMD>(…)' is converted to a system call
'git CMD …', e.g.
    from git_adapter.git import Git

    greedy_git = Git(sandbox=".")
    greedy_git.fetch("origin")
    # or
    lazy_git = Git(sandbox=".").lazy
    lazy_git.fetch("origin").run()


Note that in the command name and in the keyword arguments, underscores are mapped to
hyphens, so there currently is no way to call `git strange_command --strange_option`,
because git_adapter would try to call 'git strange-command --strange-option' instead.


Example usage:
    git = Git.clone_repo("git@git.host:test-repo")
    log_lines: Iterator[str] = git.log(first_parent=True, max_count=20, author="me")

    for file_ in git.ls_files():
        print("Git ile:", file_)

    with open("greeting.txt", "w") as fh:
        fh.write("Hello world\\n")
    git.commit("greeting.txt", m="Greet the world.", author="me")

    origin = git.remote().first_line()
    branch = git.current_branch()
    git.push(origin, branch)

    # Python reserved keywords have to be escaped with a trailing
    # underscore:
    matches = git.grep("keyword", break_=True, heading=True).lines()

    # Catch errors
    try:
        git.fetch("non-existing-origin").first_line()
    except CmdError as e:
        print("Got error {} when running {}".format(e.returncode, e.cmd_line))
        print("Error message:\n  {}".format("\n  ".join(e.error_lines)))


There are two versions of the API, which we call greedy and a lazy.
- A GreedyCommand immediately runs and consumes all its output before the call finishes.
- A LazyCommand is initiated at construction time and immediately starts to relay any
  output it receives.

Syntactically, the greedy API is closer to how one would call git from the command line:

    from git_adapter.git import Git  # greedy API
    git = Git(sandbox=".")

    # Commands are immediately called.
    # The next line returns only when the command has finished:
    git.fetch("origin")

    file="modified.txt"
    git.add(file)
                          ↦ git add modified.txt
    git.commit(m="T'was brillig.", author="me")
                          ↦ git commit -m "T'was brillig." --author=me
    git.worktree.add(PATH, BRANCH)
                          ↦ git worktree add PATH BRANCH

    # Retrieve the fist line of output
    head = git.rev_parse("HEAD").first_line()

    # The GreedyCommand is iterable and generates the lines of output
    for line in git.log(first_parent=True, max_count=20, author="me"):
        print("  ", line)
                          ↦ git log --first-parent --max-count=20 --author=me

Using the lazy API, we need to explicitly call the `run()` method in ordre to execute a
git command:

    from git_adapter.git import Git
    git = Git(sandbox=".").lazy  # lazy API

    # We need to explicitly call `run()` to execute the command
    git.fetch("origin").run()

    file="modified.txt"
    git.add(file).run()
                          ↦ git add modified.txt
    git.commit(m="T'was brillig.", author="me").run()
                          ↦ git commit -m "T'was brillig." --author=me
    git.worktree.add(PATH, BRANCH).run()
                          ↦ git worktree add PATH BRANCH

    # Retrieve the fist line of output and stop execution.
    # If you need more lines (or need the command to finish), use `lines()` instead.
    head = git.rev_parse("HEAD").first_line()

    # We need to explicitly call `lines()` to iterate over the output
    for line in git.log(first_parent=True, max_count=20, author="me").lines():
        print("  ", line)
                          ↦ git log --first-parent --max-count=20 --author=me

The difference between greedy and lazy commands is most obvious for for long-running git
commands that produce lots of output.

The greedy version will collect all output and run the command until it is complete,
even if we consume only a part of the output:

    git = Git(sandbox=".")  # greedy API
    for line in git.rev_list(objects=True, all=True).lines():
        # It may take a long time ere we start processing the first line
        if "Makefile" in line:
            print(line, end="")
            break  # has already consumed all lines of output

The lazy version yields the lines of output immediately as they are written by the
process:

    git = Git(sandbox=".").lazy  # lazy API
    for line in git.rev_list(objects=True, all=True).lines():
        # Starts immediately when the first line of output arrives
        if "Makefile" in line:
            print(line, end="")
            break  # interrupts the command

Both APIs can be used together:

    git = Git(sandbox=".")

    # We don't expect these commands to produce much output, so run them greedily:
    git.fetch(all=True)
    git.commit(m="T'was brillig.", author="me")

    # This, however, may generate lots of output and we want immediate results:
    for line in git.lazy.rev_list(objects=True, all=True).lines():
        if "Makefile" in line:
            print(line, end="")
            break  # interrupts the command

    # Here it doesn't matter much which API we use:
    git.merge("@{u}")


The Git class is derived from the more general Command class that can be
used in a similar manner:
    ip = Command(["ip"])
    ip.address.show().lines()             ↦ ip address show
    ip.address.show("dev", "lo").lines()  ↦ ip address show dev lo
    ip.address.show.dev("lo").lines()     ↦ ditto
    ip.address.show.dev.lo().lines()      ↦ ditto

"""


import os
import re
import subprocess
import sys
import traceback
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict, Iterator, List, NoReturn, Optional, Type, Union

# All(?) reserved words in Python, based on
# https://docs.python.org/3.8/reference/lexical_analysis.html#identifiers
PYTHON_RESERVED_WORDS = [
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "False",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "None",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "True",
    "try",
    "while",
    "with",
    "yield",
]


version = (0, 3, 0)


class Command(ABC):
    """A (shell) command that takes subcommands.

    Examples (replace Command with either GreedyCommand or LazyCommand):
      list(Command(["ls"])("-l"))                         # collect output from 'ls -l'
      Command(["ip"]).link.set.eth0.up().run()            # run 'ip address show'
      Command(["ip", "link", "set", "eth0", "up"]).run()  # ditto
      Command(["git"]).reset("@{u}").run()                # run 'git reset @{u}'
    """

    def __init__(
        self,
        cmd: List[str],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        """Create a Command object.
        Arguments:
            cmd:
                The command to call, as list of words.
                E.g. ["ls"], ["git", "worktree", "add"].
            cwd:
                Directory where the command will be run.
            env:
                A dict for setting environment variables for the command's
                process.
                If not set, the environment is inherited from os.environ.
            logger:
                A Logger object to log actions and output.
                The default is to use a NullLogger that will only print
                output if an error occurs.
            verbose:
                If True, use a StdoutLogger as default logger.
        """
        self.cmd = cmd
        self.cwd = cwd
        if env is None:
            self.environ = dict(os.environ)
        else:
            self.environ = dict(env)
        if logger:
            self.logger = logger  # type: Logger
        else:
            if verbose:
                self.logger = StdoutLogger()
            else:
                self.logger = NullLogger()

        # self.constructor = cast(Type[Command], None)  # will be overwritten

    def __getattr__(self, attribute: str) -> Any:
        """Map undefined attributes to commands."""
        constructor = self.__dict__["constructor"]
        return self.create_attr(attribute, constructor)

    def create_attr(self, attribute: str, clazz: Type["Command"]) -> "Command":
        """Map undefined attributes to commands."""
        kwargs: Dict[str, Any] = {}
        if self.logger:
            kwargs["logger"] = self.logger
        if self.cwd is not None:
            kwargs["cwd"] = self.cwd
        return clazz(cmd=self.cmd + [attribute], **kwargs)

    def update_env(self, env: Dict[str, str]) -> None:
        """Set/overwrite entries in the command's environment."""
        self.environ = {**self.environ, **env}

    def set_logger(self, logger: "Logger") -> None:
        """Set the logger for this Command object."""
        self.logger = logger

    @abstractmethod
    def __call__(
        self, *args: str, override_cwd: Optional[str] = None, **kwargs: str
    ) -> "Process":
        pass

    def call(
        self, lazy: bool, override_cwd: Optional[str] = None, *args: str, **kwargs: str
    ) -> "Process":
        """
        Arguments:
            lazy:
                If true, run lazily, otherwise run greedily.
            override_cwd:
                If given, run the command line from this directory, otherwise run it
                from self.cwd . This is needed for git.clone() which needs to run from
                outside git.sandbox .
            args:
                Handed on to the git command. E.g.
                   git.log("HEAD") ↦ got log HEAD
            kwargs:
                Keyword arguments that are mapped to command-line options
                for the git command. E.g.
                    self.commit(m="T'was brillig.", author="me")
                        ↦ git commit -m "T'was brillig." --author=me
        Returns:
            A string generator representing the lines of output from the
            git command.

        """
        adjusted_cmd = self._restore_names(self.cmd)
        git_cli_options = self._kwargs_to_options(kwargs)
        cmd_line = [*adjusted_cmd, *git_cli_options, *args]

        if override_cwd is None:
            cwd = self.cwd
        else:
            cwd = override_cwd
        return run_cmd(
            cmd_line,
            lazy=lazy,
            env=self.environ,
            logger=self.logger,
            cwd=cwd,
        )

    @staticmethod
    def _restore_names(cmd: List[str]) -> List[str]:
        """Revert underscores to hyphens."""
        return [part.replace("_", "-") for part in cmd]

    def _kwargs_to_options(self, kwargs: Dict[str, str]) -> List[str]:
        options = []
        for opt, value in kwargs.items():
            opt = self._reconstruct_option(opt)
            if len(opt) == 1:
                fmt = "-{}"
            else:
                fmt = "--{}"
            option = fmt.format(opt.replace("_", "-"))
            if isinstance(value, bool):
                if not value:
                    option = re.sub(r"^--", "--no-", option)
                options.append(option)
            else:
                options.append(option + "=" + str(value))
        return options

    @staticmethod
    def _reconstruct_option(parameter_name: str) -> str:
        """We cannot use Python keywords as parameter names.

        So we have appended an underscore to them that needs to be removed
        here.

        """
        if parameter_name[-1] != "_":
            return parameter_name
        keyword = parameter_name[:-1]
        if keyword in PYTHON_RESERVED_WORDS:
            return keyword
        else:
            raise Exception(
                "Unexpected escaped parameter:"
                " is {} really a reserved keyword in Python??".format(keyword)
            )


class GreedyCommand(Command):
    """A (shell) command that runs immediately.

    All output isconsumed and stored, and the constructor returns only when the process
    has finished.
    """

    def __init__(
        self,
        cmd: List[str],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        super().__init__(cmd, cwd, env, logger, verbose)
        self.constructor = GreedyCommand

    def __call__(
        self, *args: str, override_cwd: Optional[str] = None, **kwargs: str
    ) -> "Process":
        return self.call(False, override_cwd, *args, **kwargs)


class LazyCommand(Command):
    """A (shell) command that will be run when some of its methods are called.

    self.run()                # run command, discarding output.
    generator = self.list()   # run command, return iterator over output
    line = self.first_line()  # run command till first line of output is written,
                              # then stop it and return that line
    """

    def __init__(
        self,
        cmd: List[str],
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        super().__init__(cmd, cwd, env, logger, verbose)
        self.constructor = LazyCommand

    def __call__(
        self, *args: str, override_cwd: Optional[str] = None, **kwargs: str
    ) -> "Process":
        return self.call(True, override_cwd, *args, **kwargs)


class AbstractGit(Command):
    """Base class for the two git classes"""

    __metaclass__ = ABCMeta

    def __init__(
        self,
        sandbox: str,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        super().__init__(["git"], sandbox, env, logger, verbose)
        self.sandbox = sandbox

    def hard_reset(self) -> None:
        """Clean up and do a hard reset."""
        self.reset(".")
        self.checkout(".")
        self.clean("--force", "-d", "-x", "-q")
        self.reset("--hard")

    def current_branch(self) -> Optional[str]:
        """Return the current branch."""
        for line in self.branch().iterator():
            m = re.search(r"^\* +(?P<branch>\S+)$", line)
            if m:
                return m.group("branch")
        return None


class Git(AbstractGit, GreedyCommand):
    """Class to run git commands greedily."""

    def __init__(
        self,
        sandbox: str,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        """Create a Git object.

        Arguments:
            sandbox:
                Directory where the git commands will be applied [unless overridden with
                git.CMD(override_cwd=...)].
            env:
                A dict for setting environment variables for the git
                process.
                If set, defines the complete environment.
                If not set, the environment is inherited from os.environ.
            logger:
                A Logger object to log actions and output.
                The default is to use a NullLogger that will only print
                output if an error occurs.
            verbose:
                If True, use a StdoutLogger as default logger.
                This will log the git commands and all of their output.

        """
        super().__init__(sandbox, env, logger, verbose)
        self.sandbox = sandbox
        self.lazy = LazyGit(sandbox, env, logger, verbose)

    @staticmethod
    def clone_repo(
        url: str,
        sandbox: Optional[str] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
        **kwargs: str,
    ) -> "Git":
        """Clone a Git repository
        Arguments:
            url:
                Check out a Git repository from that URL.
            sandbox:
                Name of the directory to be checked out.
            env:
                A dict for setting environment variables for the git
                process.
                If set, defines the complete environment.
                If not set, the environment is inherited from os.environ.
            logger:
                A Logger object to log actions and output.
                The default is to use a NullLogger that will only print
                output if an error occurs.
            verbose:
                If True, use a StdoutLogger as default logger.

        Returns:
            A Git object providing access to the clone.

        """
        if sandbox is None:
            # Guess the default name for sandbox
            m = re.search(
                r".* : (?: .* /)? (?P<name> [^:/]*?) (?: \.git)? $",
                url,
                flags=re.VERBOSE,
            )
            if m:
                sandbox = m.group("name")
            else:
                raise CmdError(
                    None,
                    "Failed to guess sandbox name for url {}".format(url),
                )

        git = Git(sandbox, logger=logger, verbose=verbose)
        git.clone(url, "--quiet", sandbox, override_cwd=".", **kwargs)
        return git

    def __repr__(self) -> str:
        return "git_adapter.git.Git('{}')".format(self.sandbox)


class LazyGit(AbstractGit, LazyCommand):
    """Class to run git commands greedily."""

    def __init__(
        self,
        sandbox: str,
        env: Optional[Dict[str, str]] = None,
        logger: Optional["Logger"] = None,
        verbose: bool = False,
    ) -> None:
        """Create a Git object.

        Arguments:
            sandbox:
                Directory where the git commands will be applied [unless overridden with
                git.CMD(override_cwd=...)].
            env:
                A dict for setting environment variables for the git
                process.
                If set, defines the complete environment.
                If not set, the environment is inherited from os.environ.
            logger:
                A Logger object to log actions and output.
                The default is to use a NullLogger that will only print
                output if an error occurs.
            verbose:
                If True, use a StdoutLogger as default logger.

        """
        super().__init__(sandbox, env, logger, verbose)

    def __repr__(self) -> str:
        return "git_adapter.git.LazyGit('{}')".format(self.sandbox)


class Logger(ABC):
    """A logging interface."""

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        """Log one or several lines.

        Arguments:
            msg:
                One string or a list of strings representing the line(s)
                to log.
            indent:
                Indent each line by this many space characters.
            separator:
                If True, print one empty separator line before msg.
        """
        raise Exception("Abstract method not implemented")

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        """Make sure to write one or several lines.

        Arguments are as for self.log().

        """
        raise Exception("Abstract method not implemented")

    def error(self) -> None:
        """An error has occurred: apply some wind-up procedure."""
        raise Exception("Abstract method not implemented")

    @staticmethod
    def _pack_as_list(msg: Union[str, List[str]]) -> List[str]:
        """Convert one string or a list of strings to a list of strings"""
        if isinstance(msg, str):
            return [msg]
        else:
            return msg


class FileLogger(Logger):
    """Log to file and stdout."""

    def __init__(self, log_dir: str, log_file: str, separator: int = 1) -> None:
        """Create a FileLogger.

        Parameters:
            log_dir:
                Directory to write the log file to.
            log_file:
                The name of the log file.
            separator:
                Print that many empty lines to stdout.
        """
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        for i in range(separator):
            print()
        self.fh = open(os.path.join(log_dir, log_file), "w")
        self.empty = True

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        if separator and not self.empty:
            self._print()
        messages = Logger._pack_as_list(msg)
        for line in messages:
            self._log_one_line(line, indent=indent)
        self.fh.flush()

    def _log_one_line(self, line: str, indent: int = 0) -> None:
        line = line.rstrip()
        if line:
            prefix = " " * indent
            self._print(prefix + line)
        else:
            self._print()

    def _print(self, line: str = "") -> None:
        print(line)
        self.fh.write(line + "\n")
        self.empty = False

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        self.log(msg, indent=indent, separator=separator)

    def error(self) -> None:
        # Each line of output has already been printed
        pass


class StdoutLogger(Logger):
    """Log to stdout.

    This logger can be used before any directories for logging output are
    set up.

    """

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        if separator:
            print()
        messages = Logger._pack_as_list(msg)
        for line in messages:
            print(line)

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        self.log(msg, indent=indent, separator=separator)

    def error(self) -> None:
        # Each line of output has already been printed
        pass


class NullLogger(Logger):
    """Don't log unless we encounter errors."""

    def __init__(self) -> None:
        self.output = []  # type: List[str]

    def log(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        self.output.extend(Logger._pack_as_list(msg))

    def write(
        self,
        msg: Union[str, List[str]] = "",
        indent: int = 0,
        separator: bool = False,
    ) -> None:
        messages = Logger._pack_as_list(msg)
        for line in messages:
            print(line)

    def error(self) -> None:
        for line in self.output:
            print(line)


class CmdError(Exception):
    """There was an error when running a command.

    The return status is stored in self.returncode, and the output to stderr (clipped to
    ≤ 4096 bytes) is stored in self.error_lines.
    """

    def __init__(
        self,
        cmd_line: Optional[List[str]],
        error_str: str,
        returncode: Optional[int] = None,
    ) -> None:
        self.cmd_line = cmd_line
        self.returncode = returncode
        self.error_lines = []
        if cmd_line:
            self.error_lines += ["Command '{}' failed:".format(" ".join(cmd_line))]
        self.error_lines += error_str.splitlines()


class Process(ABC):
    """Run a command and provide lines of output as strings."""

    def __init__(
        self,
        cmd_line: List[str],
        env: Optional[Dict[str, str]],
        logger: Optional[Logger],
        verbose: bool,
        cwd: Optional[str],
        raise_exception: bool,
    ) -> None:
        self.cmd_line = cmd_line
        self.env = env
        if logger:
            self.logger = logger
        else:
            if verbose:
                self.logger = StdoutLogger()
            else:
                self.logger = NullLogger()
        self.verbose = verbose
        self.cwd = cwd
        self.raise_exception = raise_exception

    @abstractmethod
    def iterator(self) -> Iterator[str]:
        raise Exception("Not implemented in abstract base class")

    @abstractmethod
    def first_line(self) -> str:
        raise Exception("Not implemented in abstract base class")

    @abstractmethod
    def has_output(self) -> bool:
        raise Exception("Not implemented in abstract base class")


class GreedyProcess(Process):
    """An Process that reads all lines of output immediately."""

    def __init__(
        self,
        cmd_line: list[str],
        env: Optional[Dict[str, str]] = None,
        logger: Optional[Logger] = None,
        verbose: bool = False,
        cwd: Optional[str] = None,
        raise_exception: bool = True,
    ) -> None:
        super().__init__(cmd_line, env, logger, verbose, cwd, raise_exception)
        self.lines = []

        try:
            with subprocess.Popen(
                # Use stdbuff to unbuffer stdout, in order to get
                # immediate output and correct interspersing of stdout and
                # stderr. Note that this will still not work for arbitrary
                # commands in cmd_line.
                # In particular, for a Python script that mixes print
                # statements and output from subprocess, when run with
                # Python 2.7, stdbuf works as expected, while the script
                # running with Python 3.8 still buffers the output (and
                # git_adapter accordingly gets the output in wrong order).
                ["stdbuf", "-o0"] + cmd_line,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                env=env,
                universal_newlines=True,
            ) as process:
                output = process.stdout
                assert output is not None  # appease mypy
                for raw_line in output:
                    line = raw_line.rstrip()
                    self.logger.log(line, indent=2)
                    self.lines.append(line)
                status = process.wait()
                if status != 0:
                    self._handle_error(status)
        except OSError as e:
            raise subprocess.CalledProcessError(e.errno, cmd_line, str(e))

    def __iter__(self) -> Iterator[str]:
        """Allow iterating over the lines of output."""
        for line in self.lines:
            yield line

    def iterator(self) -> Iterator[str]:
        """Allow iterating over the lines of output."""
        yield from iter(self)

    def first_line(self) -> str:
        """Return the first line of output, or the empty string."""
        if len(self.lines) >= 1:
            return self.lines[0]
        else:
            return ""

    def has_output(self) -> bool:
        """Return True if this command produces any output."""
        return bool(self.lines)

    def _handle_error(self, status: int) -> NoReturn:
        if self.raise_exception:
            raise CmdError(
                self.cmd_line,
                error_str="\n".join(self.lines),
                returncode=status,
            )
        else:
            self.logger.error()
            self.logger.write("An error occurred when running the command")
            self.logger.write("  " + subprocess.list2cmdline(self.cmd_line))
            self.logger.write("Aborting.")
            self.logger.write(traceback.format_exc().split("\n"))
            sys.exit(1)


class LazyProcess(Process):
    """An Process that forwards each line of output immediately.

    We read the first line of output immediately, but later output is only retrieved as
    it is requested.
    In particular, self.first_line() will read only the first line of output and then
    close the process, thus aborting it if it isn't finished yet.
    """

    def __init__(
        self,
        cmd_line: list[str],
        env: Optional[Dict[str, str]] = None,
        logger: Optional[Logger] = None,
        verbose: bool = False,
        cwd: Optional[str] = None,
        raise_exception: bool = True,
    ) -> None:
        super().__init__(cmd_line, env, logger, verbose, cwd, raise_exception)

        try:
            self.process = subprocess.Popen(
                # Use stdbuff to unbuffer stdout, in order to get
                # immediate output and correct interspersing of stdout and
                # stderr. Note that this will still not work for arbitrary
                # commands in cmd_line.
                # In particular, for a Python script that mixes print
                # statements and output from subprocess, when run with
                # Python 2.7, stdbuf works as expected, while the script
                # running with Python 3.8 still buffers the output (and
                # git_adapter accordingly gets the output in wrong order).
                ["stdbuf", "-o0"] + cmd_line,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                env=env,
                universal_newlines=True,
            )
            assert self.process.stdout is not None  # appease mypy
            self.stdout = self.process.stdout
            assert self.process.stderr is not None  # appease mypy
            self.stderr = self.process.stderr
        except OSError as e:
            raise subprocess.CalledProcessError(e.errno, cmd_line, str(e))

        # Fetch the first line of output (if any) and verify that the process is still
        # alive.
        # For a command that does not produce any output for a long time, this means
        # that the client code will wait, rather than doing other useful things before
        # looking for output. But this seems to be the only way to get a CmdError
        # immediately from the Process constructor [i.e. from cmd.__call__()]
        # when we have an immediate error in the command line.
        self.line1 = self.stdout.readline().rstrip()
        self.logger.log(self.line1, indent=2)
        current_status = self.process.poll()
        if current_status is not None:
            # Process has already finished
            self._wind_up(current_status)

    def run(self) -> None:
        for _ in self.stdout.read():
            pass
        self.process.wait()

    def lines(self) -> Iterator[str]:
        yield self.line1

        for raw_line in self.stdout:
            line = raw_line.rstrip()
            self.logger.log(line, indent=2)
            yield line
        self._close()

    def first_line(self) -> str:
        """Return the first line of output and close the generator.

        Many programs don't like their output to be truncated, so this method discards
        any error status.

        If you need more than the very first line, use self.__iter__() instead.
        """
        self.stdout.close()
        self.stderr.close()
        self.process.wait()
        return self.line1

    def has_output(self) -> bool:
        """Return True if this command produces any output."""
        return bool(self.line1)

    def iterator(self) -> Iterator[str]:
        yield from self.lines()

    def _close(self) -> None:
        status = self.process.wait()
        self._wind_up(status)

    def _wind_up(self, status: int) -> None:
        max_error_bytes = 4096
        error_output = self.stderr.read(max_error_bytes)
        if status != 0:
            if self.raise_exception:
                raise CmdError(self.cmd_line, error_output, status)
            else:
                self.logger.error()
                self.logger.write("An error occurred when running the command")
                self.logger.write("  " + " ".join(self.cmd_line))
                self.logger.write("Aborting.")
                self.logger.write(traceback.format_exc().split("\n"))
                sys.exit(1)
        self.closed = True


def run_cmd(
    cmd_line: List[str],
    lazy: bool = False,
    env: Optional[Dict[str, str]] = None,
    logger: Optional[Logger] = None,
    verbose: bool = False,
    cwd: Optional[str] = None,
    raise_exception: bool = True,
) -> Process:
    """Run a shell command.

    Parameters:
        cmd_line:
            The command [cmd, arg1, …] to run.
        lazy:
            If True, run command lazily, otherwise run greedily.
        env:
            A dict for setting environment variables for the process.
            If set, defines the complete environment.
            If not set, the environment is inherited from os.environ.
        logger:
            A Logger object that logs all output (interspersed stdout
            and stderr) from the shell command.
            The default is to use a NullLogger that will only print output
            if an error occurs.
        verbose:
            If True, use a StdoutLogger as default logger.
        cwd:
            Directory in which to execute the command. If None, use '.'.
        raise_exception:
            When the system command fails: If raise_exception=True, raise
            a CalledProcessError, if False, exit with status 1.
    Returns:
        A string generator representing the lines ouf output.
    Raises:
        CalledProcessError if the command failed and raise_exception is
        True.

    """
    if cwd is None:
        cwd = "."
    if logger:
        logger_ = logger
    else:
        if verbose:
            logger_ = StdoutLogger()
        else:
            logger_ = NullLogger()
    # logger_.log(
    #     "{}  [running from: {}]".format(_format_cmd_line(cmd_line), cwd), separator=True
    # )
    logger_.log("{}".format(_format_cmd_line(cmd_line)), separator=True)

    if lazy:
        return LazyProcess(cmd_line, env, logger, verbose, cwd, raise_exception)
    else:
        return GreedyProcess(cmd_line, env, logger, verbose, cwd, raise_exception)


def _format_cmd_line(cmd_line: List[str]) -> str:
    """Format a shell command line.

    Try to use quotation marks where needed.
    No attempt is made to handle cases where both sorts of quotation marks
    would be needed in one argument.

    """
    line = []
    for part in cmd_line:
        if " " not in part:
            line.append(part)
            continue
        if "'" not in part:
            line.append("'{}'".format(part))
            continue
        line.append('"{}"'.format(part))
    return " ".join(line)


# Local Variables:
#   compile-command: (concat "mypy --ignore-missing-imports --strict \
#     " (file-name-nondirectory buffer-file-name))
# End:
