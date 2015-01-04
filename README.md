# Schema migration for Cassandra

Simple python script for generate, execute and rollback [schema migrations](http://en.wikipedia.org/wiki/Schema_migration) in Cassandra.

## Installation

Download the script, give execution permission and install the python dependencies

```
$ chmod +x cassandra-migrations.py
$ pip install cassandra-driver
$ pip install blist
```

## Usage

### Create migration

```
./cassandra-migrations.py generate {keyspace} {MigrationName}
```
This creates a new file like: ./migrations/{keyspace}/20140914222010_{MigrationName}.xml
```xml
<?xml version="1.0" ?>
<migration>
    <up>
	    <cql><![CDATA[
Here cql up
	    ]]></cql>
	</up>
	<down>
  	    <cql><![CDATA[
Here cql down
		]]></cql>
	</down>
</migration>
```
### Execute migration
```
$ ./cassandra-migrations.py migrate {keyspace}
```
or 
```
$ ./cassandra-migrations.py migrate {keyspace} {serverIP}
```
### rollback migration
```
$ ./cassandra-migrations.py rollback {keyspace}
```

## Change Log

**2015-01-02**
- Enables multiple CQL up/down executions in the same migration
- Ability to have migrations for multiple keyspaces with single installation
- Updated default migration XML template
- Added support for remote server migrations
- Better notifications and warnings/errors when running
- Help documentation
