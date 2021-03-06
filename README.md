# Meetings Registration Tool

Online registration system for managing meeting participants and for printing badges or reports.

## Installation
------------

* Install `Docker <https://docker.com>`_
* Install `Docker Compose <https://docs.docker.com/compose>`_

1. Clone the repo::

    git clone <https://github.com/eaudeweb/meetings-registration-tool.git>
    cd meetings-registration-tool

1. Create configuration files::

    cp settings.example settings.py
    cp docker/postgres.env.example docker/postgres.env
    cp docker/init.sql.example docker/init.sql
    cp docker/log.env.example docker/log.env
    cp docker/app.env.example docker/app.env

1. Edit all the above files

1. Create

1. Spin up the docker containers::

    docker-compose up -d
    docker-compose ps

## Upgrade

1. Upgrade repo::

    cd meetings-registration-tool
    git pull

1. Get the latest docker images and restart the docker containers::

    docker-compose pull
    docker-compose up -d
    docker-compose ps

## Logging

For production logging:

1. Update log.env with your Papertrail host and port destination values (<https://papertrailapp.com/account/destinations>):

    vim docker/log.env

For accurate _remote_addr_ values, please insert the correct header in VHOST file. See <https://stackoverflow.com/questions/45260132/docker-get-users-real-ip> for example.

1. Error logging is made with Sentry.io. Get client key from <https://sentry.io/[organisation]/[project]/settings/keys/> and set the value of SENTRY_DSN from settings.py file::

    SENTRY_DSN='<https://xxx@sentry.io/232313>'

Restart the application and run <http://app-url/crashme> to test the integration.

## Backup

To backup the application run the following commands:

    docker exec mrt.db pg_dump -Upostgres <db_name> -Cc | gzip  > db.sql.gz
    docker exec mrt.app tar cvf - /var/local/meetings/instance/files/ | gzip > files.gz

-Cc is equivalent to --create --clean.

    --create tells pg_dump to include tables, views, and functions in the backup, not just the data contained in the tables.
    --clean tells pg_dump to start the SQL script by dropping the data that is currently in the database. This makes it easier to restore in one step.

If you are using rsync.net or other incremental backup system, don't forget to add `--rsyncable` to gzip command.

## Data migration

1. Database

Copy the Postgres SQL dump file inside the postgres container, drop the current database and use psql to import the backup (you will find the POSTGRES_DBUSER and the POSTGRES_PASSWORD in the system environment variables)::

    $ docker cp backup.sql mrt.db:/tmp/backup.sql
    $ docker exec -it mrt.db bash
    /# dropdb cms_meetings;
    /# createdb cms_meetings;
    /# psql < /tmp/backup.sql

1. Files

Copy the _files_ directory to the _mrt.app_ container, under the _instance_ directory:

    $ sudo docker cp ./files mrt.app:/var/local/meetings/instance/
    $ sudo docker exec -ti mrt.app bash
    # chown root:root /var/local/meetings/instance/files
