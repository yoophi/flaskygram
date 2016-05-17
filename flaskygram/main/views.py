# -*- coding: utf8 -*-
from flask import request, render_template

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
