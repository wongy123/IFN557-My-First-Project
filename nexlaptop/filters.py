from datetime import timedelta
from flask import Blueprint

filters_bp = Blueprint('filters', __name__)

@filters_bp.app_template_filter('formatStorage')
def formatStorage(storage):
    if storage >= 1000:
        return f"{storage // 1000}TB"
    else:
        return f"{storage}GB"

@filters_bp.app_template_filter('formatScreensize')
def formatScreensize(screensize):
    if screensize % 1 == 0:
        return f"{int(screensize)}"
    else:
        return f"{screensize}"

@filters_bp.app_template_filter('toBrisbaneDate')
def toBrisbaneDate(utc_dt):
    brisbane_offset = timedelta(hours=10)
    brisbane_dt = utc_dt + brisbane_offset
    return brisbane_dt.strftime('%d %b %Y')

@filters_bp.app_template_filter('toBrisbaneTime')
def toBrisbaneTime(utc_dt):
    brisbane_offset = timedelta(hours=10)
    brisbane_dt = utc_dt + brisbane_offset
    return brisbane_dt.strftime('%I:%M %p')