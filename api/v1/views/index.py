from api.v1.views import app_views

"""first status"""


@app_views.route('/status')
def status():
    """return status"""
    return { "status": "OK" }
