packer {
  required_plugins {
    tart = {
      version = ">= 1.16.0"
      source  = "github.com/cirruslabs/tart"
    }
    ansible = {
      version = "~> 1"
      source  = "github.com/hashicorp/ansible"
    }
  }
}

source "tart-cli" "saltyMac" {
  vm_name      = "saltyMac"
  ssh_username = "admin"
  ssh_password = "admin"
  ssh_timeout  = "180s"
}

build {
  sources = ["source.tart-cli.saltyMac"]

  ###################################
  # Clone saltyMac repository
  ###################################

  provisioner "ansible" {
    playbook_file   = "../ansible/cloneRepo.yml"
    user            = "admin"
    extra_arguments = ["--extra-vars", "ansible_become_pass=admin"]
  }

  ###################################
  # Synchronise custom Salt modules
  ###################################

  provisioner "shell" {
    inline = [
      "sudo /opt/salt/salt-call --local saltutil.sync_all --file-root=/opt/saltyMac/salt --pillar-root=/opt/saltyMac/pillar"
    ]
  }
}
