from flask import Flask, request
import os
import json
from sh import git
import util
import sys
app = Flask(__name__)
home=os.environ['HOME']
@app.route('/',methods=['POST'])
def hook_handler():
    changes=[]
    data = request.get_json()
    print "New commit by: {}".format(data['commits'][0]['author']['name'])
    if data['head_commit']['modified']:
        changes.append(data['head_commit']['modified'])

    elif data['head_commit']['added']:
       changes.append(data['head_commit']['added'])
    else:
        return 1
    changes=[item for sublist in changes for item in sublist]
    repo_name=data["repository"]["name"]
    ssh_url=data["repository"]["ssh_url"]
    commit=data["commits"][0]["id"]

    if not os.path.exists(home+'/.env2consul/'+repo_name):
        os.makedirs(home+'/.env2consul/'+repo_name)

    repo_dir=home+'/.env2consul/'+repo_name
    print changes
    util.get_changes(ssh_url,commit,repo_dir)


    for change in changes:
        util.file2consul(home+'/.env2consul/'+repo_name+'/'+change,change)
    return "OK"


if __name__ == '__main__':
     try:
         os.environ["CONSUL_HOST"]
     except KeyError:
        print "Please set your CONSUL_HOST before running"
        sys.exit(1)
     app.debug = True
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)
