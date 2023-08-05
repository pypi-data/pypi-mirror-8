#!/bin/sh

DEBUG=""
DAEMON=""
PYTHON="python2"

kill_process() {
    # $1 is the file containing the PID to kill, $2 is the process name
    if [ -f $1 ]; then
        PID=`cat $1`
        if ps -p $PID > /dev/null; then
            echo "Terminating $2... "
            kill -INT $PID
        else
            echo "No running process of ID $PID... removing PID file"
            rm -f $1
        fi
    else
        echo "$2 is probably not running (PID file doesn't exist)"
    fi
}

#We use python to parse config files
eval `"$PYTHON" << PYTHONEND
from libervia.server.constants import Const as C
from sat.memory.memory import fixLocalDir
from ConfigParser import SafeConfigParser
from os.path import expanduser, join
import sys
import codecs
import locale

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

fixLocalDir()  # XXX: tmp update code, will be removed in the future

config = SafeConfigParser(defaults=C.DEFAULT_CONFIG)
try:
    config.read(C.CONFIG_FILES)
except:
    print ("echo \"/!\\ Can't read main config ! Please check the syntax\";")
    print ("exit 1")
    sys.exit()

env=[]
env.append("PID_DIR='%s'" % join(expanduser(config.get('DEFAULT', 'pid_dir')),''))
env.append("LOG_DIR='%s'" % join(expanduser(config.get('DEFAULT', 'log_dir')),''))
env.append("APP_NAME='%s'" % C.APP_NAME)
env.append("APP_NAME_FILE='%s'" % C.APP_NAME_FILE)
print ";".join(env)
PYTHONEND
`
PID_FILE="$PID_DIR$APP_NAME_FILE.pid"
LOG_FILE="$LOG_DIR$APP_NAME_FILE.log"

# if there is one argument which is "stop", then we kill Libervia
if [ $# -eq 1 ];then
    if [ $1 = "stop" ];then
        kill_process $PID_FILE "$APP_NAME"
        exit 0
    elif [ $1 = "debug" ];then
        echo "Launching $APP_NAME in debug mode"
        DEBUG="--debug"
    elif [ $1 = "fg" ];then
        echo "Launching $APP_NAME in foreground mode"
        DAEMON="n"
    fi
fi


#Don't change the next lines
PLUGIN_OPTIONS="-d .."
AUTO_OPTIONS=""
ADDITIONAL_OPTIONS="--pidfile $PID_FILE --logfile $LOG_FILE $AUTO_OPTIONS $DEBUG"


MAIN_OPTIONS="-${DAEMON}o"

log_dir=`dirname "$LOG_FILE"`
if [ ! -d $log_dir ] ; then
    mkdir $log_dir
fi

twistd $MAIN_OPTIONS $ADDITIONAL_OPTIONS $APP_NAME_FILE $PLUGIN_OPTIONS
