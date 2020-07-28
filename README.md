# BBBWebserver


run *BBB_LEDserver_main.py* on the BBB (-- without any virtual environment)

Note: To log into BBB via ssh (in case of crash)
        ssh root@192.168.178.56

Sometimes, the FritzBox changes the static IP of the BBB for no reason.
Then, you can find ou the new IP by logging into the FritzBox as Admin
and scan all users of the LAN. BBB should be listed as beagleboard.


After running, visit the website in the local network on:
        192.168.178.56:8050


To start the webserver automatically after a reboot, add a cronjob by editing the crontab:
	crontab -e
and add the following line:
	@reboot python ~/Git/BBBWebserver/BBB_LEDserver_main.py
