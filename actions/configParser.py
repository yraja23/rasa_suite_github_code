import configparser
from configparser_crypt import ConfigParserCrypt
from cryptography.fernet import Fernet
from io import StringIO

# Create an instance of ConfigParserCrypt
config_crypt = ConfigParserCrypt()

# Generate a secret key for encryption and decryption
secret_key = Fernet.generate_key()

# Create a sample configuration
config = configparser.ConfigParser()
config['client_details'] = {
    'client_id': 'FTS_CLIENT_APPID',
    'client_secret_key': '6057adc8-7d62-4495-a11c-bb29eb09f4b6',
    'scope': 'rgbu:merch:MFCS-STG1',
    'access_token_url': 'https://idcs-7e6742312d274583aa0f703733016616.identity.oraclecloud.com/oauth2/v1/token'
}
# Create a Fernet cipher using the secret key
cipher = Fernet(secret_key)

# Convert the configuration to a string
config_io = StringIO()
config.write(config_io)
config_string = config_io.getvalue()

# Encrypt the configuration string
encrypted_config = cipher.encrypt(config_string.encode()).decode()

# Save the encrypted configuration to a file
with open('secret.key', 'wb') as key_file:
    key_file.write(secret_key)

with open('encrypted_client_details.ini', 'w') as encrypted_file:
    encrypted_file.write(encrypted_config)
