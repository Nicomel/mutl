import os

mutl_port = os.getenv('SETTLEMENT_PORT', 8000)
mutl_log_level = os.getenv('MUTL_LOG_LEVEL', 'DEBUG')
mutl_online_default_status = os.getenv('MUTL_ONLINE_DEFAULT_STATUS', False)
mutl_file_path = os.getenv('MUTL_FILE_PATH', '/Users/nicolasmetivier/Code/local/mutl/mutl_repo.pickle')
mutl_local_queue_path = os.getenv('MUTL_LOCAL_QUEUE_PATH', '/Users/nicolasmetivier/Code/local/mutl/mutl_client_queue.pickle')
mutl_server_queue_path = os.getenv('MUTL_SERVER_QUEUE_PATH', '/Users/nicolasmetivier/Code/local/mutl/mutl_server_queue.pickle')