from flask import Flask
from admin.auth import app as admin_app  # Importing app from admin/auth.py
from server_convertor import app as main_app  # Importing app from server_convertor.py

if __name__ == '__main__':
    # Run both Flask apps
    main_app.run(host="0.0.0.0", debug=True, port=7000)
    admin_app.run(host="0.0.0.0", debug=True, port=3000)
