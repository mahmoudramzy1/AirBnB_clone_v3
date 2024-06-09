
"""first status"""


@app_views.route('/status')
def status():
    """return status"""
from api.v1.views import app_views
    return { "status": "OK" }
