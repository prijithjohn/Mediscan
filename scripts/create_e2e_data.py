import os, random, string, pathlib, time
# ensure backend URL points at compose backend
os.environ['BACKEND_URL'] = os.environ.get('BACKEND_URL', 'http://127.0.0.1:8000')
from frontend import api_client as api

suffix = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
user = {'username': f'e2euser_{suffix}', 'email': f'e2euser_{suffix}@example.com', 'password': 'Pass12345'}
print('Using BACKEND_URL=', os.environ['BACKEND_URL'])

print('Registering user')
reg = api.register(user['username'], user['email'], user['password'])
print('Register response:', {k: v for k, v in reg.items() if k!='password'})

print('Logging in')
login = api.login(user['username'], user['password'])
token = login['access_token']
print('Got token length', len(token))

# get usage before
usage_before = api.get_usage(token)
print('usage before', usage_before)

# upload image
img_path = pathlib.Path(__file__).parents[1] / 'img' / 'doc.jpeg'
if not img_path.exists():
    print('Image not found at', img_path)
else:
    b = img_path.read_bytes()
    print('Uploading image, size', len(b))
    up = api.upload_prescription(token, 'doc.jpeg', b, 'image/jpeg')
    print('Upload response keys:', list(up.keys()))
    print('Upload id:', up.get('id'))

print('Sleeping 1s to allow DB commit')
time.sleep(1)
print('Done')
