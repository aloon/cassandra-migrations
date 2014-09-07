#! /usr/bin/python

import sys, time, os, re

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from cassandra.cluster import Cluster

cluster = Cluster()

def help():
  print "help"
  
def generateMigration():
  name = sys.argv[2]
  file_name = time.strftime("%Y%m%d%H%M%S_") + convert(name) + ".xml"
  
  top = Element('migration')
  up = SubElement(top, 'up')
  up.text = '\nHere cql up\n  '
  down = SubElement(top, 'down')
  down.text = '\nHere cql down.\n  '
  
  rough_string = ElementTree.tostring(top, 'utf-8')
  reparsed = minidom.parseString(rough_string)
  xml = reparsed.toprettyxml(indent="  ")
  
  if not os.path.exists("migrations"):
    os.makedirs("migrations")
    
  target = open("migrations/" + file_name, 'a')
  target.write(xml)
  target.close()
  
  print "create    migrations/" + file_name
  
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
  
def migrate():
  keyspace = sys.argv[2]
  session = cluster.connect(keyspace)
  cql_create_schema = "CREATE TABLE IF NOT EXISTS schema_migrations (version varchar PRIMARY KEY);"
  session.execute(cql_create_schema)
  f = []
  for (dirpath, dirnames, filenames) in os.walk('migrations/'):
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
      xmldoc = minidom.parse('migrations/' + filename)
      up = xmldoc.getElementsByTagName('up')[0].firstChild.data
      down = xmldoc.getElementsByTagName('down')[0].firstChild.data
      #TODO: exception control
      session.execute(up)
      session.execute("insert into schema_migrations (version) values(%s)",[id_migration])
      print "executed: " + up
  
def current(keyspace):
  session = cluster.connect(keyspace)
  versions = []
  rows=session.execute("select version from schema_migrations")
  for c in rows:
    versions.append(c[0])
  versions = sorted(versions)
  print versions[-1]
  
if len(sys.argv) > 0:
  opt = sys.argv[1]
  if opt == "generateMigration":
    generateMigration()
  elif opt == "migrate":
    migrate()
  elif opt == "current":
    keyspace = sys.argv[2]
    current(keyspace)
  else:
    help()
else:
  help()
  