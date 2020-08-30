import os

mutl_port = os.getenv('SETTLEMENT_PORT', 8080)
mutl_log_level = os.getenv('MUTL_LOG_LEVEL', 'DEBUG')
mutl_file_path = os.getenv('MUTL_FILE_PATH', '/Users/nicolasmetivier/Code/local/mutl/mutl.json')