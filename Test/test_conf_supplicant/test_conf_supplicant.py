#!/usr/bin/env python

import os
import subprocess
import pytest
from xprocess import ProcessStarter


@pytest.fixture
def modprobe_hwsim():
    """
    pytest fixture to install/uninstall the mac80211_hwsim module before/after
    test runs.
    """

    print("Installing mac80211_hwsim module...")
    subprocess.call(['sudo', 'modprobe', 'mac80211_hwsim'])

    yield

    print("Uninstalling mac80211_hwsim module...")
    subprocess.call(['sudo', 'modprobe', '-r', 'mac80211_hwsim'])

@pytest.fixture
def start_AP(xprocess):
    """
    pytest-xprocess fixture that runs hostapd and waits for the AP to be enabled.
    """

    class Starter(ProcessStarter):
        """
        TODO: we need to bring this config file with us. Currently this will only be
              successful if run from /Test
        """
        args = ['sudo', 'hostapd', os.getcwd() + '/conf_hostapd/test_conf_supplicant.hostapd.conf']
        pattern = "wlan0: AP-ENABLED"

    xprocess.ensure("AP", Starter)
    print("Started AP...")
    return True

def test_conf_supplicant(modprobe_hwsim, start_AP):
    """
    With the mac80211_hwsim module installed and the AP running, tests that the
    client can find and connect to the AP.

    TODO: (Pending API implementation) this should implemented via:
           1 - An API call to set the SSID/password.
           2 - An API call to check that it connected.
    """
    pass
