# Server-Backup-Script

Python tool to automate server backup from a network-mapped server drive (requiring admin credentials) to a mapped Google shared drive. My workplace was requiring me to either RDP into the VM server to perform the operation, or use File Explorer (//) to manually process the backup copy. 

## Features

- Easily runs through Task Scheduler as a weekly BU
- Automates authentication to the server with simple prompt
- Robust robocopy includes resume functionality and options for multiple re-tries
- Deletes previous versions based on name (where name includes date)

## Version History
6-10-25: Initial version
- Future builds: Include ability to monitor robocopy progress. Query DB for hashed credentials to avoid any interfacing (when used with Task Scheduler). 