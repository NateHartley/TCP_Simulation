class Packet():
    def __init__(self, data=""):
        # -- TCP HEADER -- #
        self.flags = {"CWR":0, "ECE":0, "URG":0, "ACK":0, "PSH":0, "RST":0, "SYN":0, "FIN":0}
        # TODO: sequence number - order tracking of data
        # TODO: acknowledgement number - confirms receipt of data
        # TODO: checksum - error detection
        
        # -- TCP PAYLOAD -- #
        self.data = data

    def set_flag(self, name):
        if name in self.flags:
            self.flags[name] = 1
    
    def clear_flag(self, name):
        if name in self.flags:
            self.flags[name] = 0

    # Object needs to covert to dictionary before its deserialised
    def to_dict(self):
        return {"flags": self.flags,
                "data": self.data}

# TCP Packet consists of TCP header and TCP payload
# TCP header includes: source port, destination port, sequence number, acknowledgement number, data offset, reserved, flags (SYN, ACK etc.), window size, checksum, urgent pointer, options (if any)
# TCP payload includes: the actual data like "Hello World"

# PACKET SHOULD NOT CONTAIN STATES, these are supposed to be set manually inside each client/server file to simulate individual computer memory