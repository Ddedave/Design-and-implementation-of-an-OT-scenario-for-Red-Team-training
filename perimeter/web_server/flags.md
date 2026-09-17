## Exercise Flags

Two local flags are deployed on the vulnerable web server:

| Location | Flag | Objective |
|---|---|---|
| `/var/www/html/portal/uploads/flag.txt` | `flag{initial_access_obtained}` | Confirm initial remote access |
| `/root/flag.txt` | `flag{root_gained}` | Confirm successful privilege escalation |

The flags can be created automatically using:

```bash
sudo ./setup/create_flags.sh
