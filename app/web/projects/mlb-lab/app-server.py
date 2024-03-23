from multiprocessing import Process
from admin.auth import app as admin_app  # Importing app from admin/auth.py
from convertor.server_convertor import app as main_app  # Importing app from server_convertor.py
from admin.auth import login_manager
import os

if __name__ == '__main__':
    # Initialize login_manager for each Flask app
    login_manager.init_app(main_app)
    login_manager.init_app(admin_app)

    # Define functions to run each Flask app in a separate process
    def run_main_app():
        main_app.run(host="0.0.0.0", port=7000)

    def run_admin_app():
        admin_app.run(host="0.0.0.0", port=3000)

    # Create and start processes for each Flask app
    main_process = Process(target=run_main_app)
    admin_process = Process(target=run_admin_app)

    main_process.start()
    admin_process.start()

    # Wait for both processes to finish
    main_process.join()
    admin_process.join()
