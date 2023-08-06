aptitude -t wheezy-backports install xorg spectrwm xdm schroot uswsusp conky arandr git-flow
cat > ~/.conkyrc <<EOF
out_to_x no
out_to_console yes
update_interval 1.0
total_run_times 0
use_spacer none
TEXT
{time %R %a,%d-%#b-%y} |Up:${uptime_short} |Temp:${acpitemp}C |Batt:${battery_short} |RAM:$memperc% |CPU:${cpu}% | ${downspeedf eth0}
EOF

pip install bpython ipython ipdb
cd ~/.vim
mkdir -p bundle && cd bundle
git clone git://github.com/klen/python-mode.git

cd
cat > .vimrc <<EOF
" Pathogen load
filetype off

call pathogen#infect()
call pathogen#helptags()

filetype plugin indent on
syntax on
EOF

cat >> ~/.ipython/profile_default/ipython_config.py <<EOF
c.InteractiveShellApp.extensions = ['autoreload']
c.InteractiveShellApp.exec_lines = ['%autoreload 2']
EOF
