# -*- coding: utf-8 -*-
"""
Absfuyu: Fun
---
Some fun or weird stuff

Version: 1.0.0
Date updated: 25/05/2023 (dd/mm/yyyy)

Feature:
- zodiac_sign
- happy_new_year
- im_bored
"""


# Module level
###########################################################################
__all__ = [
    "happy_new_year", "zodiac_sign", "im_bored"
]


# Library
###########################################################################
from datetime import date
import subprocess
import sys

from absfuyu.logger import logger
from absfuyu.util.api import APIRequest


# Function
###########################################################################
def zodiac_sign(
        day: int,
        month: int,
        zodiac13: bool = False,
    ):
    """
    Calculate zodiac sign

    Include 13 zodiacs mode
    """

    # Condition check
    conditions = [
        0 < day < 32,
        0 < month < 13,
    ]
    if not all(conditions):
        raise SystemExit("Value out of range")

    zodiac = {
        "Aquarius": any([
            month == 1 and day >= 20,
            month == 2 and day <= 18
        ]), # 20/1-18/2
        "Pisces": any([
            month == 2 and day >= 19,
            month == 3 and day <= 20
        ]), # 19/2-20/3
        "Aries": any([
            month == 3 and day >= 21,
            month == 4 and day <= 19
        ]), # 21/3-19/4
        "Taurus": any([
            month == 4 and day >= 20,
            month == 5 and day <= 20
        ]), # 20/4-20/5
        "Gemini": any([
            month == 5 and day >= 21,
            month == 6 and day <= 20
        ]), # 21/5-20/6
        "Cancer": any([
            month == 6 and day >= 21,
            month == 7 and day <= 22
        ]), # 21/6-22/7
        "Leo": any([
            month == 7 and day >= 23,
            month == 8 and day <= 22
        ]), # 23/7-22/8
        "Virgo": any([
            month == 8 and day >= 23,
            month == 9 and day <= 22
        ]), # 23/8-22/9
        "Libra": any([
            month == 9 and day >= 23,
            month == 10 and day <= 22
        ]), # 23/9-22/10
        "Scorpio": any([
            month == 10 and day >= 23,
            month == 11 and day <= 21
        ]), # 23/10-21/11
        "Sagittarius":any([
            month == 11 and day >= 22,
            month == 12 and day <= 21
        ]), # 22/11-21/12
        "Capricorn": any([
            month == 12 and day >= 22,
            month == 1 and day <= 19
        ]), # 22/12-19/1
    }
    
    if zodiac13: # 13 zodiac signs
        zodiac = {
            "Aquarius": any([
                month == 2 and day >= 17,
                month == 3 and day <= 11
            ]), # 17/2-11/3
            "Pisces": any([
                month == 3 and day >= 12,
                month == 4 and day <= 18
            ]), # 12/3-18-4
            "Aries": any([
                month == 4 and day >= 19,
                month == 5 and day <= 13
            ]), # 19/4-13-5
            "Taurus": any([
                month == 5 and day >= 14,
                month == 6 and day <= 21
            ]), # 14/5-21/6
            "Gemini": any([
                month == 6 and day >= 22,
                month == 7 and day <= 20
            ]), # 22/6-20/7
            "Cancer": any([
                month == 7 and day >= 21,
                month == 8 and day <= 10
            ]), # 21/7-10/8
            "Leo": any([
                month == 8 and day >= 11,
                month == 9 and day <= 16
            ]), # 11/8-16/9
            "Virgo": any([
                month == 9 and day >= 17,
                month == 10 and day <= 30
            ]), # 17/9-30/10
            "Libra": any([
                month == 10 and day >= 31,
                month == 11 and day <= 23
            ]), # 31/10-23/11
            "Scorpio": any([
                month == 11 and day >= 24,
                month == 11 and day <= 29
            ]), # 24/11-29/11
            "Ophiuchus": any([
                month == 11 and day >= 30,
                month == 12 and day <= 17
            ]), # 30/11-17/12
            "Sagittarius":any([
                month == 12 and day >= 18,
                month == 1 and day <= 20
            ]), # 18/12-20/1
            "Capricorn": any([
                month == 1 and day >= 21,
                month == 2 and day <= 16
            ]), # 21/1-16/2
        }

    logger.debug(zodiac)
    
    for k, v in zodiac.items():
        if v is True:
            return k

def im_bored() -> str:
    """Get random activity from `boredapi` website"""
    api = APIRequest("https://www.boredapi.com/api/activity")
    return api.fetch_data_only().json()["activity"]


def force_shutdown():
    """Force the computer to shutdown"""
    # Get operating system
    os_name = sys.platform

    # Shutdown
    shutdown = {
        # Windows
        "win32": "shutdown -f -s -t 0".split(),
        "cygwin": "shutdown -f -s -t 0".split(),
        # Mac OS
        "darwin": ["osascript", "-e", 'tell app "System Events" to shut down'],
        # Linux
        "linux": "shutdown -h now".split(),
    }

    if os_name in shutdown:
        return subprocess.run(shutdown[os_name])
    else:
        return subprocess.run(shutdown["linux"])


# For new year only
def happy_new_year(forced: bool = False):
    """Only occurs on 01/01 every year"""

    if forced:
        return force_shutdown()

    today = date.today()
    m = today.month
    d = today.day

    if m==1 and d==1:
        print("Happy New Year! You should take rest now.")
        return force_shutdown()
    else:
        raise SystemExit("The time has not come yet")


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
