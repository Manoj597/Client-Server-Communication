#importing libraries
import sys
import socket
import urllib


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #creating socket

args_length = len(sys.argv)      #check if any extra arguments are being passed
if args_length > 1:
    port = int(sys.argv[1])      #passess port number that if it is passed through command arguments
else:
    port = 8080                  #if no parameters are passed through command arguments and default values are assigned
               
host = 'localhost'
server_address = (host, port)
serverSocket.bind(server_address)   #binds host and port number together    
serverSocket.listen(3)              #listen to the binded address
print '\nhttp request to '+str(host)+':'+ str(port)
if not port == "" :
    print 'Ready for Listening...'
    (client_connection, (client_ipaddress,client_port)) = serverSocket.accept()     #connection that accepts from the client
    #server information
    serversocket_Address_family = str(socket.AF_INET)
    serversocket_type = str(socket.SOCK_STREAM)    
    serversocket_hostname = socket.gethostname()
    
    client_request = client_connection.recv(1024)       #request that receives from client
    print client_request       #printing client request
    print "\n CLIENT IP ADDRESS: "+str(client_ipaddress)+"\n CLIENT PORT NUMBER: "+str(client_port)     #prints client ip address and port number
    #processing the request for sending back requested file
    request_method = client_request.split(' ')[0]
    if request_method == 'GET' or request_method == 'FILE' :                    #checks if the request method is FILE
        file_requested = client_request.split()     #contains the name of the file required
        file_requested = file_requested[1]
        file_requested_type = file_requested.split(".")
        if file_requested_type[1] == 'html' or file_requested_type[1] == 'txt':
            message_ToClient = "HTTP/1.1 200 OK \nContent-Type: Text/Html \r\n\r\n"
            file_name = file_requested[1:]
            file_read = open(file_name,'r')
            data_Read = file_read.read()
            client_connection.send(message_ToClient)
            client_connection.send(data_Read.encode('utf-8'))
            #sends the information of server to client
            if request_method == 'FILE' :
                client_connection.send('\n SERVER INFORMATION')
                client_connection.send('\n HOSTNAME: '+ serversocket_hostname)
                client_connection.send('\n ADDRESS_FAMILY: '+ serversocket_Address_family)
                client_connection.send('\n TYPE: '+ serversocket_type)
            client_connection.close()
     
        else :
            message_ToClient = "HTTP/1.1 404 Not Found \n Content-Type: Text/Html \r\n\r\n"
            data_Read = '<html><body><p>Error 404: File not found</p><p>Content-Type: Text/Html</p></body></html>'
            client_connection.send(message_ToClient)
            client_connection.send(data_Read.encode('utf-8'))
            client_connection.close()
     
            
serverSocket.close()

