from app import create_app

def test_health():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        r = client.get('/health')
        assert r.status_code == 200
        assert r.json['status'] == 'healthy'
