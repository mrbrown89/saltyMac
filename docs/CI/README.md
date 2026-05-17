## CI Workflow

One of the goals of this repo is to demonstrate modern Infrastructure as Code workflows for macOS. Please see the `CI.md` doc in the `docs` directory for more info.

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
