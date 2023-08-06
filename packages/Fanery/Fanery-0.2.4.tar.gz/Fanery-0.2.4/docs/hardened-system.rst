Hardened System
===============

Hardened Systems are environments that focus on high security and reliability at all levels they can control.

Let's start our journey building the basement that will support our elastic Software solution.

Physical environment
--------------------

The market is rich in alternatives, looking for private cloud virtual machines helps keeping the budget low without sacrifing to much freedom. While choosing you may consider observing the following guidelines:

- Stick to Tier 3/4 companies that offers multiple datacenter options, in multiple geo-locations/continents.
- Make sure to get support for backup/snapshots, unmetered private LAN between VMs, HTTP(S) load balancing and truthful statistics about bandwidth usage.
- Be sure that you get full root access and they let you install customized kernels.
- Use NetCraft data and investigate deeply the Web, looking for satified and disatisfied customers.
- Prefers proven FLOSS virtualization technologies like Xen and KVM.

Automation
----------

From now on installation and configuration steps are presented as shell commands and scripts for the purpose of automation and easy of management.

Intermediate knowledge of Debian GNU/Linux and Shell language is required.

Operating System
----------------

The objective here is walking through the hardening process of Debian GNU/Linux 7 (Wheezy).

System upgrade
^^^^^^^^^^^^^^

#. Setup APT mirrors list.

    .. code:: bash

        cat > /etc/apt/sources.list <<EOF
        deb http://ftp.debian.org/debian/ wheezy main
        deb http://security.debian.org/ wheezy/updates main
        deb http://ftp.debian.org/debian/ wheezy-updates main
        deb http://ftp.debian.org/debian/ wheezy-proposed-updates main
        deb http://ftp.debian.org/debian/ wheezy-backports main
        # iptables SYNPROXY target
        deb http://ftp.debian.org/debian/ testing main
        EOF

        cat >> /etc/apt/preferences << EOF
        Package: *
        Pin: release a=stable
        Pin-Priority: 700

        Package: *
        Pin: release a=wheezy-backports
        Pin-Priority: 650

        Package: *
        Pin: release a=testing
        Pin-Priority: 600
        EOF

#. System upgrade.

    .. code:: bash

        aptitude update
        aptitude full-upgrade

#. Adminitration tools and usefull utils that may not be present after default install.

    .. code:: bash

        aptitude -t wheezy-backports install bzip2 less tmux lsof htop nmon dnsutils iputils-ping telnet-ssl vim-nox wget curl git openssh-client openssh-server sysstat iotop dstat bmon acct strace

Kernel upgrade
^^^^^^^^^^^^^^

#. Kernel >= 3.12 and iptables >= 1.4.21 are required for SYNPROXY support.

    .. code:: bash

        aptitude -t wheezy-backports install linux-image-amd64 linux-headers-amd64

#. Reboot with new Kernel.

    .. code:: bash

        reboot

Firewall setup
^^^^^^^^^^^^^^

#. Install required packages.

    .. code:: bash

        aptitude -t testing install xtables-addons-dkms iptables netsniff-ng
        aptitude -t wheezy-backports install ca-certificates sed wget awk ipset ipcalc geoip-database-contrib libtext-csv-xs-perl unzip

#. Download advanced iptables script with integrated sysctl tuning and hardening.

    .. code:: bash

        wget -c -O /sbin/firewall https://bitbucket.org/mcaramma/linux-setup/raw/master/firewall-synproxy

        chmod 500 /sbin/firewall

#. Download blocklists, build geoip database and load iptables rules (will take a few minutes).

    .. code:: bash

        /sbin/firewall force-load

The proposed firewall script may seams intimidating at first but it's actually well organized and self explanatory, please take the time to study its internals and enjoy the simplicity; it shows howto:

    - Blacklist Anonymous Proxies and Satellite Providers + top sources of internet attacks.
    - Blacklist bogon/hijacked/infected/abusive hosts.
    - Discard invalid/unwanted packets.
    - Tarpit/slow-down spammers.
    - Delude PortScan attempts.
    - Prevent ssh brute-force.
    - Mitigate DDoS attacks.
    - Tune and harden TCP/IP Kernel Stack.

It's also important to stress that the script try hard to create a minimal amount of iptables rules for the job.

DNSCrypt-Proxy
^^^^^^^^^^^^^^

DNS attacks can easily turn our hardening efforts useless, dnscrypt is one way to mitigate most common DNS security threats.

#. Preparation.

    .. code:: bash

        aptitude -t wheezy-backports install build-essential checkinstall wget bzip2

#. Build libsodium deb package.

    .. code:: bash

        cd /usr/src
        mkdir libsodium && cd libsodium
        wget -c https://github.com/jedisct1/libsodium/releases/download/1.0.0/libsodium-1.0.0.tar.gz
        tar -zxvf libsodium-1.0.0.tar.gz
        cd libsodium-1.0.0
        ./configure
        make
        checkinstall --nodoc
        ldconfig -v

#. Build dnscrypt-proxy deb package.

    .. code:: bash

        cd /usr/src
        mkdir dnscrypt && cd dnscrypt
        wget -c https://github.com/jedisct1/dnscrypt-proxy/releases/download/1.4.1/dnscrypt-proxy-1.4.1.tar.bz2
        tar -jxvf dnscrypt-proxy-1.4.1.tar.bz2
        cd dnscrypt-proxy-1.4.1
        ./configure
        make
        checkinstall --nodoc

