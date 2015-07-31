## Biggest issue is the argument parser and the fact that it does change directory, 
# but only in _this_ scope, not in the outside world

import os
import random

try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

def next_sibling():
    cwd_name = os.getcwd().split('/')[-1]
    found = False 
    first = cwd_name
    for x in scandir('../'): 
        if x.is_dir():
            if first == cwd_name:
                first = x
            if found:
                break
            if x.name == cwd_name:
                found = True
    else: 
        return
    os.chdir(x.path)

def random_sibling(): 
    dirs = set()
    for x in scandir('../'): 
        if x.is_dir():
            dirs.add(x.path)
    if dirs:
        os.chdir(random.choice(dirs).path)

def first_child(p = '.'):
    for x in scandir(p): 
        if x.is_dir():
            os.chdir(x.path)
            return 

def last_child(p = '.'):
    child = None 
    for x in scandir(p): 
        if x.is_dir(): 
            child = x
    if child is not None: 
        os.chdir(child.path) 
        
def up(times = 1, p = '.'):
    if p is not None:
        if isinstance(p, str):
            os.chdir(p)
        else:
            os.chdir(p.path)    
    os.chdir('../' * int(times))

def random_walk(n = 5):
    for _ in range(n):
        fn = random.choice([up, last_child, first_child, next_sibling])
        print(os.getcwd())
        fn()
    
def main():
    """ This is the function that is run from commandline with `yagmail` """ 
    import argparse
    parser = argparse.ArgumentParser(description='Send a (g)mail with yagmail.') 
    parser.add_argument('-next', '-n', help='Send an email to address "TO"') 
    parser.add_argument('-previous', '-p', help='Subject of email') 
    parser.add_argument('-random', '-r', help='Contents to send') 
    parser.add_argument('-first', '-f', help='Username') 
    parser.add_argument('-up', '-u', help='Username') 
    parser.add_argument('-last', '-l', help='Preferable to use keyring rather than password here') 
    args = parser.parse_args() 
    mapping = {'n' : next_sibling,
               'p' : next_sibling, 
               'r' : random_walk,
               'f' : first_child,
               'l' : last_child,
               'up' : up}
    for k in mapping:
        v = getattr(args, k, None)
        if v is not None:
            mapping[k](v) 
