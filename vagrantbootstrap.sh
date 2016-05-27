#!/bin/bash


LJUST_COLS=20
RJUST_COLS=30
VERBOSE=true
RUNSERVER=false


function init() {
    printf "\n\nVERBOSE = $VERBOSE, toggle in vagrantbootstrap.sh\n\n"
    sleep 1

    echo "killing running dev servers"
    pkill -9 -f "python manage.py"
}

function progress() {
    if $VERBOSE
    then
        $@
    else
        cmd="$@"
        $@ &> /dev/null &
        pid=$!
        spinner='-\|/'

        i=0
        while kill -0 $pid &> /dev/null
        do
            i=$(( (i+1) %4 ))
            printf "\r\t%-${LJUST_COLS}.${LJUST_COLS}s %${RJUST_COLS}s" "${cmd}" "[ ${spinner:$i:1}${spinner:$i:1} ]"
            sleep .1
        done

        if [ $? -ne 0 ]
        then
            echo "return code $?";
        fi
        printf "\r\t%-${LJUST_COLS}.${LJUST_COLS}s %${RJUST_COLS}s\n" "${cmd}" "[ OK ]"
    fi
}

function update_packages() {
    echo "updating packages"
    progress sudo apt-get update
}

function install_packages() {
    echo "installing packages"
    progress sudo apt-get install -y \
        python-dev python-setuptools python-virtualenv vim \
        tmux screen git-core curl build-essential openssl \
        libjpeg8 libjpeg8-dev zlib-bin libtiff4 libtiff4-dev libfreetype6 libfreetype6-dev libwebp2 libpq-dev libssl-dev \
        python-psycopg2 imagemagick gettext sqlite3
}

function setup_virtualenv() {
    echo "installing virtualenvwrapper"
    # use pip to install globally, installing with apt doesn't create the shellscript for sourcing
    progress sudo pip install virtualenvwrapper
    source /usr/local/bin/virtualenvwrapper.sh

    if ! grep -q "source /usr/local/bin/virtualenvwrapper.sh" .bashrc; then
        echo "adding script to .bashrc"
        echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
    fi

    echo "creating virtualenv"
    progress mkvirtualenv mobiauth
}

function install_mobiauth_requirements() {
    echo "installing mobiauth requirements"
    workon mobiauth
    cd /vagrant
    progress pip install -U -r requirements.txt
}

function prepare_and_run_mobiauth() {
    workon mobiauth
    cd /vagrant
    echo "creating tables"
    progress python manage.py syncdb
    if $RUNSERVER
    then
        echo "starting dev server"
        python manage.py runserver 0.0.0.0:8000 &
        echo "done, check http://localhost:8001 on host"
    fi
}

init
update_packages
update_packages
install_packages
setup_virtualenv
install_studlan_requirements

# Support for pip install inside the VM
curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | python
rm setuptools-7.0.zip
