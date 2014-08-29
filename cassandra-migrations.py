#! /usr/bin/python

import sys, time, os, re

from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from subprocess import call
from subprocess import Popen, PIPE
from tempfile import SpooledTemporaryFile as tempfile

cqlsh = '/usr/bin/cqlsh'

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
  
def exists_schema():
  return false
  
def migrate():
  keyspace = sys.argv[2]
  cql_create_schema = "CREATE TABLE IF NOT EXISTS " + keyspace + ".schema_migrations (version varchar PRIMARY KEY);"
  print cql_create_schema
  # insert into mio.schema_migrations (version) values('456456');
  f = tempfile()
  f.write(cql_create_schema)
  f.seek(0)
  print Popen([cqlsh],stdout=PIPE,stdin=f).stdout.read()
  f.close()
  
if len(sys.argv) > 0:
  opt = sys.argv[1]
  if opt == "generateMigration":
    generateMigration()
  elif opt == "migrate":
    migrate()
  else:
    help()
else:
  help()
  