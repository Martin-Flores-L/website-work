from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os

#secret
import pandas as pd

# Create your views here.
@login_required
def osp_status(request):
    """
    Renders the 'query.html' template.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered HTML template.
    """
    return render(request, 'osp_status.html')