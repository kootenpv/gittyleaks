# gittyleaks

#### Discover where your sensitive data has been leaked.

<table>
<tr>
<td>
<img src="https://github.com/kootenpv/gittyleaks/raw/master/resources/gittyleaks.png" height="400px" width="400px"/>
</td>
<td>
Very often it happens that when mocking/just starting out with a new project on github, sensitive data gets added. api keys, usernames, passwords and emails are easily added.... and then forgotten. Use this tool to detect where the mistakes are in your repos.
</td>
</tr>
</table>

Run like:

```python
# gittyleaks -u username -r repo
gittyleaks -u kootenpv -r yagmail
```

working example:

```bash
gittyleaks -u smartczy -r weather_py
```

It is now already possible to subclass and overwrite certain methods. More docs on that to follow.

#### Roadmap

The package will soon provide the best practice to remedy this issue based on [https://help.github.com/articles/remove-sensitive-data/](https://help.github.com/articles/remove-sensitive-data/).

Furthermore, positional arguments should also be possible.

Deleting a cloned repo should also be added with perhaps adding the `-d` flag

After that, quality improvements to the detection will be done.
