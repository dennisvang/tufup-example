import logging
import sys

from myapp import main, settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info(f'{settings.APP_NAME} {settings.APP_VERSION}')

# run the app
main(sys.argv[1:])
