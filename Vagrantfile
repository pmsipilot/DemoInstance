# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box_url = "https://atlas.hashicorp.com/debian/jessie64"
  config.vm.box = "debian/jessie64"
  
  config.vm.provider :virtualbox do |v, override|
    v.customize ["modifyvm", :id, "--memory", 1024]
    v.customize ["modifyvm", :id, "--cpus", 1]
    override.vm.synced_folder ".", "/opt/demoinstance", :id => "vagrant-root", owner: "root", group: "root", :mount_options => ["dmode=777", "fmode=777"]
  end

  config.vm.usable_port_range = (2200..2299)
  config.vm.network "forwarded_port", guest: 8080,    host: 2280, auto_correct: true
  config.vm.network "forwarded_port", guest: 8081,    host: 2281, auto_correct: true

  config.vm.define :master do |master|
    master.vm.provision "shell" do |sh|
      sh.path = "ressources/vagrant_setup.sh"
    end
  end
end