from threading import Thread
from flask import Flask
from admin.auth import app as admin_app  # Importing app from admin/auth.py
from server_convertor import app as main_app  # Importing app from server_convertor.py

if __name__ == '__main__':
    # Define functions to run each Flask app in a separate thread
    def run_main_app():
        main_app.run(host="0.0.0.0", port=7000)

    def run_admin_app():
        admin_app.run(host="0.0.0.0", port=3000)

    # Create and start threads for each Flask app
    main_thread = Thread(target=run_main_app)
    admin_thread = Thread(target=run_admin_app)

    main_thread.start()
    admin_thread.start()

    # Wait for both threads to finish
    main_thread.join()
    admin_thread.join()
