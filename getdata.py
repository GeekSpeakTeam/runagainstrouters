import netmiko
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
import time
import sys
import getpass
timestr = time.strftime("%Y%m%d-%H%M%S")

if input("This Script will execute a set of commands against the routers in the text file and extract data.  Are you sure you want to continue? (y/n)") != "y":
    exit()

##### Getpass used so you do not need to hardcode the password into the configuration file ####
def get_credentials():
    username = input("Enter username: ")
    pasnsword = getpass.getpass()
    return username, password   

IP_LIST = open('C:\Python\PythonProjects\ciscoautomation\devices.txt')
username, password = get_credentials()
for IP in IP_LIST:
    print ('\n'+ IP.strip() + '  \n' )
    try:
        connection = netmiko.ConnectHandler(ip=IP, device_type="cisco_ios", username=username, password=password, secret=password)
    except NetMikoTimeoutException:
        print ('Device not reachable.')
        continue
    except AuthenticationException:
        print ('Authentication Failure.')
        continue
    except SSHException:
        print ('Make sure SSH is enabled in device.')
        continue

    # This gets us the hostname of the device so we can pop it into the file name further below
         
    hostname = connection.send_command('show run | i host')
    hostname.split(" ")
    hostname,device = hostname.split(" ")

    print ("Saving Logs for " + device)
    
    # Open file to write to
    filename = "/Python/PythonProjects/ciscoautomation/backup/TACACS-Change"+ timestr+device+ ".txt"

    # This is where you put the files you want to run to make changes to the box - config commands

   
    output = connection.send_config_from_file(config_file = 'C:\Python\PythonProjects\ciscoautomation\command.txt')
    print(output)
    
    # This is where you put the files you want to run to get information from the box - show commands
    COMMAND_LIST = open('C:\Python\PythonProjects\ciscoautomation\commandss.txt')
    
    for show in COMMAND_LIST:
        output2 = connection.send_command(show)    
        print (output2)
        with open(filename, "a") as f:    
            f.write(output2 + "\n")
            f.write("$" + "\n")
            f.close()
    connection.disconnect()

    