"""
@Purpose: Utility functions for RDT 3.0 implementation using UDP sockets.
This module provides packet construction, checksum creation, and verification
tools used by both the sender and receiver to ensure reliable data transfer.

Implements the final version of the stop-and-wait protocol (RDT 3.0) as defined
in the course project specifications.
@Author: Randy Rizo
@Course: CPSC5510
@Date: 2025-05-19
@version 1.0
"""

def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """
    # Ensure even number of bytes for 16-bit words
    if len(packet_wo_checksum) % 2 != 0:
        packet_wo_checksum += b'\x00'

    checksum = 0
    for i in range(0, len(packet_wo_checksum), 2):
        word = (packet_wo_checksum[i] << 8) + packet_wo_checksum[i+1]
        checksum += word

        # Wrap around carry bits
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    # One's complement
    checksum = ~checksum & 0xFFFF

    # Return as 2-byte big-endian
    return checksum.to_bytes(2, byteorder='big')

    

def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """

    # Extract the received checksum (bytes 8–9)
    received_checksum = packet[8:10]

    # Replace checksum bytes with zeros to recompute
    temp_packet = packet[:8] + b'\x00\x00' + packet[10:]

    # Compute checksum from rest of packet
    computed_checksum = create_checksum(temp_packet)

    # Return whether they match
    return received_checksum == computed_checksum

def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    # Constant header
    prefix = b'COMPNETW'  # 8 bytes

    # Encode data
    data_bytes = data_str.encode()

    #  calculate total packet length 
    total_len = len(prefix) + 2 + len(data_bytes)  

    # Construct 16-bit flags 
    flag_bits = (total_len << 2) | (ack_num << 1) | seq_num
    flag_bytes = flag_bits.to_bytes(2, byteorder='big')

    # Build packet without checksum to calculate it
    packet_wo_checksum = prefix + b'\x00\x00' + flag_bytes + data_bytes

    # Create actual checksum 
    checksum = create_checksum(packet_wo_checksum)

    #  Final packet 
    packet = prefix + checksum + flag_bytes + data_bytes

    return packet


    # make sure your packet follows the required format!


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  
