# CSE Poulailler

For Raspberry Pi 3 to 4.

### Enable i2c and Serial interface

I2C/Serial interface is disabled by default in Raspberry Pi, To enable it type below command.

```bash
sudo raspi-config
```

- Now select Interfacing options.
- Now we need to select I2C option.
- Now select Yes and press enter and then ok.

To enable serial,

- select interfacing options.
- Now we need to select serial.
- select no to disable serial over login shell.
- Now select yes to enable serial hardware port then ok.

After this step reboot raspberry by typing below command:

```bash
sudo reboot
```

### Install Required Libraries

```bash
sudo ./setup.sh
```

### Execute programm

```bash
python3 cse_rfid.py
```

