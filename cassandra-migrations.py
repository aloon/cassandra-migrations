#!/usr/bin/env python

import sys, time, os, re

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from cassandra.cluster import Cluster

server = ""
if len(sys.argv) > 3:
    server = sys.argv[3]
if server == "":
    server = '127.0.0.1'

cluster = Cluster([server])

def help():
  print """
  Usage:
  
  Create new migration file
     ./cassandra-migrations.py generate {keyspace} {description}
  
  Apply migrations to a keyspace:
     ./cassandra-migrations.py migrate {keyspace}
  or for a remote server
     ./cassandra-migrations.py migrate {keyspace} {serverIP}
     
  Rollback a migration:
     ./cassandra-migrations.py rollback {keyspace}
  
  """
  
def generateMigration():
  name = sys.argv[3]
  keyspace = sys.argv[2]
  file_name = time.strftime("%Y%m%d%H%M%S_") + convert(name) + ".xml"
  
  defaultText = """<?xml version="1.0" ?>
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
"""
  
  if not os.path.exists("migrations"):
    os.makedirs("migrations/")

  if not os.path.exists("migrations/" + keyspace):
    os.makedirs("migrations/" + keyspace)
    
  target = open("migrations/" + keyspace + "/" + file_name, 'a')
  target.write(defaultText)
  target.close()
  
  print "created migrations/" + keyspace + "/" + file_name
  
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
  
def migrate():
  keyspace = sys.argv[2]
  session = cluster.connect(keyspace)
  cql_create_schema = "CREATE TABLE IF NOT EXISTS schema_migrations (version varchar PRIMARY KEY);"
  session.execute(cql_create_schema)
  f = []
  for (dirpath, dirnames, filenames) in os.walk('migrations/' + keyspace + '/'):
    f.extend(filenames)
    break
  f = sorted(f)
  for filename in f:
    id_migration = filename.split('_')[0]
    rows = session.execute("SELECT COUNT(*) AS C FROM schema_migrations where version=%s",[id_migration])
    count = 0
    for c in rows:
      count = c[0]
    if count == 0:
      xmldoc = minidom.parse('migrations/' + keyspace + '/' + filename)
      up = xmldoc.getElementsByTagName('up')[0]
      cqls = up.getElementsByTagName('cql')
      applied = False
      for x in cqls:
          cql = x.firstChild.data
          try:
              session.execute(cql)
              print "Executed (" + keyspace + '/' + filename + "): "+ cql
          except Exception:
              applied = True
              print("WARNING: CQL already applied %s" % cql)
      if applied is True:
          print("NOTICE: Migration file " + keyspace + "/%s already applied" % filename)
      session.execute("insert into schema_migrations (version) values(%s)",[id_migration])
  print ("\nMigration complete.\n")
  
def current(keyspace):
  session = cluster.connect(keyspace)
  versions = []
  rows=session.execute("select version from schema_migrations")
  for c in rows:
    versions.append(c[0])
  versions = sorted(versions)
  #TODO: control first version
  return versions[-1]

def rollback():
  keyspace = sys.argv[2]
  session = cluster.connect(keyspace)
  ff = []
  for (dirpath, dirnames, filenames) in os.walk('migrations/' + keyspace + '/'):
    ff.extend(filenames)
    break
  filename=''
  id_migration=current(keyspace)
  for f in ff:
    if f.find(id_migration)>-1:
      filename=f
  xmldoc = minidom.parse('migrations/' + keyspace + '/' + filename)
  down = xmldoc.getElementsByTagName('down')[0]
  cqls = down.getElementsByTagName('cql')
  applied = False
  for x in cqls:
      cql = x.firstChild.data
      try:
          session.execute(cql)
          print "Executed ("+ keyspace + '/' +filename +"): "+ cql
      except Exception:
          applied = True
  #session.execute(down)
  session.execute("delete from schema_migrations where version=%s",[id_migration])
  #TODO: control first version
  
if len(sys.argv) > 2:
  opt = sys.argv[1]
  if opt == "generate":
    generateMigration()
  elif opt == "migrate":
    migrate()
  elif opt == "current":
    keyspace = sys.argv[2]
    print current(keyspace)
  elif opt == "rollback":
    rollback()
  else:
    help()
else:
  help()
