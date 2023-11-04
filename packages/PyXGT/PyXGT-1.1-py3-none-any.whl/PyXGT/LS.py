import socket
class plc_ls:
    def  __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn_class = self.connect_init()

    def connect_init(self):
        conn_class = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_class.connect((self.host, self.port))
        return conn_class
    
    def command(self, company_id, request, dtype, headdevice, values = '0'):
        header = makeHeader(company_id)  
        app_instruction = makeInstruction(request, dtype, headdevice, values)
        update_header = updateHeader(header, app_instruction)
        retByte = update_header + app_instruction
        conn_class = self.conn_class
        conn_class.send(retByte)
        count_val = len(headdevice.split(','))
        val_temp = conn_class.recv(1024)
        if request == 'read':
            vals = []
            num = val_temp[30]
            if num > 0:
                for i in range(count_val,0,-1):
                    val = 0
                    j = 1
                    while j<= num:
                        val += val_temp[-j-(i-1)*(num+2)]*16**(2*(num-j))
                        j += 1
                    vals.append(val)
            return vals

def makeHeader(company_id):
    header = bytearray(b'')
    if company_id == 'XGT' or company_id == 'XGB':
        company_header = bytearray(b'LSIS-XGT')
        company_header = company_header + bytearray(b'\x00\x00')
    else:
        company_header = bytearray(b'LGIS-GLOFA')
    plc_header = bytearray(b'\x00\x00')
    cpu_header = bytearray(b'\x00')
    src_frame_header = bytearray(b'\x33')
    invoke_id_header = bytearray(b'\x00\x00')
    header = company_header + plc_header + cpu_header + src_frame_header + invoke_id_header
    return header

def updateHeader(header, app_instruction):
    len_header =  bytes([len(app_instruction), 0])
    fenet_header = bytearray(b'\x00') 
    reserved_header = bytearray(b'\x00') 
    update_header = header + len_header + fenet_header + reserved_header
    return update_header

def makeInstruction(request, dtype, headdevice, values='0'):
    # for find data num & split head device name
    tmp_headdevice = headdevice.split(',') 
    dtype = dtype.lower()
    data_count = len(tmp_headdevice)
    # data type
    if dtype == 'bit':
        dtype_instruction = bytearray(b'\x00\x00')
        dtype_word = bytearray("X",'utf-8')
    elif dtype == 'byte':
        dtype_instruction = bytearray(b'\x01\x00')
        dtype_word = bytearray("B",'utf-8')
    elif dtype == 'word':
        dtype_instruction = bytearray(b'\x02\x00')
        dtype_word = bytearray("W",'utf-8')
    elif dtype == 'dword':
        dtype_instruction = bytearray(b'\x03\x00')
        dtype_word =  bytearray("D",'utf-8')
    elif dtype == 'lword':
        dtype_instruction = bytearray(b'\x04\x00')
        dtype_word = bytearray("L",'utf-8')
    else:
        dtype_instruction = bytearray(b'\x14\x00')
        dtype_word = bytearray("B",'utf-8')

    reserved_instruction = bytearray(b'\x00\x00')
    num_instruction = bytes([data_count, 0])
    data_instructions = bytearray(b'')
    for i in range(data_count):
        data_instruction = bytearray('%','utf-8')
        data_instruction = data_instruction + bytearray(tmp_headdevice[i][0],'utf-8') + dtype_word
        variable_instruction = bytearray(tmp_headdevice[i][1:],'utf-8')
        len_instruction = bytes([len(data_instruction) + len(variable_instruction), 0])
        data_instructions = data_instructions + len_instruction + data_instruction + variable_instruction
    if request == 'read':
        request_instruction = bytearray(b'\x54\x00') # read
        final_instruction = request_instruction + dtype_instruction + reserved_instruction + num_instruction + data_instructions
    else:
        request_instruction = bytearray(b'\x58\x00') # write
        value_instruction = bytearray(b'')
        values = str(values)
        values = values.split(',') 
        for value in values:
            temp_value = mk_value(dtype,int(value))
            value_instruction = value_instruction + temp_value
        final_instruction = request_instruction + dtype_instruction + reserved_instruction + num_instruction + data_instructions + value_instruction
    return final_instruction

def mk_value(dtype,value):
    if dtype == "bit":
        data = bytes([1, 0, value])
    else:
        tempData = hex(int(value))
        part = tempData[2:]
        if len(part) % 2 == 1:
            part = "0" + part
        part2 = swap_pairs(dtype, part)
        data = bytes.fromhex(part2)
    return data
def swap_pairs(dtype, input_string):
    result = ""
    n = len(input_string)
    if dtype == "word":
        num = 4
    elif dtype =="dword":
        num = 8
    elif dtype == "lword":
        num = 16
    else:
        num =2
    if n % num > 0:
        for i in range(num - n % num):
            input_string = "0" + input_string
    n = len(input_string)
    result = "2000"
    for i in range(n - 3, 0, -4):
        result += input_string[i + 1]+ input_string[i + 2]+ input_string[i - 1]+ input_string[i]
    return result