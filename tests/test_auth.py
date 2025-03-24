def test_login_blueprint_registered(app):
    assert 'auth' in app.blueprints

def test_auth_routes(client):
    response = client.get('/login/')
    assert response.status_code == 200