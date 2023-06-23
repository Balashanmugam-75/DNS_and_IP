import socket,glob,json


port = 53 #DNS operates on port 53 by default
ip = '127.0.0.1'

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #socket object(using IPv4)
sock.bind((ip,port))

def load_zone():

    jsonzone = {}
    zonefiles = glob.glob('zones/*.zone')
    for zone in zonefiles:
        with open(zone) as zonedata:
            data = json.load(zonedata)
            zonename = data['$origin']
            jsonzone[zonename] = data
    return jsonzone

zonedata = load_zone()

def getflags(flags):

    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])
    rflags = '' #response flags
    QR = '1' #first bit of flag is always 1
    OPCODE = ''
    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))

    AA = '1'
    TC = '0'
    RD = '0'
    RA = '0'
    Z = '000'
    RCODE = '0000'

    return int(QR+OPCODE+AA+TC+RD,2).to_bytes(1,byteorder='big')+int(RA+Z+RCODE,2).to_bytes(1,byteorder='big')

def getquestiondomain(data):

    state = 0
    expectedlength = 0
    domainstring = ''
    domainparts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            if byte != 0:
                domainstring += chr(byte)
            x += 1
            if x == expectedlength:
                domainparts.append(domainstring)
                domainstring = ''
                state = 0
                x=0
            if byte == 0:
                domainparts.append(domainstring)
                break

        else:
            state = 1
            expectedlength = byte
        y+=1

    questiontype = data[y:y+2]
    return(domainparts,questiontype)

def getzone(domain):
    global zonedata

    zone_name = '.'.join(domain)
    return zonedata[zone_name]

def getrecs(data):
    domain,questiontype = getquestiondomain(data)
    qt = ''
    if questiontype == b'\x00\x01':
        qt = 'a'

    zone = getzone(domain)
    return (zone[qt],qt,domainname)

def buildresponse(data):

    #TransactionID
    TransactionID = data[:2]
    TID = ''
    for byte in TransactionID:
        TID += (hex(byte))[2:]

    #Get Flags
    Flags = getflags(data[2:4])

    #Question Count
    QDCOUNT = b'\x00\x01'

    #Answer count
    getquestiondomain(data[12:])

    print(len(getrecs(data[12:])[0]))

while(1):
    data,addr = sock.recvfrom(512)
    r = buildresponse(data)
    sock.sendto(r,addr)
