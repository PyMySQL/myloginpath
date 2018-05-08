# MySQL's login path file reader

Decrypt and parse MySQL's login path file.

See also: https://dev.mysql.com/doc/refman/8.0/en/mysql-config-editor.html


## Install

```
$ pip install myloginpath
```

## Example

Create login path file with `mysql_config_editor` command:

```console
$ mysql_config_editor set --login-path=client --host=localhost --user=localuser --password
Enter password: <Type password here>
```

Use it from Python:

```python
import myloginpath, MySQLdb
conf = myloginpath.parse('client')
print(conf)  # {'host': 'localhost', 'user': 'localuser', 'password': 'secretstring'}
conn = MySQLdb.connect(**conf, db="myapp")
```
