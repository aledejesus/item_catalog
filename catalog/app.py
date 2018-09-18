from flask import Flask

app = Flask('item_catalog')


@app.route('/')
def test_route():
    return 'Working'
