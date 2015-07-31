# Run like: gittyleaks username reponame
# e.g. gittyleaks kootenpv yagmail
# working example: gittyleaks smartczy weather_py

import re
from sh import git
import sh
import os

class GittyLeak():
    def __init__(self, kwargs): 
        self.keywords = ['api', 'key', 'user', 'username', 'pw', 'pass', 'password', 'mail', 'email']

        self.revision_file_regex = '([a-z0-9]{40}):([^:]+):'

        assignment = "(\\b|[ ._-])({})[ '\"]*(=|:)[ '\"]*([^'\" ]+)"
        self.assignment_pattern = assignment.format('|'.join(self.keywords))

        excluded_value_chars = ['.', '[', 'none', 'true', 'false', 'null', 'default', 'example']    
        self.excluded_value_chars = [x.lower() for x in excluded_value_chars]

        self.revision_list = []
        self.user = None
        self.repo = None
        self.url = None
        self.strict = None 
        self.case_insensitive = True
        self.show_revision_names = False
        self.print_banner = True
        
        for k,v in kwargs.items():
            setattr(self, k, v)
        
    def clone(self): 
        if self.repo is None and (self.user or self.url):
            raise ValueError('Provide username or url')

        if self.url is not None:
            try:
                git('clone', self.url)
            except sh.ErrorReturnCode_128:
                pass 

        elif self.user is not None: 
            try:
                git('clone', 'https://github.com/{}/{}.git'.format(self.user, self.repo))
            except sh.ErrorReturnCode_128:
                pass 

        if self.repo is not None:    
            os.chdir(self.repo) 

    def get_revision_list(self):
        self.revision_list = git('rev-list', '--all').strip().split('\n')
            
    def run(self):
        self.clone()

        self.get_revision_list()

        if self.strict:     
            self.excluded_value_chars = []
            self.case_insensitive = False
            
        matched_items = self.get_matches_dict() 
        
        self.print_matches(matched_items)
    

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

def main():
    """ This is the function that is run from commandline with `gittyleaks` """ 
    import argparse
    parser = argparse.ArgumentParser(description='Discover where your sensitive data has been leaked.') 
    parser.add_argument('-user', '-u', help='Provide the user/owner of the repo, only if cloning from github') 
    parser.add_argument('-repo', '-r', help='Provide the name of the repo, only if cloning from github') 
    parser.add_argument('-host', '-h', help='If host is not github, provide the full url to clone') 
    args = parser.parse_args() 
    gl = GittyLeak(args.__dict__)    
    gl.run() 
