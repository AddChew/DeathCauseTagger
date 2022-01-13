from desktop.gui import Kiosk
from flask import Flask, render_template


# Configure application
app = Flask(__name__)


# Configure kiosk
kiosk = Kiosk(app)


@app.route('/')
def index():
    return render_template('WebApp.html')


if __name__=='__main__':
    kiosk.run()