# pre-commit hooks to run tools with uv

This repository contains [pre-commit](https://pre-commit.com) hooks to invoke
various Python-related hooks through [uv](https://docs.astral.sh/uv/). With
these hooks, you can manage dependencies for your hooks in `pyproject.toml`
like any other dependencies.

## Why not use the typical pre-commit hooks for these tools?

pre-commit usually creates isolated environments for each tool. This approach
works well for tools that are implemented in other languages - for example,
tools for Python that are written in TypeScript - or that have dependencies
that may conflict with the repo. However, there are two pain points you might
encounter:

1. Tools that require access to the full set of dependencies to function well,
such as type checkers, may not be able to find these dependencies without
specially configuring pre-commit to also add these dependencies to the tool's
isolated environment.
2. If you also install these tools some other way (for example, to run them
from the command line directly), nothing keeps the tool version in sync between
your pre-commit config and your other method of installing them.

If you use uv, and either of these points apply to you, you may find it easier
to use these hooks and let uv manage the tools.

## How to use these hooks?

To use these hooks, add the following to your `.pre-commit-config.yaml`:
```
- repo: https://github.com/wlritchi/pre-commit-via-uv
  rev: '1.0.0'
  hooks:
  - id: mypy-all-files
  # etc
```

Additionally, you will need to add these tools to your `pyproject.toml` if you
don't already have them installed; unlike most pre-commit hooks, these hooks
will not install them for you.

The configuration and defaults for each hook are generally intended to mirror
the upstream or most commonly used community hook for that tool, if it exists.

## Supported hooks

- [mypy](https://www.mypy-lang.org/)
- [pyright](https://github.com/Microsoft/pyright)

## Hook-specific notes

### all-files hooks

Some hooks can report on more errors if they run against the entire repository
than if they run against individual changed files. By default, pre-commit only
runs hooks against the files that have changed. This repo provides alternate
versions of some hooks, that will run against all files rather than just changed
files. This is nearly equivalent to setting `pass_filenames: false` on the hook,
but with additional checks to avoid running on untracked files. Be advised that
for many hooks, this will incur a **substantial** performance penalty,
especially on larger repos. Supported hooks are:

- `mypy-all-files`
- `pyright-all-files`

Note that these hooks are not currently tested on Windows, and may not correctly
invoke hooks due to shebang weirdness. PRs are welcome!

### Mypy

Some kinds of type error will not be reported by mypy in the default pre-commit
configuration, because pre-commit only runs mypy on files that have been changed
in the current commit. If your commit makes changes that cause type errors in
another file (for example, refactoring an interface but forgetting to update one
implementation of it), the default mypy hook will not warn you about this error.
See the section on all-files hooks for an alternative (but note the performance
impact).

### Pyright

Pyright is not implemented in Python and does not come with its own pre-commit
hook. However, [a Python wrapper](https://pypi.org/project/pyright) exists, and
running the tool through uv using this wrapper may allow Pyright to locate
your dependencies more easily and provide more complete type checking results.
To use the Pyright hook, you will need to add this wrapper to your dev
dependencies, or require that all developers have Pyright installed on their
systems through some other means.

Additionally, some kinds of type error will not be reported by Pyright in the
default pre-commit configuration, because pre-commit only runs Pyright on files
that have been changed in the current commit. If your commit makes changes that
cause type errors in another file (for example, refactoring an interface but
forgetting to update one implementation of it), the default Pyright hook will
not warn you about this error. See the section on all-files hooks for an
alternative (but note the performance impact).
