import json


with open('data/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

#Telegram
TOKEN: str = data['TELEGRAM']['token']

#Ngrok
NGROK: str  = data['NGROK']['address']
WEBHOOK_URL: str = f'{NGROK}/{TOKEN}'
PORT_NGROK: int = data['NGROK']['port']

#Scheduler
HOUR: int = data['SCHEDULER']['hour']
MINUTE: int = data['SCHEDULER']['minute']

# Telegram admins ID
ADMINS: list = data['TELEGRAM']['admins']

# SSH
IP_SERVERS: str = data['SSH']['ip']
PORTS_SSH: int = data['SSH']['port']
USERS: str = data['SSH']['username']
PASSWORDS: str = data['SSH']['password']

# Paths
PATHS_TO_SOURCE: str = data['SSH']['path_to_source']
PATHS_TO_DESTINATION: str = data['SSH']['path_to_destination']

# OS version
OPERATING_SYSTEM: list[str] = []
for path in PATHS_TO_SOURCE:
    if '\\' in path:
        OPERATING_SYSTEM.append('Windows')
    else:
        OPERATING_SYSTEM.append('Linux')

# Extension for fils
FILE_EXTENSION: str = '.zip'

# Merge archive name and extension
ARCHIVE_NAMES: str = [name + FILE_EXTENSION for name in data['SSH']['archive_name']]

# Make paths to archive
PATH_TO_ARCHIVE: list[str] = []
paths = zip(PATHS_TO_SOURCE, ARCHIVE_NAMES, OPERATING_SYSTEM)
for path in paths:
    if path[2] == 'Windows':
        index = path[0].rfind('\\') + 1
        path_to_archive = path[0][:index] + path[1]
        PATH_TO_ARCHIVE.append(path_to_archive)
    else:
        index = path[0].rfind('/') + 1
        path_to_archive = path[0][:index] + path[1]
        PATH_TO_ARCHIVE.append(path_to_archive)
