#My Name: Sai Vamshi Thonukunuri, My Partner: Sai Krishna Palukuri
import socket
import time
import random

s_b_id = "sthonuku"

print("Connected")
robo_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
robo_soc.connect(("192.168.1.71", 3310)) #here we are initiating a tcp connection to robot
robo_soc.send(s_b_id.encode()) #here we are sending encoded blazer id to the robot.
print("BlazerID sent successfully..")

cn_port = int(robo_soc.recv(1024).decode()) #here we are recieving a TCP port number
print(f"TCP port {cn_port} received!!!")

print("Creating new socket s2 ...")
robo_udp_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #here we are creating a new tcp connection object
robo_udp_soc.bind(("", cn_port)) #here we are binding the socket to the TCP port
robo_udp_soc.listen(1) 
conn, addr = robo_udp_soc.accept() #here we are listening to any incoming connections and accepting the connection request and creating a new connection object.

iTCPPort2Connect = conn.recv(1024).decode().split(',') #here we are recieving a tcp port number from the robot
print("UDP ports", iTCPPort2Connect[0] + "," + iTCPPort2Connect[1], "received!!")
s_port = int(iTCPPort2Connect[0])
r_port = int(iTCPPort2Connect[1]) #here we are splitting recieved port number object and storing into a separate variables.

udp_soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
udp_soc.bind(("", r_port))  #here we are creating a udp socket object and binding it to the port
num = int(random.uniform(5,10))
print(f"Sending {num} using port {s_port}")
udp_soc.sendto(str(num).encode(), ("192.168.1.71", s_port)) #we are sending the num as a UDP message to robot ip address

data, addr = udp_soc.recvfrom(int(num * 10)) #here we are recieving a response from the server for the sent message
print(f"Recieved {data.decode()} using port {r_port}")

print("Sending UDP packets:")  #this will send the udp packets in loop to the robot
for i in range(5):
    udp_soc.sendto(data, ("192.168.1.71", s_port))
    print(f"Packet {i} sent!!")
    time.sleep(1)
print("Sent!") 

robo_soc.close()
robo_udp_soc.close()
udp_soc.close()  #we are closing all the sockets after all the needed communication is done.