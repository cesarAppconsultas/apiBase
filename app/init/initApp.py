from app import app

@app.route('/')
def hello_api():
    return '<html><body><h1>API ACTIVA</h1></body></html>'