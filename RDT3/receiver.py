from socket import *
from time import sleep
from util import create_checksum, verify_checksum

"""
@Purpose: Receiver implementation for RDT 3.0 using UDP.
Receiver class responsible for reliably receiving
messages sent by the sender using the stop-and-wait protocol (RDT 3.0).
It handles simulated corruption, timeouts, duplicate detection, checksum
verification, and ACK generation in accordance with the RDT 3.0 FSM.

@Author: Randy Rizo  
@Course: CPSC5510  
@Date: 2025-05-19  
@Version: 1.0
"""

## No other imports allowed
class Receiver:
    """
    Implements the receiving side of RDT 3.0 over UDP.

    The Receiver class listens for incoming packets, validates checksums,
    simulates packet loss and corruption, handles duplicates, and sends back
    appropriate ACK packets based on sequence number.
    """
    def __init__(self, host='localhost', port=10116):
        """Initialize the receiver with a UDP socket and default state."""
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((host, port))
        self.expected_seq = 0
        self.received_count = 0
        print(f"[INIT] Receiver listening on {host}:{port}\n")

    def start(self):
        """Begin receiving packets using rdt3.0 logic."""
        try:
            while True:
                packet, sender_addr = self.socket.recvfrom(2048)
                self.received_count += 1
                print(f"[RECV] Packet #{self.received_count} received")

                # Simulate timeout every 6th packet
                if self.received_count % 6 == 0:
                    print(f"[SIMULATION] Timeout triggered (packet #{self.received_count})")
                    sleep(2)
                    continue

                # Simulate corruption every 3rd packet (not 6th)
                if self.received_count % 3 == 0:
                    print(f"[SIMULATION] Corruption simulated (packet #{self.received_count})")
                    self._send_ack(sender_addr, 1 - self.expected_seq)
                    continue

                # Check checksum
                if not verify_checksum(packet):
                    print(f"[ERROR] Checksum failed (packet #{self.received_count})")
                    self._send_ack(sender_addr, 1 - self.expected_seq)
                    continue

                # Sequence check
                seq_num = self._extract_seq_num(packet)
                if seq_num != self.expected_seq:
                    print(f"[DUPLICATE] Unexpected seq #{seq_num}, expected #{self.expected_seq}")
                    self._send_ack(sender_addr, 1 - self.expected_seq)
                    continue

                # Deliver message
                payload = packet[12:].decode()
                print(f"[DELIVERED] Payload: {payload}")
                self._send_ack(sender_addr, self.expected_seq)
                self.expected_seq = 1 - self.expected_seq

        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Receiver interrupted by user.")
        finally:
            self.close()

    def _extract_seq_num(self, packet):
        """Extract sequence number from packet."""
        return packet[11] & 0x01

    def _send_ack(self, sender_addr, seq_num):
        """Send an ACK packet."""
        ack_packet = self._build_ack_packet(seq_num)
        self.socket.sendto(ack_packet, sender_addr)
        print(f"[ACK] Sent ACK for seq #{seq_num}\n")

    def _build_ack_packet(self, seq_num):
        """Construct an ACK packet with the correct format."""
        header = b'COMPNETW'
        length = len(header) + 2  # header + flags
        flags = (length << 2) | (1 << 1) | seq_num
        flags_bytes = flags.to_bytes(2, byteorder='big')
        packet_wo_checksum = header + b'\x00\x00' + flags_bytes
        checksum = create_checksum(packet_wo_checksum)
        return header + checksum + flags_bytes

    def close(self):
        """Close the socket."""
        self.socket.close()
        print("[CLOSED] Receiver socket closed.")


if __name__ == "__main__":
    receiver = Receiver(port=10116)  
    receiver.start()