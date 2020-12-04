import re

HEX_PAT = re.compile('^#[0-9|a-f]{6}$')
def is_hex(s):
    m = re.match(HEX_PAT, s)
    return m is not None

def is_valid_pport(pport):
    req_keys = {'byr','eyr','iyr','hgt','hcl','ecl','pid'}
    for key in req_keys:
        if key not in pport:
            return False

    try:
        if not 1920 <= int(pport['byr']) <= 2002:
            return False
        if not 2010 <= int(pport['iyr']) <= 2020:
            return False
        if not 2020 <= int(pport['eyr']) <= 2030:
            return False
        units = pport['hgt'][-2:]
        if units == 'cm':
            if not 150 <= int(pport['hgt'][:-2]) <= 193:
                return False
        elif units == 'in':
            if not 59 <= int(pport['hgt'][:-2]) <= 76:
                return False
        else:
            return False
        if not is_hex(pport['hcl']):
            return False
        if not pport['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            return False
        if not (len(pport['pid']) == 9 and pport['pid'].isnumeric()):
            return False
    except:
        return False

    return True

def read_input():
    valid_pports = []
    invalid_pports = []

    with open("dec04in.txt") as in_file:

        pport = dict()

        for line in in_file:
            line = line.strip()
            if len(line) == 0:
                if is_valid_pport(pport):
                    valid_pports.append(pport) 
                else:
                    invalid_pports.append(pport)
                pport = dict()
                continue

            for part in line.split(' '):
                k,v = part.split(':')
                pport[k] = v

        if is_valid_pport(pport):
            valid_pports.append(pport) 
        else:
            invalid_pports.append(pport)

    return (valid_pports, invalid_pports)

v_passports, i_passports = read_input()
print(f"There were {len(v_passports)} valid, and {len(i_passports)} invalid passports")
