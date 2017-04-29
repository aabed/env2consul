# env2consul
A small web app that acts as a webhook for your github repo holding your environmental file2consul

## Running

````
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -r requirements.txt
export CONSUL_HOST=your_consul_host
#optionally
export CONSUL_PORT=your_consul_port #defaults to 80
export CONSUL_TOKEN=your_consul_token #defaults to empty
export CONSUL_DC=your_consul_datacentre #defaults to empty

export
python server.py
```

Then you can go ahead an setup your github webhook following this [link](https://developer.github.com/webhooks/creating/)

## Description
If you are using [Twelve-Factor](https://12factor.net/) approach to deliver software, you must be using environmental variables to configure your apps

One of the widely used tools for that is [env2consul](https://github.com/hashicorp/envconsul)

This tool works as a webhook handler to receive the changes on a git repo where you are holding you configurations in the form of environmental file2consul

*example.env*

```
PORT=5050
DEBUG=true
```
this will create a key called example on your consul server
i.e http://consul.myserver.com/v1/kv/example/
under that key you will find key/value pairs as the env above
and when ever you push a change it will create/update the current keys

if your files are under a directory path inside your repo "i.e not in the root of your repo"
for example env/production/example.env
will result into http://consul.myserver.com/v1/kv/production/example/


## Shortages and future work
* delete variables when they are removed from file
* different branches handling
* code quality
* tests
