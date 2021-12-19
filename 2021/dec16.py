from math import prod

def hex_to_bits(hex_str):
    return ''.join([f'{int(ch,16):0>4b}' for ch in hex_str])


def get_version(as_bits, start_index=0):
    return int(as_bits[start_index:start_index+3], 2)


def get_type_id(as_bits, start_index=0):
    return int(as_bits[start_index+3:start_index+6], 2)


def get_literal(as_bits, start_index=0):  # returns the bitstring and the int value
    chunk_pointer = start_index
    relevant_bits = ''
    while as_bits[chunk_pointer] == '1':
        relevant_bits += as_bits[chunk_pointer+1:chunk_pointer+5]
        chunk_pointer += 5
    relevant_bits += as_bits[chunk_pointer+1:chunk_pointer+5]
    return (as_bits[start_index:chunk_pointer+5], int(relevant_bits,2))


def get_entire_packet(bit_str, start_index):
    version = get_version(bit_str, start_index)
    type_id = get_type_id(bit_str, start_index)
    if type_id == 4:
        prefix = bit_str[start_index:start_index + 6]
        return prefix + get_literal(bit_str, start_index+6)[0]
    else:
        i_index = start_index + 6
        prefix_end = i_index + (12 if bit_str[i_index] == '1' else 16)
        prefix = bit_str[start_index:prefix_end]
        return prefix + get_sub_packets_str(bit_str, i_index) 


def get_sub_packets_str(as_bits, i_index=6):
    i = as_bits[i_index]
    if i == '0':
        sub_packet_bits = int(as_bits[i_index+1:i_index+16] ,2)
        return as_bits[i_index+16:i_index+16+sub_packet_bits]
    else:  # i == 1
        num_sub_packets = int(as_bits[i_index+1:i_index+12],2)
        sub_packet_bits = ''
        for p in range(num_sub_packets):
            sub_packet_bits += get_entire_packet(as_bits, i_index + 12 + len(sub_packet_bits))
        return sub_packet_bits


def packets_str_to_packets(as_bits):
    consumed = 0
    result = []
    while consumed < len(as_bits) and '1' in as_bits[consumed:]:
        packet = get_entire_packet(as_bits, consumed)
        result.append(packet)
        consumed += len(packet)
    return result


def recursively_total_versions(bit_str):
    vtot = get_version(bit_str)
    type_id = get_type_id(bit_str)
    if type_id == 4:
        return vtot
    else:
        for packet in packets_str_to_packets(get_sub_packets_str(bit_str)):
            vtot += recursively_total_versions(packet)
    return vtot


def evaluate(bit_str):
    type_id = get_type_id(bit_str)
    if type_id == 4:
        return get_literal(bit_str, 6)[1] 

    packets = packets_str_to_packets(get_sub_packets_str(bit_str))

    if type_id == 0:
        return sum([evaluate(sub_packet) for sub_packet in packets])
    elif type_id == 1:
        return prod([evaluate(sub_packet) for sub_packet in packets])
    elif type_id == 2:
        return min([evaluate(sub_packet) for sub_packet in packets])
    elif type_id == 3:
        return max([evaluate(sub_packet) for sub_packet in packets])
    elif type_id == 5:       
        return 1 if evaluate(packets[0]) > evaluate(packets[1]) else 0
    elif type_id == 6:
        return 1 if evaluate(packets[0]) < evaluate(packets[1]) else 0
    else:
        return 1 if evaluate(packets[0]) == evaluate(packets[1]) else 0

with open("dec16in.txt") as in_file:
    in_str = in_file.readline().strip()

as_bits = hex_to_bits(in_str)
rtv = recursively_total_versions(as_bits)
print(f'Total versions: {rtv}')
print(evaluate(as_bits))

# test = 'D2FE28'
# as_bits = hex_to_bits(test)
# type_id = get_type_id(as_bits)
# lit = get_literal(as_bits, 6)[1]
# print(lit)
# print(f'Total versions: {recursively_total_versions(as_bits)}')
# test = '38006F45291200'
# as_bits = hex_to_bits(test)
# type_id = get_type_id(as_bits)
# pstr = get_sub_packets_str(as_bits)
# print(pstr)
# packets = packets_str_to_packets(pstr)
# print(f'{len(packets)} packets')
# print(f'Total versions: {recursively_total_versions(as_bits)}')
# test = 'EE00D40C823060'
# as_bits = hex_to_bits(test)
# type_id = get_type_id(as_bits)
# pstr = get_sub_packets_str(as_bits)
# print(pstr)
# packets = packets_str_to_packets(pstr)
# print(f'{len(packets)} packets')
# print(f'Total versions: {recursively_total_versions(as_bits)}')

# rtv = recursively_total_versions(hex_to_bits('8A004A801A8002F478'))
# print(f'Total versions: {rtv}')
# rtv = recursively_total_versions(hex_to_bits('620080001611562C8802118E34'))
# print(f'Total versions: {rtv}')
# rtv = recursively_total_versions(hex_to_bits('C0015000016115A2E0802F182340'))
# print(f'Total versions: {rtv}')
# rtv = recursively_total_versions(hex_to_bits('A0016C880162017C3686B18A3D4780'))
# print(f'Total versions: {rtv}')

# print(evaluate(hex_to_bits('C200B40A82')))
# b = hex_to_bits('04005AC33890')
# print(evaluate(b))
# print(evaluate(hex_to_bits('880086C3E88112')))
# print(evaluate(hex_to_bits('CE00C43D881120')))

# print(evaluate(hex_to_bits('D8005AC2A8F0')))
# print(evaluate(hex_to_bits('F600BC2D8F')))
# print(evaluate(hex_to_bits('9C005AC2F8F0')))
# print(evaluate(hex_to_bits('9C0141080250320F1802104A08')))

# exit()