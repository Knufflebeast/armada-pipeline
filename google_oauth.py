

from google_auth_oauthlib.flow import InstalledAppFlow


flow = InstalledAppFlow.from_client_secrets_file(
    'W:/OneDrive/Knufflebeast/Technology/ArmadaPipeline/Google_API/client_secret.json',
    ['openid'])

cred = flow.run_local_server()

print(cred)