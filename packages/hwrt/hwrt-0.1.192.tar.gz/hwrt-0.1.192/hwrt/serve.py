#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Start a webserver which can record the data and work as a classifier."""

import pkg_resources
from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import os
import json
import requests


# hwrt modules
import hwrt
import hwrt.utils as utils


def submit_recording(raw_data_json):
    """Submit a recording to the database on write-math.com."""
    url = "http://www.martin-thoma.de/write-math/classify/index.php"
    headers = {'User-Agent': 'Mozilla/5.0',
               'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'drawnJSON': raw_data_json}

    s = requests.Session()
    req = requests.Request('POST', url, headers=headers, data=payload)
    prepared = req.prepare()
    s.send(prepared)


def show_results(results, n=10):
    """Show the TOP n results of a classification."""
    import nntoolkit
    classification = nntoolkit.evaluate.show_results(results, n)
    return "<pre>" + classification.replace("\n", "<br/>") + "</pre>"

# configuration
DEBUG = True

template_path = pkg_resources.resource_filename('hwrt', 'templates/')

# create our little application :)
app = Flask(__name__, template_folder=template_path)
Bootstrap(app)
app.config.from_object(__name__)


@app.route('/', methods=['POST', 'GET'])
def heartbeat():
    """Use heartbeat."""
    return request.args.get('heartbeat', '')


@app.route('/interactive', methods=['POST', 'GET'])
def interactive():
    """Interactive classifier."""
    if request.method == 'POST':
        raw_data_json = request.form['drawnJSON']

        # Check recording
        try:
            json.loads(raw_data_json)
        except ValueError:
            return "Invalid JSON string: %s" % raw_data_json

        # Submit recorded json to database
        submit_recording(raw_data_json)

        # Classify
        model_path = pkg_resources.resource_filename('hwrt', 'misc/')
        model = os.path.join(model_path, "model.tar")
        print(model)
        results = utils.evaluate_model_single_recording(model, raw_data_json)

        # Show classification page
        page = show_results(results, n=10)
        page += '<a href="../interactive">back</a>'
        return page
    else:
        # Page where the user can enter a recording
        return render_template('canvas.html')


def get_json_result(results, n=10):
    """Return the top ``n`` results as a json list.
    >>> results = [{'symbolnr': 2, \
                    'probability': 0.65, \
                    'semantics': '\\alpha'}, \
                   {'symbolnr': 45, \
                    'probability': 0.25, \
                    'semantics': '\\propto'}, \
                   {'symbolnr': 15, \
                    'probability': 0.0512, \
                    'semantics': '\\varpropto'}]
    >>> get_json_result(results, n=10)
    [{'\\alpha': 0.65}, {'\\propto': 0.25}, {'\\varpropto': 0.0512}]
    """
    s = []
    for res in results[:min(len(results), n)]:
        s.append({res['semantics']: res['probability']})
    return json.dumps(s)


@app.route('/worker', methods=['POST', 'GET'])
def worker():
    """Implement a worker for write-math.com."""
    if request.method == 'POST':
        raw_data_json = request.form['classify']

        # Check recording
        try:
            json.loads(raw_data_json)
        except ValueError:
            return "Invalid JSON string: %s" % raw_data_json

        # Submit recorded json to database
        submit_recording(raw_data_json)

        # Classify
        model_path = pkg_resources.resource_filename('hwrt', 'misc/')
        model = os.path.join(model_path, "model.tar")
        results = utils.evaluate_model_single_recording(model, raw_data_json)
        return get_json_result(results, n=10)
    else:
        # Page where the user can enter a recording
        return "Classification Worker (Version %s)" % hwrt.__version__


def get_parser():
    """Return the parser object for this script."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    return parser


def main():
    """Main function starting the webserver."""
    app.run()

if __name__ == '__main__':
    main()
