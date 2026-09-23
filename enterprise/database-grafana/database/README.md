## MariaDB Database

The laboratory database is provided in:

    database/enterprise_db.sql

The laboratory uses the following database account:

    User: backup_reader
    Allowed host: %
    Password: backup2026

The dump contains the schema and data required to recreate the
`enterprise_db` database used by the training scenario.

Before importing the dump, create the database:

    mysql -u root -p -e "CREATE DATABASE enterprise_db;"
    
To restore the database:

    mysql -u root -p enterprise_db < mariadb/enterprise_db.sql

The database contains intentionally exposed internal infrastructure information and exercise flags used during the Enterprise reconnaissance stage.
