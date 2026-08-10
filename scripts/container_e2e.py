import os, random, string, pathlib, time, traceback
os.environ['BACKEND_URL'] = os.environ.get('BACKEND_URL', 'http://127.0.0.1:8000')
from frontend import api_client as api
from backend.app.db.session import SessionLocal
from backend.app.services.alert_service import create_alert

suffix = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
user = {'username': f'e2euser2_{suffix}', 'email': f'e2euser2_{suffix}@example.com', 'password': 'Pass12345'}
print('Using BACKEND_URL=', os.environ['BACKEND_URL'])

results = {'register': False,'login': False,'usage_before': None,'upload': False,'usage_after': None,'history': False,'alert_created': False,'alerts_listed': False}

try:
    r = api.register(user['username'], user['email'], user['password'])
    results['register'] = True
    print('registered')
    l = api.login(user['username'], user['password'])
    token = l['access_token']
    results['login'] = True
    print('logged in')
    usage_before = api.get_usage(token)
    results['usage_before'] = usage_before
    print('usage before', usage_before)
    img_path = pathlib.Path(__file__).parents[1] / 'img' / 'doc.jpeg'
    b = img_path.read_bytes()
    up = api.upload_prescription(token, 'doc.jpeg', b, 'image/jpeg')
    results['upload'] = True
    prescription_id = up.get('id')
    print('uploaded id', prescription_id)
    time.sleep(1)
    usage_after = api.get_usage(token)
    results['usage_after'] = usage_after
    print('usage after', usage_after)
    # history
    pres = api.get_prescriptions(token)
    results['history'] = any(p.get('id')==prescription_id for p in pres)
    print('history contains uploaded:', results['history'])
    # create alert via DB directly (attach to the created user)
    with SessionLocal() as db:
        from backend.app.db.models.user import User
        u = db.query(User).filter(User.username == user['username']).first()
        if u:
            alert = create_alert(db, user_id=u.id, prescription_id=prescription_id, subject='E2E alert', message='test', to_email=None)
            results['alert_created'] = bool(alert and alert.id)
            print('alert created id', alert.id)
        else:
            print('Could not find user in DB to attach alert')
    # fetch alerts via API
    alerts = api.get_alerts(token)
    results['alerts_listed'] = any(a.get('prescription_id')==prescription_id for a in alerts)
    print('alerts listed and contain alert:', results['alerts_listed'])
except Exception as e:
    traceback.print_exc()
    print('Error during E2E', e)

print('RESULTS', results)
