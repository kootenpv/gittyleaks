# gittyleaks

#### Discover where your sensitive data has been leaked.

<table>
<tr>
<td>
<img src="https://github.com/kootenpv/gittyleaks/raw/master/resources/gittyleaks.png" height="400px" width="600px"/>
</td>
<td>

<p>Very often it happens that when mocking/just starting out with a new project on github, sensitive data gets added. API keys, usernames, passwords and emails are easily added.... and then forgotten.</p>

<p>Use this tool to detect where the mistakes are in your repos. </p>

<p>It works by trying to find words like 'username', 'password', and 'email' and shortenings in quoted strings, config style or JSON format. It captures the value assigned to it (after meeting some conditions) for further work.</p>

</td>
</tr>
</table>

### Installation

Best way is to use pip to install:

```python
pip install gittyleaks    # for python 2
pip3 install gittyleaks   # for python 3
```

Now you have `gittyleaks` as a python executable available on your system.

Upgrades can be done by giving the -U flag; `pip3 install -U gittyleaks`.

### Command line usage 
Generally, the program can be called by `gittyleaks`. There will be 4 types of arguments.
- Arguments for solving a bad situation (not there yet)
- Arguments for changing whether there is a hit
- Arguments for cloning a repo
- Arguments concerned with printing results

Note that all arguments mentioned below have a short one letter + dash (e.g. `-delete` -> `-d`) version.

Find out more by using `gittyleaks -h` at commandline, or read on.

#### Solving bad situations

There has yet to be found a way how to help the user do something about it. This guide can help in the mean time:
[https://help.github.com/articles/remove-sensitive-data/](https://help.github.com/articles/remove-sensitive-data/)

#### Hits
By default `gittyleaks` tries to be smart about what might be compromising.

If you really want to find anything remotely suspicious:

```gittyleaks --find-anything```

If you want to exclude some string matches (e.g. if a `$` occurs in a value), use:

```gittyleaks --excluding $ . [ example ,```

Case sensitive:

```gittyleaks --case-sensitive```

#### Cloning

```bash
# gittyleaks -l some-git-cloneable-link
gittyleaks -link https://github.com/kootenpv/yagmail

# gittyleaks -user githubusername -repo githubusername
gittyleaks -user kootenpv -repo yagmail

# Giving the -d option deletes the repo afterwards immediately
gittyleaks -user smartczy -repo weather_py -delete
```

### Printing results

``` bash
gittyleaks --verbose              # longer output
gittyleaks --no-banner (-b)       # do not print banner 
gittyleaks --no-fancy-color (-f)  # turn off colors 
```

### Roadmap

~~Deleting a cloned repo should also be added with perhaps adding the `-d` flag~~

~~Allow user to `--find-anything` rather than filtering~~

~~Allow subclassing and overwriting certain methods.~~ Docs on that to follow.

The package will soon provide the best practice to remedy this issue based on [https://help.github.com/articles/remove-sensitive-data/](https://help.github.com/articles/remove-sensitive-data/).

Quality improvements to the detection.

Tests, tests, tests
