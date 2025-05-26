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
#Operating system functions, talks and checks in with our os to verify things such as 
import re # for matching 
import sys
import zlib #compressing 

argparser = argparse.ArgumentParser(description="The stupidest content tracker")
#Sub parsers cmds like init and commit
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True
#Read the string and be able to call the correct function(bridge functions)
#Responsable for processing and validating before executing the cmd
def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")