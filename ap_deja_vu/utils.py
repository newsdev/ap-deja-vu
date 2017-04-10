import os
import socket

def build_context():
    """
    Every page needs these two things.
    """
    context = {}
    context['hostname'] = socket.gethostname()
    return dict(context)

def to_bool(v):
    return v.lower() in ("yes", "true", "t", "1")
