FROM centos:centos7.4.1708
MAINTAINER "Vaishal" <vaishal.shah@hcl.com>
ENV container docker

RUN yum -y update; yum clean all

RUN yum -y install systemd; yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

RUN yum -y groupinstall "Development Tools";
RUN yum -y install epel-release;

RUN yum -y install git rsync \
                   zlib-devel openssl-devel readline-devel \
                   libyaml-devel libffi-devel gdbm-devel \
                   httpd-devel libcurl-devel apr-devel apr-util-devel mod_ssl\
                   mariadb-devel mariadb-server vim wget nodejs; yum clean all;

RUN wget https://kojipkgs.fedoraproject.org//packages/sqlite/3.8.11/1.fc21/x86_64/sqlite-devel-3.8.11-1.fc21.x86_64.rpm; \
        wget https://kojipkgs.fedoraproject.org//packages/sqlite/3.8.11/1.fc21/x86_64/sqlite-3.8.11-1.fc21.x86_64.rpm; \
        yum install -y sqlite-3.8.11-1.fc21.x86_64.rpm sqlite-devel-3.8.11-1.fc21.x86_64.rpm; \
        curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo; \
        rpm --import https://dl.yarnpkg.com/rpm/pubkey.gpg; \
        curl --silent --location https://rpm.nodesource.com/setup_10.x | bash; \
        yum -y install yarn;

RUN git clone https://github.com/rbenv/rbenv.git ~/.rbenv; \
        echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bash_profile; \
        echo 'eval "$(rbenv init -)"' >> ~/.bash_profile; \
        git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build; \
        source ~/.bash_profile; \
        rbenv install 2.7.1; \
        npm cache clean -f; \
        npm install -g n; \
        n stable; \
        mv -f /usr/local/bin/node /usr/bin/node;

VOLUME /sys/fs/cgroup

CMD ["/usr/sbin/init"]