import os

CDN_URL = os.environ.get('AP_DEJA_VU_CDN_URL','http://int.nyt.com.s3.amazonaws.com/cdn')

def build_context():
    """
    Every page needs these two things.
    """
    context = {}
    context['CDN_URL'] = CDN_URL
    return dict(context)

def to_bool(v):
    print v
    return v.lower() in ("yes", "true", "t", "1")