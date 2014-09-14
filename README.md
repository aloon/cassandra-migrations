# Schema migration for Cassandra

Simple python script for generate, execute and rollback [schema migrations](http://en.wikipedia.org/wiki/Schema_migration) in Cassandra.

## Intallation

Download the script, give execution permission and install the python dependencies

```
$ chmod +x cassandra-migrations.py
$ pip install cassandra-driver
$ pip install blist
```

## Usage

### Create migration

```
./cassandra-migrations.py generateMigration DescriptionMigrationName
```
This create the file like: ./migrations/20140914222010_decription_migration_name.xml
```xml
<?xml version="1.0" ?>
<migration>
  <up>
CQL migration command
  </up>
  <down>
CQL rollback
  </down>
</migration>
```
### Execute migration
```
$ ./cassandra-migrations.py migrate keyspace
```
### rollback migration
```
$ ./cassandra-migrations.py rollback keyspace
```