#. Add dnscrypt user & init script.

    .. code:: bash

        adduser --system --quiet --shell /bin/false --group --disabled-password --disabled-login --no-create-home dnscrypt
        wget -O /etc/default/dnscrypt-proxy -c https://raw.githubusercontent.com/jedisct1/dnscrypt-proxy/master/packages/debian/dnscrypt-proxy.default
        wget -O /etc/init.d/dnscrypt-proxy -c https://raw.githubusercontent.com/jedisct1/dnscrypt-proxy/master/packages/debian/dnscrypt-proxy.init
        sed -i -e '/\(\/usr\)\(\/sbin\/dnscrypt-proxy\)/ s//\1\/local\2/g' /etc/init.d/dnscrypt-proxy
        chmod 550 /etc/init.d/dnscrypt-proxy

#. Set resolv configuration.

    .. code:: bash

        cat > /etc/resolv.conf <<EOF
        search $(hostname -d)
        nameserver 127.0.0.2
        EOF

Miscelaneous hardening and help scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Disable core dumps.

    .. code:: bash

        echo 'fs.suid_dumpable = 0' >> /etc/sysctl.conf
        echo '* hard core 0' >> /etc/security/limits.conf
        echo 'ulimit -S -c 0 > /dev/null 2>&1' >> /etc/profile

#. Decrease per process/thread stack size

    .. code:: bash

        echo '* soft stack 1024' >> /etc/security/limits.conf
        echo '* hard stack 2048' >> /etc/security/limits.conf

#. Disable CTRL+ALT+DEL reboot secuence.

    .. code:: bash

        sed -i -e '/^\(ca:.*:ctrlaltdel:.*\)/ s//#\1/' /etc/inittab

#. Disable crontab for non-root users.

    .. code:: bash

        echo ALL > /etc/cron.deny
        echo root > /etc/cron.allow

        chown root.root /etc/cron.{allow,deny}
        chmod 444 /etc/cron.{allow,deny}

#. Stop using root.

    .. code:: bash

        # Disable local root login
        aptitude -t wheezy-backports install sudo
        sudo passwd -l root

        # Add user operator
        useradd -p "*" -U -m operator -G sudo
        passwd operator
        chage -M 60 -m 7 -W 7 operator

        # Add user sshadmin (remote login only via SSH key ... remember to copy your key with ssh-copy-id)
        useradd -p "*" -U -m sshadmin

        # Disable remote root login
        sed -i -e '/^PermitRootLogin .*/ s//PermitRootLogin no\nAllowUsers sshadmin/' /etc/ssh/sshd_config
        service ssh restart

        # Set motd/issue.net banner text
        cat > /etc/motd <<EOF
        Unauthorized access to this machine is prohibited
        Press <Ctrl-D> if you are not an authorized user
        EOF
        cat /etc/motd > /etc/issue.net
        chown root.root /etc/{motd,issue.net}
        chmod 444 /etc/{motd,issue.net}

#. Build /sbin/lock-filesystem script.

    .. code:: bash

        cat > /sbin/lock-filesystem <<EOF
        #!/bin/sh

        [ -d /var/tmp ] && {
            rm -rf /var/tmp
            ln -s /tmp /var/tmp
        }

        chattr -R +i /boot /usr /bin /sbin /lib* /root /vmlinuz* /initrd* /etc 2> /dev/null
        chattr -R -i /etc/adjtime /etc/blkid.tab /etc/mtab /etc/network/run /etc/udev/rules.d 2> /dev/null

        mount -o ro,remount /boot
        mount -o ro,remount /usr
        mount -o nosuid,noexec,nodev,remount /home
        mount -o nosuid,noexec,nodev,remount /tmp
        EOF

        chmod 500 /sbin/lock-filesystem

#. Build /sbin/unlock-filesystem script.

    .. code:: bash

        cat > /sbin/unlock-filesystem <<EOF
        #!/bin/sh

        mount -o rw,remount /boot
        mount -o rw,remount /usr
        mount -o exec,remount /tmp

        chattr -R -i /boot /usr /bin /sbin /lib* /root /vmlinuz* /initrd* /etc 2> /dev/null
        EOF

        chmod 500 /sbin/unlock-filesystem

#. Build /sbin/system-upgrade script.

    .. code:: bash

        cat > /sbin/system-upgrade <<EOF
        #!/bin/sh

        aptitude update && \\
            /sbin/unlock-filesystem && \\
            aptitude \${1:-safe}-upgrade && \\
            aptitude -f install && \\
            apt-get autoremove && \\
            apt-get autoclean && \\
            apt-get clean && \\
            /sbin/lock-filesystem
        EOF

        chmod 500 /sbin/system-upgrade

#. Build /sbin/lock-system script.

    .. code:: bash

        cat > /sbin/lock-system <<EOF
        #!/bin/sh

        /sbin/lock-filesystem
        /sbin/firewall force-load
        EOF

        chmod 500 /sbin/lock-system

#. Activate /sbin/lock-system after boot.

    .. code:: bash

            sed -i -e 's/^\(exit 0\)/\/root\/lock-system\n\n\1/' /etc/rc.local

#. Remove unnecesary packages.

    .. code:: bash

        aptitude purge at nano tasksel tasksel-data task-english

   No other remotely accessible network service should stand active except ssh.
 
#. Final clean-up.

    .. code:: bash

        aptitude -f install
        apt-get autoremove
        apt-get autoclean
        apt-get clean
        rm -rf /tmp/*
        rm -f /var/log/wtmp /var/log/btmp
        history -c
        reboot

Remark note
-----------

The proposed hardening process is just the beginning, the first step to system hardening; a lot more can be done to strengh the security of a GNU/Linux system, like using a custom grsecurity patched kernel.

From now on every private virtual machine explained is implied to have gone through all the previously described hardening steps.
