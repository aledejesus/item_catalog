# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.box_version = "= 2.3.5"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  # Work around disconnected virtual network cable.
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update
    apt-get -qqy install postgresql python3 python3-pip

    # TODO: make this variables persistent
    # export LC_ALL="en_US.UTF-8"
    # export LC_TYPE="en_US.UTF-8"

    pip3 install -r /vagrant/requirements.txt

    cd /vagrant
    cp .env_example .env
    su postgres -c "psql -f sql/create_user.sql"
    su vagrant -c "createdb catalog"
    flask db upgrade
    su vagrant -c "psql catalog < sql/dump_test.sql"

    vagrantTip="[35m[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant[m"
    echo -e $vagrantTip > /etc/motd

    echo "Done installing your virtual machine!"
  SHELL
end
