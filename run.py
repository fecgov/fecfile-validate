import os
import settings

from api.validate import app


if __name__ == '__main__':
    app.debug = True
    host = settings.API_URL
    port = settings.API_PORT
    app.run(host=host, port=port)
