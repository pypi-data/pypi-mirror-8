Backend Web Farm
================

The web application we'll build with Fanery is going to run inside a restricted and replicable environment.

Restricted environment
----------------------

Schroot is a tool that offers many additional functionalities not found in chroot.

Alternatives like LXC or Docker are also valid but we are already running inside a Xen/KVM virtualized environment with more isolation garanties; adding another virtualization layer won't be beneficial in term of performance or security.

Replicable environment
----------------------

Our goal here is to build a restricted environment that provides the conditions for:

- quick and easy replication to several different private virtual machines.
- quick and easy switching between different versions of the same application.
- graceful code reload.

Schroot bootstrap script
^^^^^^^^^^^^^^^^^^^^^^^^

First let's create a simple shell script that aid and speed-up the creation of schroot bootstrapped minimal Debian Wheezy environments.

#. Install required packages.

    .. code:: bash

        aptitude -t wheezy-backports install debootstrap schroot bzip2

#. Change schroot default bind setup.
   
   Do not share /home and /tmp partitions with main system.

    .. code:: bash

        sed -i -e '/\(^\/home\)/ s//#\1/' -e '/\(^\/tmp\)/ s//#\1/' /etc/schroot/default/fstab

#. Build /sbin/bootstrap-schroot script.

    .. code:: bash

        cat > /sbin/bootstrap-schroot <<EOF
        #!/bin/sh

        [ \$# -lt 4 ] && {
            echo "Usage: \$0 SYSTEM VGNAME LVNAME LVSIZE [LVTYPE]"
            exit 1
        }

        SYSTEM=\$1
        VGNAME=\$2
        LVNAME=\$3
        LVSIZE=\$4
        LVTYPE=\${5:-xfs}

        lvcreate -n \$LVNAME -L\$LVSIZE \$VGNAME && \\
            mkfs.\$LVTYPE /dev/\$VGNAME/\$LVNAME && \\
            mount -t \$LVTYPE /dev/\$VGNAME/\$LVNAME /mnt && \\
            debootstrap --include apt-utils,aptitude,locales,dialog \\
                        --exclude tasksel,tasksel-data,nano,isc-dhcp-client \\
                        --variant=minbase wheezy /mnt http://ftp.debian.org/debian || \\
            exit 1

        grep -v ^mount /sbin/unlock-filesystem > /mnt/sbin/unlock-filesystem
        grep -v ^mount /sbin/lock-filesystem > /mnt/sbin/lock-filesystem
        echo "# schroot nssdatabases
        chattr -i /etc /etc/passwd /etc/shadow /etc/group /etc/gshadow /etc/services /etc/protocols /etc/networks /etc/hosts
        " >> /mnt/sbin/lock-filesystem
        chmod 500 /mnt/sbin/{lock,unlock}-filesystem
        cp -a /sbin/system-upgrade /mnt/sbin/
        cp -a /etc/apt/sources.list /etc/apt/preferences /mnt/etc/apt/
        cp -a /usr/src/libsodium/libsodium*/libsodium*.deb /mnt/usr/src/
        cp -a /etc/skel /mnt/home/operator
        chown -R operator.operator /mnt/home/operator

        umount /mnt

        cat >> /etc/schroot/schroot.conf <<EOC

        [\$SYSTEM]
        type=lvm-snapshot
        users=operator
        root-users=operator
        source-root-users=operator
        device=/dev/\$VGNAME/\$LVNAME
        lvm-snapshot-options=--size 2G
        EOC

        schroot -c source:\$SYSTEM -u root --directory /root -- sh -c "
            dpkg-reconfigure locales
            dpkg-reconfigure tzdata
            aptitude update
            aptitude full-upgrade
            aptitude -f install
            apt-get autoremove
            apt-get autoclean
            apt-get clean
            rm -f /etc/ssh_host_*
            rm -rf /var/tmp /tmp/*
            ln -s /tmp /var/tmp
            rm -f /var/log/wtmp /var/log/btmp
            /sbin/lock-filesystem
            history -c"
        EOF

        chmod 500 /sbin/bootstrap-schroot

Build Fanery tarball
^^^^^^^^^^^^^^^^^^^^

Now it's time to build our fanery node base tarball, a single compressed files that we'll be able to replicate as many times as required.

#. Bootstrap Wheezy minbase.

    .. code:: bash

        /sbin/bootstrap-schroot wheezy-fanery VG-NAME LV-NAME 1G

#. Enter schroot in write mode.

    .. code:: bash

        schroot -c source:wheezy-fanery -u root

#. Install packages required to build Fanery dependencies.

    .. code:: bash

        aptitude install build-essential pkg-config graphviz-dev uuid-dev libffi-dev libev-dev python-dev
        dpkg -i /usr/src/libsodium*.deb

#. Install Python virtualenv and wrappers.

    .. code:: bash

        aptitude -t wheezy-backports install python-setuptools git
        easy_install pip
        pip install setuptools --no-use-wheel --upgrade
        pip install virtualenv virtualenvwrapper

#. Setup virtualenvwrappers.

    .. code:: bash

        su - operator
        mkdir ~/.virtualenvs
        cat >> .bashrc <<EOF

        VIRTUALENVWRAPPER_PYTHON=$(which python2.7)
        export WORKON_HOME=\$HOME/.virtualenvs
        export PIP_VIRTUALENV_BASE=\$WORKON_HOME
        export PIP_RESPECT_VIRTUALENV=true
        source /usr/local/bin/virtualenvwrapper.sh
        EOF
        . .bashrc

#. Create project virtualenv.

    .. code:: bash

        mkvirtualenv MyProject
        pip install fanery gunicorn rainbow-saddle
        python .virtualenvs/MyProject/lib/python*/site-packages/fanery/tests/test_term.py
        python .virtualenvs/MyProject/lib/python*/site-packages/fanery/tests/test_service.py
        pip install git+https://bitbucket.org/USER-NAME/MyProject.git@v0.0.1
        deactivate

