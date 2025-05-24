#importing helpful python modeules
import argparse #parsing library for cmd
import configparser
from datetime import datetime #data and time manipulation
import grp, pwd #grp for groups and pwd for users 
from fnmatch import fnmatch # filename patterns 
import hashlib
from math import ceil
#Unlike a Unix shell, Python does not do any automatic path expansions.
import os
import re # for matching 
import sys
import zlib #compressing 