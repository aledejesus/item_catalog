from flask import Flask

app = Flask('item_catalog')


@app.route('/test')
def test_route():
    return 'Working'
