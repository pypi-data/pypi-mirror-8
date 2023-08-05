"""Main Application Controllers"""
import functools
import httplib2
import os.path
import uuid
import time
from functools import partial

import zmq
import json
from flask import ( Flask, render_template, request, redirect, abort, Response,
                    jsonify, make_response, session)
from apiclient.discovery import build
from oauth2client.client import ( AccessTokenRefreshError,
                                  AccessTokenCredentials,
                                  flow_from_clientsecrets,
                                  FlowExchangeError)

from app import app, db, sockets
from model import Model, UnknownUserError, UnknownTestError
from notifications import console_subscribe

import logging
log = logging.getLogger('cstar_perf.controllers')


### Google+ API:
gplus = build('plus', 'v1')
google_client_secrets = os.path.join(os.path.expanduser("~"),'.cstar_perf','client_secrets.json')
with open(google_client_secrets) as f:
    google_client_id = json.load(f)['web']['client_id']

################################################################################
#### Template functions:
################################################################################
def get_user_id():
    return session.get('user_id', None)
app.jinja_env.globals['get_user_id'] = get_user_id

def user_is_authenticated():
    return session.get('logged_in',False)
app.jinja_env.globals['user_is_authenticated'] = user_is_authenticated


################################################################################
#### Helpers
################################################################################
def user_in_role(role, user=None):
    """Find if a user is in the given role"""
    if user is None:
        user = get_user_id()
    try:
        user_roles = db.get_user_roles(get_user_id())
        if role in user_roles:
            return True
    except UnknownUserError:
        pass
    return False

def requires_auth(role):
    """Ensures the current user has the appropriate authorization before
    running the wrapped function"""
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kw):
            # Do the check:
            if user_is_authenticated():
                if user_in_role(role):
                    return function(*args, **kw)
            return make_response(render_template('access_denied.jinja2.html'), 401)
        return wrapper
    return decorator

@app.context_processor
def inject_template_variables():
    """Common variables available to all templates"""
    return dict(clusters = db.get_cluster_names(),
                google_client_id=google_client_id)

################################################################################
#### Page Controllers
################################################################################

@app.route('/')
def index():
    return render_template('index.jinja2.html')

