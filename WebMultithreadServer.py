
#importing libraries
import socket
import thread
import sys

args_length = len(sys.argv)      #check if any extra arguments are being passed
if args_length > 1:
    host = sys.argv[1]
    port = int(sys.argv[2])
    
else:
    port = 8080                  #if no parameters are passed through command arguments and default values are assigned
    host = 'localhost'          

def multi_Threading(clientsocket, clientaddr):
    print "\n"
    print "\n"
    print "Connection is establishing from: ", clientaddr
    if port:
        file_Toprocessed = clientsocket.recv(1024)
        print file_Toprocessed                     #prints request from client
        file_splits = file_Toprocessed.split()     #splits the request
        file_splits_type = file_splits[0]
        if file_splits_type == 'GET' or file_splits_type == 'FILE' :                    #checks if the request method is FILE
            file_name = file_splits[1]                 #splits the name of the file
            file_requested_type = file_name.split(".")
            if file_requested_type[1] == 'html' or file_requested_type[1] == 'txt':
                message_ToClient = "HTTP/1.1 200 OK \r\n\r\n"
                file_name = file_name[1:]
                file_read = open(file_name,'r')
                data_Read = file_read.read()
                clientsocket.send(message_ToClient)
                clientsocket.send(data_Read.encode('utf-8'))
                #sends the information of server to client
                if file_splits_type == 'FILE' :
                    clientsocket.send('\n INFORMATION OF SERVER')
                    clientsocket.send('\n HOSTNAME: '+ serversocket_hostname)
                    clientsocket.send('\n ADDRESS FAMILY: '+ serversocket_family)
                    clientsocket.send('\n TYPE: '+ serversocket_type)
                clientsocket.close()
                
        else:
            message_ToClient = "HTTP/1.1 404 Not Found \r\n\r\n"
            data_Read = '<html><body><p>Error 404: File not found</p><p>Content-Type: Text/Html</p></body></html>'
            clientsocket.send(message_ToClient)
            clientsocket.send(data_Read.encode('utf-8'))
            clientsocket.close()

if __name__ == "__main__":
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    serversocket.bind(server_address)
    serversocket.listen(5)
    serversocket_family = str(socket.AF_INET)
    serversocket_type = str(socket.SOCK_STREAM)
    serversocket_hostname = str(socket.gethostname())
    
    while True:
        print "Ready for Listening..."
        print "Server is ready for listening connections on "+str(host)+ " "+str(port)+"\n"
        clientsocket, clientaddr = serversocket.accept()
        thread.start_new_thread( multi_Threading, (clientsocket, clientaddr))
serversocket.close()

