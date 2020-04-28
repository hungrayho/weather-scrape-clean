import settings
import os

if not os.path.exists(settings.PATH):
    os.mkdir(settings.PATH)