@app.route('/login', methods=['POST'])
def login():
    """Login via Google+"""
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(google_client_secrets, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return make_response(
            jsonify({'error':'Failed to upgrade the authorization code.'}), 401)

    # An ID Token is a cryptographically-signed JSON object encoded in base 64.
    # Normally, it is critical that you validate an ID Token before you use it,
    # but since you are communicating directly with Google over an
    # intermediary-free HTTPS channel and using your Client Secret to
    # authenticate yourself to Google, you can be confident that the token you
    # receive really comes from Google and is valid. If your server passes the
    # ID Token to other components of your app, it is extremely important that
    # the other components validate the token before using it.
    gplus_id = credentials.id_token['sub']
    
    stored_credentials = AccessTokenCredentials(session.get('credentials'), 
                                                request.user_agent)
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        return make_response(jsonify(
            {'success':'Current user is already connected.'}), 200)
    # Get the user's email address:
    http = httplib2.Http()
    http = credentials.authorize(http)
    # Get a list of people that this user has shared with this app.
    google_request = gplus.people().get(userId='me')
    user_obj = google_request.execute(http=http)
    email = None
    # Find the google account email:
    for e in user_obj['emails']:
        if e['type'] == 'account':
            email = e['value']
            break
    else:
        return make_response(
            jsonify({'error':'Authorization from Google failed.'}), 401)
    
    # Store the access token in the session for later use.
    session['credentials'] = credentials.access_token
    session['gplus_id'] = gplus_id
    session['logged_in'] = True
    session['user_id'] = email
    return make_response(jsonify({'success':'Successfully connected user.'}), 
                         200)

@app.route('/logout', methods=['GET','POST'])
def logout():
    for i in ['credentials','gplus_id','logged_in'] :
        try:
            session.pop(i)
        except KeyError:
            pass
    if request.method == "POST":
        return make_response(jsonify({'success':'Logged out.'}), 200)
    else:
        return redirect("/")


@app.route('/tests')
def tests():
    clusters = db.get_cluster_names()
    cluster_scheduled_tests = {}
    cluster_in_progress_tests = {}
    for c in clusters:
        scheduled_tests = db.get_scheduled_tests(c)
        if len(scheduled_tests) > 0:
            cluster_scheduled_tests[c] = scheduled_tests
        in_progress_tests = db.get_in_progress_tests(c)
        if len(in_progress_tests) > 0:
            cluster_in_progress_tests[c] = in_progress_tests
    completed_tests = db.get_completed_tests()
    return render_template('tests.jinja2.html', clusters=clusters, 
                           cluster_scheduled_tests=cluster_scheduled_tests, 
                           cluster_in_progress_tests=cluster_in_progress_tests,
                           completed_tests=completed_tests)

@app.route('/tests/user')
@requires_auth('user')
def my_tests():
    queued_tests = db.get_user_scheduled_tests(get_user_id())
    in_progress_tests = db.get_user_in_progress_tests(get_user_id())
    completed_tests = db.get_user_completed_tests(get_user_id())
    failed_tests = db.get_user_failed_tests(get_user_id(), 10)
    return render_template('user.jinja2.html', queued_tests=queued_tests, 
                           in_progress_tests=in_progress_tests, 
                           completed_tests=completed_tests,
                           failed_tests=failed_tests)

@app.route('/tests/id/<test_id>')
def view_test(test_id):
    try:
        test = db.get_test(test_id)
    except UnknownTestError:
        return make_response('Unknown Test {test_id}.'.format(test_id=test_id), 404)
    artifacts = db.get_test_artifacts(test_id)

    has_chart = False
    for a in artifacts:
        if a['artifact_type'] in ['failure','link']:
            # Proactively fetch non-blob artifacts:
            a['artifact'] = db.get_test_artifact_data(test_id, a['artifact_type']).artifact
        if a['artifact_type'] == 'stats':
            has_chart = True

    return render_template('view_test.jinja2.html', test=test, artifacts=artifacts, has_chart=has_chart)

@app.route('/tests/artifacts/<test_id>/<artifact_type>')
def get_artifact(test_id, artifact_type):
    if artifact_type == 'graph':
        return redirect("/graph?stats={test_id}".format(test_id=test_id))
    artifact, description = db.get_test_artifact_data(test_id, artifact_type)
    if description.endswith(".tar.gz"):
        mimetype = 'application/gzip'
    elif description.endswith(".json"):
        mimetype = 'application/json'
    else:
        mimetype = 'text/plain'

    return Response(response=artifact,
                    status=200,
                    mimetype=mimetype,
                    headers={"Content-Disposition": "filename={name}".format(name=description)}
    )

@app.route('/graph')
def graph():
    return render_template('graph.jinja2.html')


@app.route('/schedule', methods=['GET', 'POST'])
@requires_auth('user')
def schedule():
    """Page to schedule a test - GET to view - POST test json to pre-populate page"""
    job = None
    if request.method == "POST":
        job = request.get_json()
    return render_template('schedule.jinja2.html', job=job)

@app.route('/cluster/<cluster_name>')
@requires_auth('user')
def cluster(cluster_name):
    return render_template('cluster.jinja2.html',
                           cluster_name=cluster_name)
    
################################################################################
#### JSON API
################################################################################

@app.route('/api/tests/schedule', methods=['POST'])
@requires_auth('user')
def schedule_test():
    """Schedule a test"""
    job = request.get_json()
    job_id = uuid.uuid1()
    job['test_id'] = str(job_id)
    job['user'] = get_user_id()
    db.schedule_test(test_id=job_id, user=job['user'], 
                     cluster=job['cluster'], test_definition=job)
    return jsonify({'success':True, 'url':'/tests/id/{test_id}'.format(test_id=job['test_id'])})

@app.route('/api/tests/cancel', methods=['POST'])
@requires_auth('user')
def cancel_test():
    """Cancel a scheduled test"""
    test_id = request.form['test_id']
    if user_in_role('admin'):
        db.update_test_status(test_id, 'cancelled')
    else:
        # Check if the test is owned by the user:
        test = db.get_test(test_id)
        if test['user'] == get_user_id():
            db.update_test_status(test_id, 'cancelled')
        else:
            return make_response(jsonify({'error':'Access Denied to modify test {test_id}'
                            .format(test_id=test_id)}), 401)
    return jsonify({'success':'Test cancelled'})
    
@requires_auth('user')
@app.route('/api/tests/id/<test_id>')
def get_test(test_id):
    """Retrieve the definition for a scheduled test"""
    try:
        test = db.get_test(test_id)
        log.debug(test)
        return jsonify(test)
    except UnknownTestError:
        return make_response(jsonify({'error':'Unknown Test {test_id}.'.format(test_id=test_id)}), 404)

@requires_auth('user')
@app.route('/api/clusters')
def get_clusters():
    """Retrieve information about available clusters"""
    clusters = db.get_cluster_names()
    return make_response(jsonify({'clusters':clusters}))


################################################################################
#### Websockets
################################################################################

@requires_auth('user')
@sockets.route('/api/console')
def console_messages(ws):
    """Receive console messages as they happen

    ZMQ message format:
     Console messages:
      console cluster_name {"job_id":"current_job_id", "msg":"message from console"}
     Control messages:
      Keep alive:
      The cluster is starting a job:
       console cluster_name {"job_id":"current_job_id", "ctl":"START"}
      The cluster finished a job:
       console cluster_name {"job_id":"current_job_id", "ctl":"DONE"}
      The cluster is not working on anything:
       console cluster_name {"ctl":"IDLE"}

    When forwarding messages to the websocket client, the "console cluster_name" 
    portion is dropped and just the JSON is sent.

    Websocket sends keepalive messages periodically:
     {"ctl":"KEEPALIVE"}

    """
    cluster_name = ws.receive()
    console_socket = console_subscribe(cluster_name)
    try:
        while True:
            try:
                data = console_socket.recv_string()
                data = data.lstrip("console {cluster_name} ".format(cluster_name=cluster_name))
                ws.send(data)
            except zmq.error.Again:
                # If we timeout from zmq, send a keep alive request to the
                # websocket client:
                ws.send('{"ctl":"KEEPALIVE"}')
                # The client websocket will send keepalive back:
                ws.receive()
            except zmq.error.ZMQError, e:

                if e.errno == zmq.POLLERR:
                    log.error(e)
                    # Interrupted zmq socket code, reinitialize:
                    # I get this when I resize my terminal.. WTF?
                    console_socket = setup_zmq()
    finally:
        log.error("Unsubscribing from zmq socket")
        console_socket.setsockopt_string(zmq.UNSUBSCRIBE, u'')
