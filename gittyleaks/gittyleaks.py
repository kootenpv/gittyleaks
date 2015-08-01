# Run like: gittyleaks username reponame
# e.g. gittyleaks kootenpv yagmail
# working example: gittyleaks smartczy weather_py

import re
from sh import git
from sh import rm
import sh
import os
import argparse

def get_immediate_subdirectories():
    return set([fname for fname in os.listdir('.') if os.path.isdir(fname)])

class GittyLeak():
    def __init__(self, kwargs): 
        self.keywords = ['api', 'key', 'user', 'username', 'pw', 'pass', 'password', 'mail', 'email']

        self.revision_file_regex = '([a-z0-9]{40}):([^:]+):'

        assignment = "(\\b|[ ._-])({})[ '\"]*(=|:)[ '\"]*([^'\" ]+)"
        self.assignment_pattern = assignment.format('|'.join(self.keywords))

        excluded_value_chars = ['.', '[', 'none', 'true', 'false', 'null', 'default', 'example', 
                                'username', 'email', 'password']    

        self.min_value_length = 4
        
        self.excluded_value_chars = [x.lower() for x in excluded_value_chars]

        self.excluding = None
        self.revision_list = []
        self.user = None
        self.repo = None
        self.link = None
        self.find_anything = None 
        self.case_insensitive = True
        self.show_revision_names = False
        self.print_banner = True
        self.delete = None
        
        for k,v in kwargs.items():
            setattr(self, k, v)

        if self.find_anything:     
            self.excluded_value_chars = []
            self.case_insensitive = False
            
        if self.excluding is not None:
            self.excluded_value_chars.extend(self.excluding)
        
        
    def clone(self): 
        if self.link is not None:
            try:
                pre = get_immediate_subdirectories()
                git('clone', self.link) 
                post = get_immediate_subdirectories()
                self.repo = (post - pre).pop()
            except sh.ErrorReturnCode_128:
                pass 

        elif self.user is not None: 
            try:
                git('clone', 'https://github.com/{}/{}.git'.format(self.user, self.repo))

            except sh.ErrorReturnCode_128:
                pass

        os.chdir(self.repo) 

    def get_revision_list(self):
        self.revision_list = git('rev-list', '--all').strip().split('\n')                

    def get_git_matches(self, revision):
        try: 
            return str(git('grep', '-i', '-e', '"({})"'.format(r'\|'.join(self.keywords)), revision, _tty_out=False))
        except sh.ErrorReturnCode_1:
            return ''    

    def get_word_matches(self):
        # git grep simple word matches (python processing follows)
        word_matches = set()    
        for revision in self.revision_list: 
            for m in self.get_git_matches(revision).split('\n'): 
                word_matches.add(m)
        return word_matches        

    def validated_value(self, v):
        if v.strip():
            if len(v) < self.min_value_length:
                return False
            if self.excluded_value_chars:
                if self.case_insensitive:
                    v = v.lower()
                if not any([x in v for x in self.excluded_value_chars]):
                    return True
            else:
                return True    
        return False 
    
    def get_matches_dict(self):
        matches = {}
        for match in self.get_word_matches():
            if self.case_insensitive:
                m = re.search(self.assignment_pattern, match, re.IGNORECASE)
            else:
                m = re.search(self.assignment_pattern, match)    
            if m: 
                rev, fname = (re.search(self.revision_file_regex, match).groups()) 
                key, _, value = m.groups()[1:]
                if self.validated_value(value):
                    appearance = ':'.join(match.split(':')[2:]).strip()
                    identifier = (fname, key, value)
                    if identifier not in matches:
                        matches[identifier] = [] 
                    matches[identifier].append((appearance, rev))
        return matches

    def print_matches(self, matches):
        if self.print_banner:
            print("""
            ----------------------------------------------------------------------------------------------
            Bot Detective at work ...
            ----------------------------------------------------------------------------------------------
            """)
        if matches:
            print('----------------------------------------') 
        else:
            print('No matches.')    
        for k,v in matches.items():
            print('file: {}\nwhat: {}\nvalue: {}\nmatch:'.format(*k))
            for appear in set([x[0] for x in v]):
                print('    {}'.format(appear))
            if self.show_revision_names: 
                print('-----Revisions--------------------------') 
                for x in v: 
                    print(x[1])
            else:
                print('num_of_revisions: {}'.format(len(set([x[1] for x in v]))))        
            print('----------------------------------------')

    def run(self):
        if (self.user and self.repo) or self.link:
            self.clone()

        self.get_revision_list()

        matched_items = self.get_matches_dict() 
        
        self.print_matches(matched_items)

        if self.delete and (self.user and self.repo) or self.link:
            rm('-rf', '../' + self.repo)

            
def get_args_parser():
    parser = argparse.ArgumentParser(description='Discover where your sensitive data has been leaked.') 
    parser.add_argument('-user', '-u', help='Provide the user/owner of the repo, only if cloning from github') 
    parser.add_argument('-repo', '-r', help='Provide the name of the repo, only if cloning from github') 
    parser.add_argument('-link', '-l', help='Default is to load from github, provide the full url (link) to clone that instead') 
    parser.add_argument('-delete', '-d', action='store_true',
                        help = 'If cloned, remove the repo afterwards')
    parser.add_argument('--find-anything', '-a', action='store_true',
                        help='If you really want to find anything remotely suspicious, set this flag')
    parser.add_argument('--excluding', '-e', nargs = '+',
                        help='List of words that are ignored when they occur as value. E.g. you might want to exclude $ signs whenever they occur in the value')
    return parser
            
def main():
    """ This is the function that is run from commandline with `gittyleaks` """ 
    args = get_args_parser().parse_args() 
    gl = GittyLeak(args.__dict__)    
    gl.run() 