#. Build project start script.

    .. code:: bash

        mkdir ~/bin
        cat > ~/bin/project <<EOF
        #!/bin/sh

        [ \$# -lt 2 ] && {
            echo "Usage: \$0 {start|stop|restart|reload} PROJECT"
            echo "           upgrade PROJECT GITREPO"
            exit 1
        }

        VIRTUALENVWRAPPER_PYTHON=$(which python2.7)
        export WORKON_HOME=\$HOME/.virtualenvs
        export PIP_VIRTUALENV_BASE=\$WORKON_HOME
        export PIP_RESPECT_VIRTUALENV=true
        source /usr/local/bin/virtualenvwrapper.sh

        ACTION=\$1
        shift
        PROJECT=\$1
        shift
        GITREPO=\$1
        PIDFILE=/var/run/\${PROJECT}.pid

        case "\${ACTION}" in
            start)
                workon \${PROJECT} && {
                    CORES=\$(grep ^processor /proc/cpuinfo | wc -l)
                    WORKERS=\$((\${CORES} * 2 + 1))
                    rainbow-saddle --pid \${PIDFILE} gunicorn -w \${WORKERS} $@
                }
                ;;
            stop)
                kill -TERM \$(cat \${PIDFILE})
                ;;
            restart|reload)
                kill -HUP \$(cat \${PIDFILE})
                ;;
            upgrade)
                workon \${PROJECT} && \\
                    pip install \${GITREPO} --upgrade && \\
                    kill -HUP \$(cat \${PIDFILE})
                }
                ;;
        esac

        exit \$?
        EOF

        chmod 500 ~/bin/project
 
#. Cleanup.

    .. code:: bash

        exit
        aptitude -f install
        apt-get autoremove
        apt-get autoclean
        apt-get clean
        rm -rf /tmp/*
        rm -f /var/log/wtmp /var/log/btmp
        /sbin/lock-system
        history -c

#. Exit schroot and create compressed tarball.

    .. code:: bash

        exit
        mount -t auto /dev/VG-NAME/LV-NAME /mnt
        cd /mnt
        mkdir /var/lib/schroot/tarballs
        tar -Jcvf /var/lib/schroot/tarballs/MyProject-node_$(date +%F_%T).tar.xz ./
        cd /var/lib/schroot/tarballs
        umount /mnt
        ls -lh

#. Build schroot node setup script.

    .. code:: bash

        cat > /var/lib/schroot/tarballs/build-schroot <<EOF
        #!/bin/sh

        XZFILE=\$1
        SYSTEM=\$2
        VGNAME=\$3
        LVNAME=\$4
        LVSIZE=\$5
        LVTYPE=\${6:-xfs}

        [ \$# -lt 5 ] && {
            echo "Usage: \$0 XZFILE SYSTEM VGNAME LVNAME LVSIZE [LVTYPE]"
            exit 1
        }

        lvcreate -n \$LVNAME -L\$LVSIZE \$VGNAME && \\
            mkfs.\$LVTYPE /dev/\$VGNAME/\$LVNAME && \\
            mount -t \$LVTYPE /dev/\$VGNAME/\$LVNAME /mnt && \\
            tar -C /mnt -Jxvf \$XZFILE || exit 1

        umount /mnt

        /sbin/unlock-filesystem

        aptitude update
        aptitude full-upgrade
        aptitude -t wheezy-backports install schroot tar xz
        apt-get autoremove
        apt-get autoclean
        apt-get clean

        sed -i -e '/\(^\/home\)/ s//#\1/' -e '/\(^\/tmp\)/ s//#\1/' /etc/schroot/default/fstab

        cat >> /etc/schroot/schroot.conf <<EOC

        [\$SYSTEM]
        type=lvm-snapshot
        users=operator
        root-users=operator
        source-root-users=operator
        device=/dev/\$VGNAME/\$LVNAME
        lvm-snapshot-options=--size 2G
        EOC

        /sbin/lock-filesystem
        EOF

        chmod 500 /var/lib/schroot/tarballs/build-schroot

Web farm node setup
^^^^^^^^^^^^^^^^^^^

We are now ready to replicate our project node in a few simple steps to whatever Debian based hardened virtual machine we selected as member of our `Backend Web Farm`.

#. Preparation.

    .. code:: bash

        aptitude -t wheezy-backports install schroot
        cd /var/lib/schroot/
        scp -r sshadmin@host:/var/lib/schroot/tarballs .

#. Build schrooted node from tarball.

    .. code:: bash

        cd /var/lib/schroot/tarballs
        ./build-schroot MyProject-node_VERSION.tar.xz MyProject VG-NAME LV-NAME 10G

WebApp management
^^^^^^^^^^^^^^^^^

Once in place our Web application is easily managed via schroot sessions.

#. Start MyProject daemon.

    .. code:: bash

        schroot -b -n MyProject -c MyProject -u operator
        schroot -r -c MyProject -- /home/operator/bin/project start MyProject myproject:app --log-level debug

#. Project version upgrade and graceful code reload.

    .. code:: bash

        schroot -c source:MyProject -u operator -- /home/operator/bin/project upgrade MyProject git+https://bitbucket.org/USER-NAME/MyProject.git@v0.0.2

Read schroot-faq(7) man page for more details about schroot sessions.
