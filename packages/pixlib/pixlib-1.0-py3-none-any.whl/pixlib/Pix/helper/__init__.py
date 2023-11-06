import os
import sys
from pyrogram import Client

from pixlib.Pix.helper.adminHelpers import *
from pixlib.Pix.helper.aiohttp_helper import*
from pixlib.Pix.helper.basic import *
from pixlib.Pix.helper.constants import *
from pixlib.Pix.helper.data import *
from pixlib.Pix.helper.inline import *
from pixlib.Pix.helper.interval import *
from pixlib.Pix.helper.parser import *
from pixlib.Pix.helper.PyroHelpers import *
from pixlib.Pix.helper.utility import *
from pixlib.Pix.helper.what import *
from pixlib.Pix.helper.pluginhelper import *

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Pix"])

