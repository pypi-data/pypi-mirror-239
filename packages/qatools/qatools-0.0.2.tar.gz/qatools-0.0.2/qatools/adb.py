#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2023/11/6 7:18 PM
@Desc    :  adb line.
"""
import base64
import os
import platform
import socket
import stat

import psutil

STATICPATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_ADB_PATH = {
    "Windows": os.path.join(STATICPATH, "adb", "windows", "adb.exe"),
    "Darwin": os.path.join(STATICPATH, "adb", "mac", "adb"),
    "Linux": os.path.join(STATICPATH, "adb", "linux", "adb"),
    "Linux-x86_64": os.path.join(STATICPATH, "adb", "linux", "adb"),
    "Linux-armv7l": os.path.join(STATICPATH, "adb", "linux_arm", "adb"),
}


def make_file_executable(file_path):
    """
    If the path does not have executable permissions, execute chmod +x
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        mode = os.lstat(file_path)[stat.ST_MODE]
        executable = True if mode & stat.S_IXUSR else False
        if not executable:
            os.chmod(file_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
    return False


def builtin_adb_path():
    system = platform.system()
    machine = platform.machine()
    adb_path = DEFAULT_ADB_PATH.get(f"{system}-{machine}")
    if not adb_path:
        adb_path = DEFAULT_ADB_PATH.get(system)
    if not adb_path:
        raise RuntimeError(
            f"No adb executable supports this platform({system}-{machine})."
        )

    if system != "Windows":
        # chmod +x adb
        make_file_executable(adb_path)
    return adb_path


def get_adb_path():
    if platform.system() == "Windows":
        ADB_NAME = "adb.exe"
    else:
        ADB_NAME = "adb"

    # Check if adb process is already running
    for process in psutil.process_iter(["name", "exe"]):
        if process.info["name"] == ADB_NAME:
            return process.info["exe"]

    # Check if ANDROID_HOME environment variable exists
    android_home = os.environ.get("ANDROID_HOME")
    if android_home:
        adb_path = os.path.join(android_home, "platform-tools", ADB_NAME)
        if os.path.exists(adb_path):
            return adb_path

    # Use qatools builtin adb path
    adb_path = builtin_adb_path()
    return adb_path


def get_host_ip():
    """
    Query the local ip address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def encryption(value):
    """
    encryption
    :param value:
    :return:
    """
    bytes_url = value.encode("utf-8")
    str_url = base64.b64encode(bytes_url)
    return str_url


def decryption(value):
    """
    decryption
    :param value:
    :return:
    """
    str_url = base64.b64decode(value).decode("utf-8")
    return str_url
