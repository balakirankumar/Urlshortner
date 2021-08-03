from urlshort import create_app

def test_shorten(client):
    responce=client.get('/')
    assert b'Shorten' in  responce.data
