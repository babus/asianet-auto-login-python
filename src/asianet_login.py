"""
@name: Asianet auto login script - V1.0
@author: Babu Somasundaram (bubalanisaipriyan@gmail.com)
@credit: V R Vijayaraj for the earlier base version

Usage: asianet_login.py [options]

Options:
  -h, --help            show this help message and exit
  -u USERNAME, --username=USERNAME    Username of your ADL connection.
  -p PASSWORD, --password=PASSWORD    Password of your ADL connection.

LICENCE:
--------
Copyright © 2013 Babu Somasundaram
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import httplib
import os
import sys
import urllib
from datetime import datetime
from optparse import OptionParser


debug = True  # Print flag


def log_message(msg):
    log_msg = datetime.now().strftime(
        "%b %d, %Y %I:%M %p") + " - " + msg + "\n"
    if debug:
        print log_msg
    logfile.write(log_msg)


def send_keep_alive():
    log_message("Sending keep alive to " + keep_alive_url)
    params = "alive=y&auth_user=%s" % (user_name)
    response = urllib.urlopen(keep_alive_url, params)
    if response.info().status == 200 or response.info().status == 202 or response.info().status == "":
        log_message("Sent keep alive..")
    else:
        log_message("Sending keep alive failed..")


def do_asianet_login():
    log_message("Logging into the Asianet..")
    params = urllib.urlencode({'auth_user': user_name,
                               'auth_pass': password,
                               'accept': accept})
    response = urllib.urlopen(login_url, params)
    log_message("Response: %s" % (response.info().status))
    if response.info().status == 200 or response.info().status == 202 or response.info().status == "":
        log_message("Login Successful..")
    else:
        log_message("Login Failed. Try again later..")


def do_auto_login():
    """
    Do a test connection with google and if not success, redirect to asianet login
    """
    try:
        log_message("Test connecting to %s" % (test_con_url))
        test_con = httplib.HTTPConnection(test_con_url)  # create a connection
        test_con.request("GET", test_con_resouce)  # do a GET request
        response = test_con.getresponse()  # get the response
        test_con.close()
        if response.status == 304 or response.status == 302:  # not yet connected
            do_asianet_login()
        elif response.status == 200 or response.status == 202:  # active connection present
            log_message("Active connection present.")
            send_keep_alive()
        else:
            log_message("Oops..something went wrong. " +
                        "Response: %s %s" % (response.status, httplib.responses[response.status]))
    except:
        log_message("Error sending the request.")

# Script execution starts here
# Parsing the commandline arguments, 'username' and 'password'
parser = OptionParser()
parser.add_option("-u", "--username", dest="username",
                  help="Username of your ADL connection.")
parser.add_option("-p", "--password", dest="password",
                  help="Password of your ADL connection.")
(options, args) = parser.parse_args()

if hasattr(options, 'username') and options.username and hasattr(options, 'password') and options.password:
    user_name = options.username
    password = options.password
else:
    parser.print_help()
    sys.exit()

accept = 'Login >>'
test_con_url = "www.google.com"  # For connection testing
test_con_resouce = "/intl/en/policies/privacy/"  # may change in future

# Login and Keep-alive URL. Hard-coding here since asianet changes their urls often.
login_url = "https://mwcp-spg-01a.adlkerala.com:8003/index.php"
keep_alive_url = "https://mwcp-spg-01a.adlkerala.com:8003"

src_dir = os.path.dirname(os.path.realpath(sys.argv[0]))  # Getting the current directory path
log_file = os.path.join(src_dir, "connection_log.log")  # this will be automatically created
logfile = open(log_file, "a")
do_auto_login()
log_message("Exiting..")
logfile.close()
sys.exit()
