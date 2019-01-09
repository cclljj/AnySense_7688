def scaler(data_dict):
    if data_dict['s_t0'] >= -20 and data_dict['s_t0'] <= 80:
        data_dict['s_t0'] = round(data_dict['s_t0'], 1)
        data_dict['s_t0'] = int((data_dict['s_t0'] + 20) * 10)
    else:
        data_dict['s_t0'] = 0
    if data_dict['s_h0'] < 0 or data_dict['s_h0'] > 100:
        data_dict['s_h0'] = 0
    if data_dict['s_d0'] < 0 or data_dict['s_d0'] > 1023:
        data_dict['s_d0'] = 0
    if data_dict['s_d1'] < 0 or data_dict['s_d1'] > 1023:
        data_dict['s_d1'] = 0
    if data_dict['s_d2'] < 0 or data_dict['s_d2'] > 1023:
        data_dict['s_d2'] = 0
    if data_dict['s_g8'] < 0 or data_dict['s_g8'] > 8191:
        data_dict['s_g8'] = 0
    if data_dict['s_lr'] < 0 or data_dict['s_lr'] > 65535:
        data_dict['s_lr'] = 0
    if data_dict['s_lg'] < 0 or data_dict['s_lg'] > 65535:
        data_dict['s_lg'] = 0
    if data_dict['s_lb'] < 0 or data_dict['s_lb'] > 65535:
        data_dict['s_lb'] = 0
    if data_dict['s_lc'] < 0 or data_dict['s_lc'] > 65535:
        data_dict['s_lc'] = 0
    return data_dict

def dec_to_binstr(data_dict):
    T1_name = ['type', 's_t0', 's_h0', 's_b0', 's_d0', 's_d1', 's_d2']
    T2_name = ['type', 's_g8', 's_gg', 's_lr', 's_lg', 's_lb', 's_lc']

    Type1 = {'type': bin(1), 's_t0': bin(0), 's_h0': bin(0), 's_b0': bin(0), 's_d0': bin(0), 's_d1': bin(0), 's_d2': bin(0)}
    Type2 = {'type': bin(2), 's_g8': bin(0), 's_gg': bin(0), 's_lr': bin(0), 's_lg': bin(0), 's_lb': bin(0), 's_lc': bin(0)}

    for name, data in data_dict.items():
        if name in T1_name:
            Type1[name] = bin(data_dict[name])
        elif name in T2_name:
            Type2[name] = bin(data_dict[name])
    
    for bin_num in Type1:
        Type1[bin_num] = Type1[bin_num].replace("0b", "")
        if bin_num == 'type':
            Type1[bin_num] = Type1[bin_num].zfill(4)
        else:
            Type1[bin_num] = Type1[bin_num].zfill(10)
    for bin_num in Type2:
        Type2[bin_num] = Type2[bin_num].replace("0b", "")
        if bin_num == 'type':
            Type2[bin_num] = Type2[bin_num].zfill(4)
        elif bin_num == 's_g8' or bin_num == 's_gg':
            Type2[bin_num] = Type2[bin_num].zfill(13)
        else:
            Type2[bin_num] = Type2[bin_num].zfill(16)
            
    T1_binstr = ""
    T2_binstr = ""
    for name in T1_name:
        T1_binstr = T1_binstr + Type1[name] 

    for name in T2_name:
        T2_binstr = T2_binstr + Type2[name]
    T1_binstr += (96 - len(T1_binstr)) * "0"
    T2_binstr += (96 - len(T2_binstr)) * "0"
        # T1_binstr = T1_binstr + "00000000000000000000000000000000"
        # T2_binstr = T2_binstr + "00"
   	return T1_binstr, T2_binstr

def bin_to_hex(value):
    hex_map = {	"0000": "0",
                "0001": "1",
                "0010": "2",
                "0011": "3",
                "0100": "4",
                "0101": "5",
                "0110": "6",
                "0111": "7",
                "1000": "8",
                "1001": "9",
                "1010": "A",
                "1011": "B",
                "1100": "C",
                "1101": "D",
                "1110": "E",
                "1111": "F"
                }
    i = 0
    output = ""
    while (i < len(value)):
        output = output + hex_map[value[i:i + 4]]
        i = i + 4
    return output
