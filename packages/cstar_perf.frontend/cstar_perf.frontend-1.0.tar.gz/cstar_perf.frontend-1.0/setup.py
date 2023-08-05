import sys
from setuptools import setup, find_packages

requires = (
    'flask',
    'Flask-Script',
    'flask_sockets',
    'gunicorn',
    'cassandra-driver',
    'google-api-python-client',
    'ecdsa',
    'daemonize',
    'websocket-client',
    'pyzmq',
    'fabric',
    'pyyaml',
    'supervisor',
    'pexpect',
    'blist'
)

setup(
    name = 'cstar_perf.frontend',
    version = '1.0',
    description = 'A web frontend for cstar_perf, the Cassandra performance testing platform',
    author = 'The DataStax Cassandra Test Engineering Team',
    author_email = 'ryan@datastax.com',
    url = 'https://github.com/datastax/cstar_perf',
    install_requires = requires,
    namespace_packages = ['cstar_perf'],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    entry_points = {'console_scripts': 
                    ['cstar_perf_client = cstar_perf.frontend.client.client:main',
                     'cstar_perf_server = cstar_perf.frontend.lib.server:main',
                     'cstar_perf_notifications = cstar_perf.frontend.server.notifications:main']},
)

from cstar_perf.frontend.lib.crypto import generate_server_keys
generate_server_keys()
