import base64
import paramiko
#key = paramiko.RSAKey(data=base64.b64decode(b''))
client = paramiko.SSHClient()
#client.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('165.124.33.144', username='waue', password='crypto0920')
stdin, stdout, stderr = client.exec_command('ls -al / ')
for line in stdout:
    print('... ' + line.strip('\n'))
client.close()
