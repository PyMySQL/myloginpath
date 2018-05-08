# MySQL's login path file reader

Decrypt and parse MySQL's login path file.

See also: https://dev.mysql.com/doc/refman/8.0/en/mysql-config-editor.html


## Install

```
$ pip install myloginpath
```

## Example

```console
$ mysql_config_editor set --login-path=client --host=localhost --user=localuser --password
Enter password: <Type password here>
```

```python
import myloginpath, MySQLdb
conf = myloginpath.parse('client')
print(conf)  # {'host': 'localhost', 'user': 'localuser', 'password': 'secretstring'}
conn = MySQLdb.connect(**conf, db="myapp")
```
