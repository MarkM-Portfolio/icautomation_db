Install Docker on local machine
Reference Links -: https://docs.docker.com/docker-for-windows/install/

                                 -: https://docs.docker.com/docker-for-mac/install/

Save attached Dockerfile on your local.
Build the docker image and Run the container with below commands.
 docker build -t dashboard_setup .
 docker run -t -d --privileged -p 3000:3000 --name dashboard -h "server.hcl.lan" dashboard_setup
 docker exec -it dashboard bash
You are now inside docker container, Clone the dashboard project from git inside container.We need to create ssh key and add pub key in github repository to clone dashboard inside container.
 ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub
Copy the key and add to your github repository.
Clone the repo.
 cd ~
 git clone git@git.cwp.pnp-hcl.com:conn-automation/dashboard.git
 cd dashboard/
Install the Gems of the project.
 source ~/.bash_profile
rbenv local 2.7.1
gem install bundler -v "2.1.4"
rbenv rehash
bundle
yarn install
rake db:setup
source ~/.bash_profile
rails server -d -b 0.0.0.0
       7. Open Web browser and run “localhost:3000” should open Dashboard UI.

 

********************

Things you need to setup also:

Need to configure LDAP in config/ldap.yml file for development environment.

 

For Development Environment we can use below code

development:

  host: icsswgldap.cnx.cwp.pnp-hcl.com

  port: 389

  attribute: mail

  base: ou=collab,dc=ibm,dc=com

  admin_user: uid=Fvt Admin,cn=Users,ou=collab,dc=ibm,dc=com

  admin_password: fvtadmin

 

***********************

Troubleshoot:

If you are getting this error after you run "bundle":

Your bundle is locked to mimemagic (0.3.5), but that version could not be found in any of the sources listed in your Gemfile. If you haven't changed sources, that means the author of mimemagic (0.3.5) has removed it. You'll need to update your
bundle to a version other than mimemagic (0.3.5) that hasn't been removed in order to install.

Solution:

Try to remove Gemfile.lock and bundle again


LOGIN CREDS:
username: ajones1@janet.iris.com
password: jones1