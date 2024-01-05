#!usr/bin/bash
# Update and upgrade the system

sudo apt update && sudo apt upgrade -y


# Install puppet for automated setup
sudo apt-get install -y ruby ruby-augeas ruby-shadow puppet
sudo gem install puppet-lint

# Install python 3.11.5 if it doesn't exist as well as pip and set it to be python3
sudo puppet apply setup.pp

# create the virtual environment for the project development

