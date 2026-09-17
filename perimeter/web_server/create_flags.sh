#!/bin/bash

set -e

# Flag 1: initial access
mkdir -p /var/www/html/portal/uploads
echo 'flag{initial_access_obtained}' > /var/www/html/portal/uploads/flag.txt

# Flag 2: privilege escalation
echo 'flag{root_gained}' > /root/flag.txt

# Permissions
chown www-data:www-data /var/www/html/portal/uploads/flag.txt
chmod 644 /var/www/html/portal/uploads/flag.txt

chown root:root /root/flag.txt
chmod 600 /root/flag.txt
