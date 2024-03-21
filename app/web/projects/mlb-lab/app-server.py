from multiprocessing import Process
from admin.auth import app as admin_app  # Importing app from admin/auth.py
from convertor.server_convertor import app as main_app  # Importing app from server_convertor.py
import os

if __name__ == '__main__':
    # Define functions to run each Flask app in a separate process
    def run_main_app():
        os.system("gunicorn -b 0.0.0.0:7000 convertor.server_convertor:app")

    def run_admin_app():
        os.system("gunicorn -b 0.0.0.0:3000 admin.auth:app")

    # Create and start processes for each Flask app
    main_process = Process(target=run_main_app)
    admin_process = Process(target=run_admin_app)

    main_process.start()
    admin_process.start()

    # Wait for both processes to finish
    main_process.join()
    admin_process.join()
