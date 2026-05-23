## CI Workflow

One of the goals of this repo is to demonstrate modern Infrastructure as Code workflows for macOS. Please see the `CI.md` doc in the `docs` directory for more info.

### Workflow Overview

I've included a CI directory for this repo which uses the following:

- Tart
- Packer
- Ansible

Using the above tools you can automate the build of a macOS VM and deploy salt so that you can have a playground to play with salt.

You can install the tools needed using brew.

## Base VM

There is a packer file to automate the build of a basic macOS VM which we will clone later. `cd` into:

```
/ci/tart/
```

Now we need to init packer with `packer init .`. Then build the VM with `packer build .`. Now pop off to make a cuppa. Its going to take awhile to download and build but once complete you will have a fully built VM which requires no input whilst building.

To view the VM run `tart list` in your terminal. You'll see:

```
Source Name       Disk Size Accessed       State  
local  tahoe-26.2 50   30   17 minutes ago stopped
```

## Clone VM

Now we can clone this VM and put this repo on it ready for you to run salt. `cd` into:

```
/ci/saltyMac
```

Now clone our base VM with:

```
tart clone tahoe-26.2 saltyMac
```

Running `tart list` will show:

```
Source Name       Disk Size Accessed       State  
local  saltyMac   50   28   31 seconds ago stopped
local  tahoe-26.2 50   30   2 minutes ago  stopped
```

Now we can run the `saltyMac.pkr` file in `/ci/saltyMac`. Run `packer init .` to make sure we are ready to go. Then run `packer build .`. 

## Running Salt

Start up the `saltyMac` VM with `tart run saltyMac` and login with the password `admin`. Or SSH in with `ssh admin@$(tart ip saltyMac)`.


Once the mac is up we can run the first salt call to build the mac with:

```
sudo salt-call --local state.apply --file-root="/opt/saltyMac/salt" --pillar-root="/opt/saltyMac/pillar" test=false
```

Once the first run has completed you can run a salt test with:

```
sudo salt-call --local state.apply test=true
```

You can run a full salt build with:

```
sudo salt-call --local state.apply test=false
```

During the first run you will get errors as some plists do not exist but the plists will get added during the first salt call. 
