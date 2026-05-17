# saltyMac

Welcome to my saltyMac repo!

saltyMac is a demonstration project showing how `SaltStack` can be used to manage and secure macOS systems in a clean, modular, and reproducible way.

The goal of this repo is not just to show individual Salt states, but to demonstrate a complete macOS management workflow using:

- Salt states
- Custom grains
- Custom execution modules
- Pillars
- CI automation
- Masterless Salt workflows
- Automated macOS VM testing

## Why This Repo Exists

The purpose of this project is to show that:

- Salt can manage macOS effectively
- macOS can be treated like infrastructure
- Apple fleet management can benefit from GitOps workflows
- Security configuration can be automated and version controlled
- Linux style automation patterns work extremely well on Macs
- Managing macOS with salt is awesome! 

This repo is intentionally designed as a learning and experimentation environment for MacAdmins interested in infrastructure engineering approaches.

## Why Salt for macOS?

Salt is usually associated with Linux infrastructure but it also works extremely well for macOS management (and Windows!). Using Salt on macOS gives you:

- Infrastructure as Code for Mac fleets
- Reusable and modular configuration management
- Easy automation of security settings
- Powerful remote execution
- Custom Python extensibility
- Git based change management
- Agent based or masterless deployments

## Project Structure

```
saltyMac/
├── ci/
│   ├── ansible/
│   ├── scripts/
│   └── tart/
├── docs/
├── pillar/
├── salt/
│   ├── _grains/
│   ├── _modules/
│   ├── _states/
│   ├── macOS/
│   ├── rosetta/
│   ├── security/
│   ├── smbSigning/
│   ├── saltyStuff/
│   └── top.sls
└── README.md
```

## What Is Included?

### States

The repo includes several example Salt states focused on macOS administration and security hardening.

### macOS States

Located in:
```
/salt/macOS/
```
Examples include:

- Installing Xcode Command Line Tools
- macOS specific configuration management

#### Security States

Located in:
```
/salt/security/
```
These states demonstrate how Salt can manage macOS security controls such as:

- Disabling SSH
- Disabling Guest access
- Disabling Guest SMB access
- Disabling Remote Apple Events
- Configuring firewall settings
- Configuring auditd
- Setting sudo timeout policies
- Disabling auto login
- Enforcing network time settings

This is one of the strongest use cases for Salt on macOS. Security configuration becomes repeatable, testable and version controlled.

### Rosetta Management

Located in:
```
/salt/rosetta/
```
Shows how Salt can manage Apple Silicon compatibility tooling.

### SMB Signing

Located in:
```
/salt/_grains/
```
Example state for configuring SMB signing behaviour.

## Custom Grains

Custom grains allow Salt to collect macOS-specific information that can then be used for targeting or logic inside states.

Included examples:

### battery.py

Collects battery related information from macOS systems.

### macPrinters.py

Collects information about configured printers.

These examples show how Salt can be extended to understand Apple specific system details.

## Custom Execution Modules

Located in:
```
/salt/_modules/
```
Custom modules extend Salt with macOS specific functionality.

Included examples:

### macSoftware.py

Custom software management functionality for macOS.

### commandLineTools.py

Functions for handling Xcode Command Line Tools installation and management. This demonstrates one of Salt's biggest strengths in that you are not limited to built in functionality. You can extend Salt using Python.

## Custom States

Located in:
```
/salt/_states/
```
### commandLineTools.py

A custom Salt state used to manage Xcode Command Line Tools. Custom states allow you to create higher level abstractions tailored to macOS workflows.

## Pillars

Located in:
```
/pillar/
```
Pillars allow sensitive or environment specific data to remain separate from states.

This keeps your Salt code:
- Cleaner
- Reusable
- Easier to maintain
- Safer for production use

## Top File

The repo uses a standard Salt top file:

```
base:
  '*':
    - saltyStuff
    - macOS
    - rosetta
    - security
    - smbSigning
```

This defines which states are applied to minions.

## CI Workflow

One of the goals of this repo is to demonstrate modern Infrastructure as Code workflows for macOS.

The CI pipeline is designed around automated macOS VM testing.

### Workflow Overview

I've included a CI directory for this repo which uses the following:

- Tart
- Packer
- Ansible

Using the above tools you can automate the build of a macOS VM and deploy salt so that you can have a playground to play with salt.

You can install the tools needed using brew. Once you have the tools `cd` into:
```
/ci/tart/
```
Now we need to init packer with `packer init .`. Then build the VM with `packer build .`. Now pop off to make a cuppa. Its going to take awhile to download and build but once complete you will have a fully built VM which requires no input whilst building.

To view the VM run `tart list` in your terminal. You'll see:

```
Source Name     Disk Size Accessed     State  
local  saltyMac 50   30   1 days ago   stopped
```

Start the VM with `tart run saltyMac`. 

Lets look at somethings we can do:


