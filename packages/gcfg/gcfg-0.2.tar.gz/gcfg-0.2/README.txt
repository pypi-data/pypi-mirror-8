ConfigParser to Module
==========================
UsageExample
files(_config.ini) content
```
[db]
dbtype = mysql
```

files(_config.default.ini) content
```
[db]
dbtype = sqlite
user = guest
```

sample code
```
import gcfg
gcfg.DEFAULTFILES = ['_config.ini', '_config.default.ini']
print gcfg.db.dbtype # expect mysql
print gcfg.db.user   # expect guest
```
