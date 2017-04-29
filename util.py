import consul
from sh import git
import os

def file2consul(file,key):

    consul_host=os.environ.get("CONSUL_HOST")
    consul_port=os.environ.get("CONSUL_PORT","80")
    consul_dc=os.environ.get("CONSUL_DC","dc1")
    consul_token=os.environ.get("CONSUL_TOKEN","")

    consul_client = consul.Consul(host=consul_host, port=consul_port,dc=consul_dc,token=consul_token)
    with open(file) as myfile:
        for line in myfile:
            #import ipdb; ipdb.set_trace()
            name, var = line.partition("=")[::2]
            consul_client.kv.put(''.join(key.split('.')[:-1])+'/'+name,var)

def get_changes(ssh_url,commit,repo_dir):
    git('init',repo_dir,_cwd=repo_dir)
    git('-c','core.askpass=true','fetch','--tags','--progress',ssh_url,'+refs/heads/*:refs/remotes/origin/*',_cwd=repo_dir)
    git('config','remote.origin.url',ssh_url)
    git('config','--add','remote.origin.fetch','+refs/heads/*:refs/remotes/origin/*',_cwd=repo_dir)
    git('checkout','-f',commit,_cwd=repo_dir)
