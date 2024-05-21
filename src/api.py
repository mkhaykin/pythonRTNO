import logging
import sys

import uvicorn

from api import app

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
    ],
    format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
