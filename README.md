# gittyleaks

#### Discover where your sensitive data has been leaked.

<table>
<tr>
<td>
<img src="https://github.com/kootenpv/gittyleaks/raw/master/resources/gittyleaks.png" height="400px" width="600px"/>
</td>
<td>
Very often it happens that when mocking/just starting out with a new project on github, sensitive data gets added. API keys, usernames, passwords and emails are easily added.... and then forgotten. Use this tool to detect where the mistakes are in your repos.
</td>
</tr>
</table>

Usage examples:

```python
# gittyleaks -u username -r repo
gittyleaks -u kootenpv -r yagmail

# gittyleaks -l some-git-cloneable
gittyleaks https://github.com/kootenpv/yagmail
```

another example:

```python
gittyleaks -u smartczy -r weather_py
```

By default `gittyleaks` tries to be smart about might be compromising. If you really want to find anything, you can use the '--find-anything' option to find things less likely to be hardcoded.

#### Installation

Best way is to use pip to install:

```python
pip install gittyleaks    # for python 2
pip3 install gittyleaks   # for python 3
```

Upgrades can be done by giving the -U flag; `pip3 install -U gittyleaks`.

#### Roadmap

It is now already possible to subclass and overwrite certain methods. More docs on that to follow.

~~Deleting a cloned repo should also be added with perhaps adding the `-d` flag~~

~~Allow user to --find-anything rather than filtering~~

The package will soon provide the best practice to remedy this issue based on [https://help.github.com/articles/remove-sensitive-data/](https://help.github.com/articles/remove-sensitive-data/).

After that, quality improvements to the detection will be done.

