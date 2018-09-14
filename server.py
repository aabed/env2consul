import os
import sys

import consul
from sh import git
from flask import Flask, request

APP = Flask(__name__)
REPOS_ROOT = os.environ['HOME'] + '/' + '.env2consul/'
PORT = int(os.environ.get("PORT", 5000))
APP.debug = bool(os.environ.get('DEBUG'))

def sync_file_to_consul(path, consul_client):
    with open(path) as env_file:
        for line in env_file:
            if '=' in line:
                key, value = line.split('=')
                value = value.strip('\n')
                consul_key = path.replace(REPOS_ROOT, '').lstrip('/').rstrip('.env') + '/' + key
                APP.logger.info('key: %s \tvalue: %s', consul_key, value)
                consul_client.kv.put(consul_key, value)

def sync_repo_to_consul(repo_dir):
    consul_host = os.environ.get("CONSUL_HOST")
    consul_port = os.environ.get("CONSUL_PORT", "80")
    consul_dc = os.environ.get("CONSUL_DC", "dc1")
    consul_token = os.environ.get("CONSUL_TOKEN", "")

    consul_client = consul.Consul(host=consul_host, port=consul_port,
                                  dc=consul_dc, token=consul_token)

    for root, _, files in os.walk(repo_dir):
        for _file in files:
            if _file.endswith('.env'):
                # sync content to consul
                sync_file_to_consul(root + '/' + _file, consul_client)

def get_changes(ssh_url, commit, repo_dir):
    git('init', repo_dir, _cwd=repo_dir)
    git('-c', 'core.askpass=true', 'fetch', '--tags', '--progress', ssh_url,
        '+refs/heads/*:refs/remotes/origin/*', _cwd=repo_dir)
    git('config', 'remote.origin.url', ssh_url)
    git('config', '--add', 'remote.origin.fetch',
        '+refs/heads/*:refs/remotes/origin/*', _cwd=repo_dir)
    git('checkout', '-f', commit, _cwd=repo_dir)

@APP.route('/', methods=['POST'])
def hook_handler():
    data = request.get_json()

    repo_name = data["repository"]["name"]
    ssh_url = data["repository"]["ssh_url"]
    commit = data["commits"][0]["id"]
    repo_dir = REPOS_ROOT + repo_name
    APP.logger.info('%s\t%s', repo_name, commit)

    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)

    get_changes(ssh_url, commit, repo_dir)

    sync_repo_to_consul(repo_dir)
    return "OK"


if __name__ == '__main__':
    try:
        os.environ["CONSUL_HOST"]
    except KeyError:
        print "Please set your CONSUL_HOST before running"
        sys.exit(1)
    APP.run(host='0.0.0.0', port=PORT)
