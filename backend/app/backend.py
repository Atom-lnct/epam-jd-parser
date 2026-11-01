import os
import sys

app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)) , "backend" , "app")
if app_dir not in sys.path:
     sys.path.insert(0, app_dir)


from main import app

__all__ = ["app"]
