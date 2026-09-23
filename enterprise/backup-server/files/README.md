## Backup Files

This directory contains the files that must be placed in the publicly accessible SMB share of the Backup Server.

During deployment, these files should be copied to:

    /srv/backups

and exposed through the SMB share:

    \\10.10.4.107\backups

The files intentionally contain migration notes, maintenance information and laboratory credentials required for the progression of the training scenario.
