import logging
import sys

# Set up logging
log_file_path = "shared_log.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a logger instance that can be imported in other modules
logger = logging.getLogger("shared_logger")
