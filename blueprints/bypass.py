from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from core.bypass import bypass
import httpx

bypass = Blueprint('bypass', __name__, template_folder='templates')

@bypass.route('/url_bypass/', methods=['post', 'get'])
def check_url():
    message = {
        "method": "GET",
        "body": " "
    }
    if request.method == "GET":
        return render_template('bypass.html', message=message)
    else:
        bypass(request.form.get('url'))