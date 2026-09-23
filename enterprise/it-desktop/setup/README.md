## SMB Share
The workstation exposes a SMB share folder.
The share is named:

    it
The share contains:

- `readme.txt`
  - Contains `flag{smbflag}`.
- `network.txt`
  - Contains internal infrastructure notes:
    - Database Server: `10.10.4.108`
    - Backup Server: `10.10.4.107`

The share can be recreated automatically using:

    powershell.exe -ExecutionPolicy Bypass -File create_smb_share.ps1
