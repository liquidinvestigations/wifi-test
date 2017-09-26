#!/usr/bin/env python

import os
import subprocess
import pytest
from xprocess import ProcessStarter


@pytest.fixture
def modprobe_hwsim():
    """
    pytest fixture to install/uninstall the mac80211_hwsim module before/after
    test runs. defaults to two simulated radios.
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

    class APStarter(ProcessStarter):
        test_dir = os.path.dirname(__file__)
        args = ['sudo', 'hostapd', os.path.join(test_dir, 'conf_hostapd/hostapd.conf')]
        pattern = "wlan0: AP-ENABLED"

    xprocess.ensure("AP", APStarter)
    print("Started AP...")
    return True

@pytest.fixture
def start_supplicant(xprocess):
    """
    pytest-xprocess fixture that runs wpa_supplicant and waits for it to connect
    to the AP.
    """

    class SupplicantStarter(ProcessStarter):
        test_dir = os.path.dirname(__file__)
        args = ['sudo', 'wpa_supplicant', '-i', 'wlan1', '-c', os.path.join(test_dir, 'conf_supplicant/wpa_supplicant.conf')]
        pattern = "wlan1: CTRL-EVENT-CONNECTED"

    xprocess.ensure("supplicant", SupplicantStarter)
    print("Started supplicant...")
    return True

def test_conf(modprobe_hwsim, start_AP, start_supplicant):
    print("TODO: verify connection via iw")
    pass
