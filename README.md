cassandra-migrations.py generateMigration AddPartNumberToProducts

create    migrations/20140829171538_add_part_number_to_products.xml

....................................................................

cassandra-migrations.py migrate my_keyspace

schema_migrations create
CREATE TABLE IF NOT EXISTS mio.schema_migrations (version varchar PRIMARY KEY);

CREATE TABLE "schema_migrations" ("version" varchar(255) NOT NULL);
CREATE UNIQUE INDEX "unique_schema_migrations" ON "schema_migrations" ("version");


== 20140829171538 AddPartNumberToProducts: migrating ==========================
-- create_table(:products)
   -> 0.0009s
== 20140829171538 AddPartNumberToProducts: migrated (0.0010s) =================