 
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
sudo i2cdetect -y 1
git clone https://github.com/jwgit2/CSE-Poulailler.git
cd CSE-Poulailler
python3 cse_rfid.py