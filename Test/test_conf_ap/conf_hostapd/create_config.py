#!/usr/bin/env python

from hostapdconf.parser import HostapdConf
from hostapdconf import helpers as ha
import subprocess

def create_hostapd_conf(ssid, password, interface):
    """

    Create a new hostapd.conf with the given ssid, password, interface.

    Overwrites the current config file.

    """
    subprocess.call(['touch', './hostapd.conf'])
    conf = HostapdConf('./hostapd.conf')

    # set some common options
    ha.set_ssid(conf, ssid)
    ha.reveal_ssid(conf)
    ha.set_iface(conf, interface)
    ha.set_driver(conf, ha.STANDARD)
    ha.set_channel(conf, 2)
    ha.enable_wpa(conf, passphrase=password, wpa_mode=ha.WPA2_ONLY)
    ha.set_country(conf, 'ro')

    # my hostapd doesn't like the default values of -1 here, so we set some
    # dummy values
    conf.update({'rts_threshold': 0, 'fragm_threshold': 256})

    print("writing configuration")
    conf.write()

if __name__ == '__main__':
    print("Creating conf file...")
    create_hostapd_conf('test_conf_supplicant', 'password', 'wlan0')
