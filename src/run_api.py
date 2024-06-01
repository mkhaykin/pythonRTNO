import logging
import sys

import uvicorn

from api.main import app

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
    ],
    format="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa S104
