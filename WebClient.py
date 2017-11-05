
#importing the libraries
import socket
import sys
import timeit

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #client object is created
args_length = len(sys.argv)
if args_length > 1:                #check if any extra arguments are being passed
    host = sys.argv[1]
    port = sys.argv[2]
    file_processed = '/'+sys.argv[3]
else:
    port = '8080'                  #if no parameters are passed through command arguments and default values are assigned
    host = 'localhost'             #host name is localhost
    file_processed = '/Sample.html'
port_length = len(port)
file_extn = file_processed.split('.')[1]
if port_length == 4 and (file_extn == 'txt' or file_extn == 'html' or file_extn == 'htm')  :
    client_socket_type =  str(socket.SOCK_STREAM)          #getting the socket type
    client_socket_family = str(socket.AF_INET)             #getting the socket family
    client_socket_hostname = socket.gethostname()          #getting the hostname
    print"\n"               
    port = int(port)
    clientSocket.connect((host, port))                     #connection to the server
    client_socket_peername = str(clientSocket.getpeername())
    #request for the file
    clientSocket.send("FILE "+file_processed+" HTTP/1.0\n")
    #sending the client information to the server
    clientSocket.send("\n INFORMATION OF CLIENT")
    clientSocket.send("\n CLIENT HOSTNAME: "+client_socket_hostname)
    clientSocket.send("\n CLIENT ADDRESS FAMILY: "+client_socket_family)
    clientSocket.send("\n CLIENT TYPE: "+client_socket_type)
    clientSocket.send("\n CLIENT PEER NAME: "+client_socket_peername)

    file_start_time = timeit.default_timer()         #calculation of the RTT begins 
    while True:
            recieved = clientSocket.recv(2048)       #receiving file from the server
            RTT_file_processing = timeit.default_timer() - file_start_time   #calculating final reading of the RTT
            if recieved == "": break
            print recieved,                       #printing the file received

    print "\n RTT: "+str(RTT_file_processing)     #printing the calculated RTT value
else :
    if not port_length == 4 :
        print "\nPort is not defined properly "
    else :
        print "\nfile name is not defined properly and it's extension should be .html or .txt"
clientSocket.close()
print "\n Processed"
