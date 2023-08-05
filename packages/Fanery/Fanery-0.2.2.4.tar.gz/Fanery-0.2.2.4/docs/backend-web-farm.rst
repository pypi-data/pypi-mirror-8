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

        SYSTEM=\$1
        VGNAME=\$2
        LVNAME=\$3
        LVSIZE=\$4
        LVTYPE=\${5:-xfs}

        lvcreate -n \$LVNAME -L\$LVSIZE \$VGNAME && \\
            mkfs.\$LVTYPE /dev/\$VGNAME/\$LVNAME && \\
            mount -t \$LVTYPE /dev/\$VGNAME/\$LVNAME /mnt && \\
            debootstrap --include aptitude,locales,dialog \\
                        --exclude tasksel,tasksel-data,nano,isc-dhcp-client \\
                        --variant=minbase wheezy /mnt http://ftp.debian.org/debian || \\
            exit 1

        grep -v ^mount /sbin/unlock-filesystem > /mnt/sbin/unlock-filesystem
        grep -v ^mount /sbin/lock-filesystem > /mnt/sbin/lock-filesystem
        chmod 500 /mnt/sbin/{lock,unlock}-filesystem
        cp -a /sbin/system-upgrade /mnt/sbin/
        cp -a /etc/apt/{sources.list,preferences} /mnt/etc/apt/
        cp -a /usr/src/dnscrypt/libsodium*/libsodium*.deb /mnt/usr/src/
        cp -a /etc/skel /mnt/home/operador
        chown -R operador.operador /mnt/home/operador

        umount /mnt

        cat >> /etc/schroot/schroot.conf <<EOC
        [\$SYSTEM]
        type=lvm-snapshot
        users=operador
        root-users=operador
        source-root-users=operador
        device=/dev/\$VGNAME/\$LVNAME
        lvm-snapshot-options=--size 2G
        EOC

        schroot -c \$SYSTEM:source -u root sh -c "
            dpkg-reconfigure locales
            dpkg-reconfigure tzdata
            aptitude full-upgrade
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

        schroot -c wheezy-fanery:source -u root

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

        su - operador
        mkdir ~/.virtualenvs
        cat >> .bashrc <<EOF
        VIRTUALENVWRAPPER_PYTHON=$(which python2.7)
        export WORKON_HOME=\$HOME/.virtualenvs
        export PIP_VIRTUALENV_BASE=\$WORKON_HOME
        export PIP_RESPECT_VIRTUALENV=true
        source /usr/local/bin/virtualenvwrapper.sh
        EOF

#. Create project virtualenv.

    .. code:: bash

        mkvirtualenv MyProject
        pip install fanery gunicorn rainbow-saddle
        python .virtualenvs/MyProject/lib/python*/site-packages/fanery/tests/test_term.py
        python .virtualenvs/MyProject/lib/python*/site-packages/fanery/tests/test_service.py
        pip install git+https://bitbucket.org/USER-NAME/MyProject.git@v0.0.1
        deactivate
        exit

#. Build project start script.

    .. code:: bash

        mkdir ~/bin
        cat > ~/bin/project <<EOF
        #!/bin/sh

        VIRTUALENVWRAPPER_PYTHON=$(which python2.7)
        export WORKON_HOME=\$HOME/.virtualenvs
        export PIP_VIRTUALENV_BASE=\$WORKON_HOME
        export PIP_RESPECT_VIRTUALENV=true
        source /usr/local/bin/virtualenvwrapper.sh

        ACTION=\$1
        shift
        PROJECT=\$1
        shift
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
        esac

        exit \$?
        EOF

        chmod 500 ~/bin/project
 
#. Cleanup.

    .. code:: bash

        exit
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
        tar -Jcvf /var/lib/schroot/tarballs/MyProject-node_$(date +%F_%H).tar.xz ./

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
        aptitude clean

        sed -i -e '/\(^\/home\)/ s//#\1/' -e '/\(^\/tmp\)/ s//#\1/' /etc/schroot/default/fstab

        cat >> /etc/schroot/schroot.conf <<EOC
        [\$SYSTEM]
        type=lvm-snapshot
        users=operador
        root-users=operador
        source-root-users=operador
        device=/dev/\$VGNAME/\$LVNAME
        lvm-snapshot-options=--size 2G
        EOC

        /sbin/lock-filesystem
        EOF

        chmod 500 /var/lib/schroot/tarballs/build-schroot

Web farm node setup
^^^^^^^^^^^^^^^^^^^

We are now ready to replicate our project node in a few simple steps.

#. Preparation.

    .. code:: bash

        cd /var/lib/schroot/
        scp -r sshadmin@host:/var/lib/schroot/tarballs .

#. Build schrooted node from tarball.

    .. code:: bash

        cd /var/lib/schroot/tarballs
        ./build-schroot MyProject-node_VERSION.tar.xz MyProject VG-NAME LV-NAME 10G

And finally enjoy the simplicity.

#. Start MyProject schroot session.

    .. code:: bash

        schroot -b -n MyProject -c MyProject -u operador
        schroot -r -c MyProject -- /home/operador/bin/project start MyProject myproject:app --log-level debug

#. Project version upgrade and graceful code reload.

    .. code:: bash

        schroot -c MyProject-source -u root -- /bin/sh -c "
            su - operador -c '
                workon MyProject
                pip install git+https://bitbucket.org/USER-NAME/MyProject.git@v0.0.2 --upgrade
                ~/bin/project reload MyProject
            '"

Read schroot-faq(7) man page for more details about schroot sessions.
