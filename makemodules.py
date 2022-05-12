"""
Create migrations
en base al folder apps for migrations change path persint volumen
"""

import json
import os

dir_apps = "apps/"
dir_migrations = "dbmigrations"
file_name = "__init__.py"
modules = {}
dir_exclude = ["__pycache__"]
dir_modules = "config/settings/modules.py"


def scan_dir(dirname):
    """Scan dir an return sub folders"""
    folders = [
        f.name for f in os.scandir(dirname) if f.is_dir() and f.name not in dir_exclude
    ]
    return folders


def touch_file(dir_file_name):
    open(dir_file_name, "a").close()
    os.utime(dir_file_name, None)


apps = scan_dir(dir_apps)
for app in apps:
    file_path = f"{dir_migrations}/{app}/{file_name}"
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    touch_file(file_path)
    modules.update({app: f"{dir_migrations}.{app}"})

with open(dir_modules, "w") as temp:
    temp.write("MODULES = %s" % (json.dumps(modules)))
