# epass-barrier-gate
using Python Script to open the barrier gate to let person come out. and also flag the database server (using CakePHP) to know that person has already out, by tapping the ticket.
However this script is running background and auto-start when reboot.

# Install
In order to run background script, we need to create service first :

```
sudo make install
```

# Run
After installing the service, run it.

```
sudo make run
```

# Uninstall
To remove the service, just input following command in terminal :

```
sudo make uninstall
```

# Check Status Service

```
sudo systemctl status epass.service
```
