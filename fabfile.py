from time import sleep
from fabric.api import env, run, cd
env.user = 'root'
env.hosts = ['siva-tech.com']
def deploy():
    print "Deploying at Siva-tech.com ..."
    run('cd /root/portal && git pull origin master')
    print "Deplyment complete"
