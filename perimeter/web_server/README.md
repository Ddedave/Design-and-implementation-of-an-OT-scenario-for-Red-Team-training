# Vulnerable Web Server

This system represents the initial entry point of the Red Team exercise.

It is deployed in the Level 5 Internet-facing DMZ and exposes an intentionally vulnerable web application used during the initial-access stage of the scenario.

## System Information

- Operating system: Debian 13
- CPU: 2 vCPU
- Memory: 3 GB RAM
- Disk: 20 GB
- Web server: Apache2

## Network Configuration

- IP address: `10.10.5.110/24`
- Default gateway: `10.10.5.1`
- Network: Level 5 Internet-facing DMZ

## Role

The server exposes the vulnerable web application used as the initial compromise point of the exercise.

Firewall 1 forwards TCP port 80 from the attacker-facing network to this server.

## Web Application

The web application represents the public customer-support portal of **Refrescos Favoritos**.

Users can submit support requests and attach files through the web interface.

The form is implemented in `index.html` and sends submitted data to `support.php` using `multipart/form-data`.

## Files
### `index.html`

Main page of the fictitious customer portal.

It contains:

- General company information.
- A support form.
- Contact information fields.
- A file-upload field.
- A ticket description field.

The support form submits the request to `support.php` using `multipart/form-data`.

### `support.php`

Processes requests submitted by `index.html`.

Uploaded files are stored inside:

    uploads/

The uploaded file is saved using the filename provided by the user.

The application intentionally does not validate the uploaded file extension or file type before saving it.

The saved file is also assigned permissive filesystem permissions.

This behaviour is intentionally insecure and forms part of the initial-access stage of the Red Team training scenario.
After a successful upload, the application displays a direct link to the stored file.

### `create_flags.sh`

Creates the exercise flags associated with the Web Server stage.

The script creates the following flags:

| Location | Flag | Objective |
|---|---|---|
| `/var/www/html/portal/uploads/flag.txt` | `flag{initial_access_obtained}` | Confirm successful initial access |
| `/root/flag.txt` | `flag{root_gained}` | Confirm successful privilege escalation |

The initial-access flag is located in the web application's upload directory so that it can be discovered after obtaining remote access to the server.

The root flag is stored inside `/root` and should only be readable after successful privilege escalation.

Run the flag deployment script with:

    sudo chmod +x create_flags.sh
    sudo ./create_flags.sh

### `uploads/`Directory used by `support.php` to store files submitted through the customer support portal.

This directory is intentionally writable by the web application as part of the training scenario.

## Deployment

Install Apache and PHP:

    sudo apt update
    sudo apt install apache2 php libapache2-mod-php -y

Create the application directory:

    sudo mkdir -p /var/www/html/portal/uploads

Copy the application files into the web directory:

    sudo cp index.html /var/www/html/portal/
    sudo cp support.php /var/www/html/portal/

Configure ownership:

    sudo chown -R www-data:www-data /var/www/html/portal

Configure the upload directory:

    sudo chmod 777 /var/www/html/portal/uploads

Restart Apache:
   sudo systemctl restart apache2

The application should then be accessible through:

    http://10.10.5.110/portal/

## Exercise Flags

After deploying the web application, execute:

    sudo ./create_flags.sh

This creates:

    /var/www/html/portal/uploads/flag.txt
    /root/flag.txt

The expected exercise progression is:

    Web application access
            ↓
    File upload
            ↓
    Remote access
            ↓
    flag{initial_access_obtained}
            ↓
    Privilege escalation
            ↓
    flag{root_gained}## Intended Vulnerability

The support portal contains an intentionally insecure file-upload mechanism.

The application:

- Accepts user-controlled filenames.
- Does not validate file extensions.
- Does not validate MIME types.
- Stores uploaded files inside a web-accessible directory.
- Assigns permissive permissions to uploaded files.
- Returns a direct link to uploaded content.

These characteristics are intentionally included to support the initial-access exercise.

## Security Notice

This application is intentionally vulnerable.

It must only be deployed inside an isolated cybersecurity training environment.

It must not be exposed to production networks or directly connected to the public Internet.

The vulnerabilities and weak permissions documented in this repository are intentional components of the Red Team laboratory and do not represent secure deployment practices.
