import json


with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


TOKEN: str = data['TELEGRAM']['token']
NGROK: str  = data['NGROK']['address']
WEBHOOK_URL: str = f'{NGROK}/{TOKEN}'
PORT_NGROK: int = data['NGROK']['port']
HOUR: int = data['SCHEDULER']['hour']
MINUTE: int = data['SCHEDULER']['minute']
ADMINS: list = data['TELEGRAM']['admins']
IP_SERVERS: str = data['SSH']['ip']
PORTS_SSH: int = data['SSH']['port']
USERS: str = data['SSH']['username']
PASSWORDS: str = data['SSH']['password']
PATHS_TO_SOURCE: str = data['SSH']['path_to_source']
PATHS_TO_DESTINATION: str = data['SSH']['path_to_destination']
ARCHIVE_NAMES: str = data['SSH']['archive_name']
