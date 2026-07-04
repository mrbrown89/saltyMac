# saltyMac VM Demo

This directory contains an optional local demo environment for saltyMac. It
uses Tart, Packer, and Ansible to build a disposable macOS virtual machine in
which you can run and modify the Salt states safely.

This is not the repository's CI system. Automated validation is handled by
GitHub Actions and is documented in
[docs/githubActions.md](../docs/githubActions.md).

## Prerequisites

Run the demo on an Apple silicon Mac with enough free disk space for the macOS
restore image and VMs. Install these tools before continuing:

- [Tart](https://tart.run/)
- [Packer](https://developer.hashicorp.com/packer)
- [Ansible](https://docs.ansible.com/)

They can be installed with Homebrew:

```bash
brew install cirruslabs/cli/tart hashicorp/tap/packer ansible
```

Run all commands below from a clone of this repository.

## 1. Build the base macOS VM

The Packer template in `demo/tart` creates a base macOS VM called
`tahoe-26.2`. It downloads a macOS restore image, completes Setup Assistant,
enables remote access, and prepares an `admin` account.

```bash
cd demo/tart
packer init .
packer build .
```

The first build can take a while because it downloads and installs macOS. Check
the result with:

```bash
tart list
```

## 2. Create the saltyMac demo VM

Return to the repository root, clone the base VM, and run the second Packer
template:

```bash
cd ../..
tart clone tahoe-26.2 saltyMac
cd demo/saltyMac
packer init .
packer build .
```

This template uses Ansible to clone the `main` branch of this repository into
`/opt/saltyMac` inside the VM. Consequently, uncommitted local changes are not
copied into the demo VM.

## 3. Start and access the VM

Start the VM:

```bash
tart run saltyMac
```

Log in once through the VM window with username `admin` and password `admin`.
Keeping an active GUI login is useful for states that interact with the console
user or LaunchAgents.

You can then connect from another terminal:

```bash
ssh admin@"$(tart ip saltyMac)"
```

The credentials are deliberately simple because this VM is only a disposable
local demo. Do not expose it to an untrusted network or reuse these credentials
for a real system.

## 4. Run Salt

First synchronize the custom execution modules, states, and grains:

```bash
sudo salt-call --local saltutil.sync_all \
  --file-root="/opt/saltyMac/salt" \
  --pillar-root="/opt/saltyMac/pillar"
```

Apply the complete configuration:

```bash
sudo salt-call --local state.apply saltenv=base \
  --file-root="/opt/saltyMac/salt" \
  --pillar-root="/opt/saltyMac/pillar"
```

The first run also writes the masterless Salt configuration. Subsequent runs
can therefore use the shorter command:

```bash
sudo salt-call --local state.apply
```

Run it again to verify convergence: a correctly converged state should report
few or no additional changes. To preview changes without applying them, use:

```bash
sudo salt-call --local state.apply test=True
```

## Demo layout

- `tart/`: Packer template that creates the reusable base macOS VM.
- `saltyMac/`: Packer template that provisions the cloned demo VM.
- `ansible/`: playbooks used by the Packer templates.
- `scripts/`: bootstrap and Homebrew installation helpers.

To discard the demo machines when finished:

```bash
tart delete saltyMac
tart delete tahoe-26.2
```
