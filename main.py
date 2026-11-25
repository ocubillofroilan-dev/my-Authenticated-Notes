import os

from website import create_app

app = create_app()

if __name__ == '__main__':
    # Debug mode is handy while developing, but never run it on a public server.
    # To turn it off:  set FLASK_DEBUG=0  (Windows)  /  export FLASK_DEBUG=0  (Mac/Linux)
    app.run(debug=os.environ.get('FLASK_DEBUG', '1') == '1')