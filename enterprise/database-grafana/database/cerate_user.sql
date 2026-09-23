CREATE USER IF NOT EXISTS 'backup_reader'@'%' IDENTIFIED BY 'backup2026';

GRANT SELECT ON enterprise_backups.* TO 'backup_reader'@'%';
GRANT SELECT ON enterprise_db.* TO 'backup_reader'@'%';

FLUSH PRIVILEGES;
