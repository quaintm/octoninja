#!flask/bin/python

from app import app, manager
manager.run()
app.run(debug=True)
