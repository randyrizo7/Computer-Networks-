from socket import *
from util import *

"""
@Purpose: Sender implementation for RDT 3.0 using UDP.
Sender class responsible for reliably sending
application messages to a receiver using the stop-and-wait protocol (RDT 3.0).
It simulates reliable data transfer by handling packet creation, timeouts,
ACK verification, and retransmissions over an unreliable UDP channel.

@Author: Randy Rizo  
@Course: CPSC5510  
@Date: 2025-05-19  
@Version: 1.0
"""

class Sender:
    """
      Implements the sending side of RDT 3.0 over UDP sockets.

      The Sender class handles message packetization, sequence number management,
      timeout-based retransmissions, and ACK validation to simulate reliable
      communication over an unreliable transport.
    """
    def __init__(self):
        self.receiver_host = '127.0.0.1'
        self.receiver_port = 10116
        self.sender_socket = socket(AF_INET, SOCK_DGRAM)
        self.seq_num = 0
        self.packet = None
        self.acknowledged = False
        self.data = None
        self.packet_number = 1
    """
    Reliably send a single message to the receiver using RDT 3.0.

    Constructs a packet, sends it, and waits for a valid ACK. If a timeout occurs
    or a corrupted/duplicate ACK is received, the message is resent. Successfully
    received messages are acknowledged, and the sequence number is toggled.

    Args:
        app_msg_str (str): The message to be sent in the packet's data field.
    """

    def rdt_send(self, app_msg_str):
        #store message and reset ack 
        self.data = app_msg_str
        self.acknowledged = False

        #print oringal message being sent. 

        print("original message string: {}".format(self.data))
        self.packet = make_packet(self.data, 0, self.seq_num)
        print("packet created: {}".format(self.packet))

        #loop until valid ack is recvd 
        while not self.acknowledged:
            self.sender_socket.sendto(self.packet, (self.receiver_host, self.receiver_port))
            print("packet num.{} is successfully sent to the receiver.".format(self.packet_number))

            self.sender_socket.settimeout(2)
            try:
                ack_packet, addr = self.sender_socket.recvfrom(1024)
            except timeout:
                print("socket timeout! Resend!\n")
                print("[timeout retransmission]: {}".format(self.data))
                self.packet_number += 1
                continue
            #extract 16 bit flags 
            flags = int.from_bytes(ack_packet[10:12], byteorder='big')
            ack_flag = (flags >> 1) & 0x01
            ack_seq = flags & 0x01
            #check if ack vaid 
            if verify_checksum(ack_packet) and ack_flag == 1 and ack_seq == self.seq_num:
                print("packet is received correctly: seq num {} = ACK num {}. all done!\n".format(self.seq_num, self.seq_num))
                self.seq_num = 1 - self.seq_num
                self.acknowledged = True
                #resend packet if ack not valid . 
            else:
                print("receiver acked the previous pkt, resend!\n")
                print("[ACK-Previous retransmission]: {}".format(self.data))
                self.packet_number += 1
                self.sender_socket.sendto(self.packet, (self.receiver_host, self.receiver_port))
                print("packet num.{} is successfully sent to the receiver.".format(self.packet_number))
                try:
                    ack_packet, addr = self.sender_socket.recvfrom(1024)
                    flags = int.from_bytes(ack_packet[10:12], byteorder='big')
                    ack_flag = (flags >> 1) & 0x01
                    ack_seq = flags & 0x01
                    if verify_checksum(ack_packet) and ack_flag == 1 and ack_seq == self.seq_num:
                        print("packet is received correctly: seq num {} = ACK num {}. all done!\n".format(self.seq_num, self.seq_num))
                        self.seq_num = 1 - self.seq_num
                        self.acknowledged = True
                except timeout:
                    print("socket timeout! Resend!\n")
                    print("[timeout retransmission]: {}".format(self.data))

            self.packet_number += 1




  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT change the function name.                    #######                    
  ####### You can have other functions if needed.                             #######   