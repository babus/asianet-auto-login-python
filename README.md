#asianet-auto-login-python#

Asianet auto login python script and executable.
___
###Requirements###
Windows: [Python 2.7](http://www.python.org/download/releases/2.7.5/)(to run from source) and [py2exe](http://www.py2exe.org/)(For building exe). If you intend to use `.exe` then no additional installations needed.

Linux: Python 2.7
___
###Features###
1. Does auto-login.
2. Send keep alive signal for uninterrupted browsing and downloading.

___

###Setup###
#####Windows#####
1. Get the zip and extract to any directory.<code>-u [username] -p [password]</code>
2. Use Windows Task Schedular to schedule the task targetting `.exe`. 
3. "At login, At task creation/modification" triggers will be enough with repeat every 5 minutes.

#####Linux#####
1. Download `src/asianet_login.py`.
2. Add a cron job to run `src/asianet_login.py` with arguments <code>-u [username] -p [password]</code> with repeat every 5 minutes.


