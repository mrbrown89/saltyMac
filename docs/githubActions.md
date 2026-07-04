# GitHub Actions CI

The workflow in [`.github/workflows/saltyAction.yml`](../.github/workflows/saltyAction.yml)
is the repository's automated CI and promotion pipeline. It validates changes
on a real GitHub-hosted macOS runner; the separate [`demo/`](../demo/) directory
is only for building a local VM playground.

## Trigger and branch flow

The workflow runs whenever commits are pushed to the `testing` branch:

```text
push to testing
      |
      v
lint repository
      |
      v
test Salt on macOS
      |
      v
open testing -> main pull request
```

The workflow has `contents: write` and `pull-requests: write` permissions so the
final job can update the CI badge when necessary and create the promotion pull
request.

## Job 1: Lint Repository

The `lint` job runs on Ubuntu and catches inexpensive errors before allocating a
macOS runner. It performs these checks:

- `yamllint` for YAML and Salt state files.
- ShellCheck for repository shell scripts, excluding the vendored
  Installomator script.
- Ruff for custom Python grains, execution modules, and states.
- `ansible-playbook --syntax-check` for playbooks under `demo/ansible`.
- `packer fmt -check` for the Packer demo templates.

If any lint check fails, the macOS and promotion jobs do not run.

## Job 2: Test Salt on macOS

The `test-macos` job depends on `lint` and runs on GitHub's current hosted macOS
image. The helper script `.github/scripts/installSaltMacos.sh`:

1. Downloads and installs the pinned Salt package.
2. copies the checked-out repository to `/opt/saltyMac`.
3. writes a static `salty_ci: true` grain.

The CI grain allows states that require a normal interactive GUI session, such
as Nudge LaunchAgent loading and Remote Apple Events changes, to substitute a
no-op on the hosted runner.

The job calls `saltutil.sync_all` so Salt can load the repository's custom
grains, execution modules, and state modules. It then applies the full highstate
three times to allow dependent resources to converge. Those preliminary runs
continue even if one reports a failure.

A fourth state application is the strict verification step. It does not ignore
the exit code, so the job fails unless the complete Salt configuration applies
successfully.

## Job 3: Promote to Main

The `promote` job runs only after the macOS test succeeds. It checks out the
`testing` branch and:

1. ensures the README contains the workflow status badge;
2. commits and pushes the badge if it was missing;
3. checks for an existing open `testing` to `main` pull request;
4. creates that pull request when one does not already exist.

The workflow opens the pull request but does not merge it. Repository reviewers
retain control over promotion to `main`.

## Updating the workflow

When changing Salt states or the workflow itself, push the change to `testing`
and inspect all three jobs in the repository's **Actions** tab. A green workflow
means linting completed, the final macOS convergence run succeeded, and the
promotion job completed.

The most relevant files are:

- `.github/workflows/saltyAction.yml`: jobs, ordering, and branch promotion.
- `.github/scripts/installSaltMacos.sh`: Salt installation and runner setup.
- `pyproject.toml`: Ruff configuration for Salt-injected Python globals.
- `.yamllint`: YAML lint configuration.
