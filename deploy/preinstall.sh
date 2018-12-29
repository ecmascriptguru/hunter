sudo apt-get update
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
# sudo -u postgres psql
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
cd ~
mkdir Envs
cd Envs/
virtualenv staging.email.hunter
source staging.email.hunter/bin/activate