#!usr/bin/bash
# Update and upgrade the system

sudo apt update && sudo apt upgrade -y


# Install puppet for automated setup
sudo apt-get install -y ruby ruby-augeas ruby-shadow puppet
sudo gem install puppet-lint

# Recommended to use python3. Run this to set it up if the server doesn't have python
sudo puppet apply prep_for_python.pp
sudo ln -s /usr/local/bin/python3.11 /usr/bin/python
cd /tmp/Python-3.11.5
sudo make altinstall
sudo ln -s /usr/local/bin/python3.11.5 /usr/local/bin/python,
cd -


# Set up the environment

# create the virtual environment for the project development
