from typing import List, Dict


def parse_input_file() -> List[Dict[str, str]]:
    input_path = "./d4_passport_processing/input.txt"
    with open(input_path, "r") as file:
        passports_str = file.read().strip().split("\n\n")
        passports = []
        for passport_str in passports_str:
            passport_str = passport_str.replace('\n', ' ') # remove newlines and replace with space for split
            new_passport = {field.split(':')[0]:field.split(':')[1] for field in passport_str.split()}
            passports.append(new_passport)
    return passports


def validate_passports1(passports: List[Dict[str, str]]) -> int:
    """Count number of valid passports

    Valid passports have all required fields:
        'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'.

        'cid' is optional.

    Args:
        passports (List[Dict[str: str]]): contains dict where key is
            a passport field and value its str value.

    Returns:
        int: number of valid passports
    """
    valid_passports_count = 0
    for passport in passports:
        if is_valid_passport1(passport):
            valid_passports_count += 1

    return valid_passports_count

def is_valid_passport1(passport: Dict[str, str]) -> bool:
    """Check if given passport is valid

    Valid passports have all required fields:
        'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'.

        'cid' is optional.


    Args:
        passports (Dict[str: str]): key is a passport field
            and value its str value.

    Returns:
        bool: if given passport is valid
    """
    required_fields = {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}
    for f in required_fields:
        if passport.get(f, None) is None:
            return False
    return True



def validate_passports2(passports: List[Dict[str, str]]) -> int:
    """Count number of valid passports

    Valid passports have all required fields:
        'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'.

        'cid' is optional.

    Moreover,
        byr (Birth Year) - four digits; at least 1920 and at most 2002.
        iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
        hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        pid (Passport ID) - a nine-digit number, including leading zeroes.
        cid (Country ID) - ignored, missing or not.


    Args:
        passports (List[Dict[str: str]]): contains dict where key is
            a passport field and value its str value.

    Returns:
        int: number of valid passports
    """
    valid_passports_count = 0
    for passport in passports:
        if is_valid_passport2(passport):
            valid_passports_count += 1

    return valid_passports_count

def is_valid_passport2(passport: Dict[str, str]) -> bool:
    """Check if given passport is valid

    Valid passports have all required fields:
        'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'.

        'cid' is optional.

    Moreover,
        byr (Birth Year) - four digits; at least 1920 and at most 2002.
        iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
        hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        pid (Passport ID) - a nine-digit number, including leading zeroes.
        cid (Country ID) - ignored, missing or not.


    Args:
        passports (Dict[str: str]): key is a passport field
            and value its str value.

    Returns:
        bool: if given passport is valid
    """
    required_fields = ['ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt']
    for field in required_fields:
        value = passport.get(field, None)
        if value is None or not is_valid_field(field, value):
            return False

    return True

def is_valid_field(field: str, value: str) -> bool:
    """Checks whether a value is valid for a given field

    Simple case distinction. Rather long, given the number
    of cases and specific way to handle each.

    Args:
        field (str): given field to check validity of value against
        value (str): value associated to given field

    Returns:
        bool: whether value is valid for given field
    """
    if field == 'byr': # (Birth Year) - four digits; at least 1920 and at most 2002.
        return len(value) == 4 and int(value) >= 1920 and int(value) <= 2002

    elif field == 'iyr': # (Issue Year) - four digits; at least 2010 and at most 2020.
        return len(value) == 4 and int(value) >= 2010 and int(value) <= 2020

    elif field == 'eyr': # (Expiration Year) - four digits; at least 2020 and at most 2030.
        return len(value) == 4 and int(value) >= 2020 and int(value) <= 2030

    elif field == 'hgt': # (Height) - a number followed by either cm or in:
        value, unit = value[:-2], value[-2:]
        if unit == 'cm': #If cm, the number must be at least 150 and at most 193.
            return int(value) >= 150 and int(value) <= 193

        if unit == 'in': # If in, the number must be at least 59 and at most 76.
            return int(value) >= 59 and int(value) <= 76
        else:
            return False

    elif field == 'hcl': # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        return value[0] == '#' and len(value[1:]) == 6 and (value[1:].isnumeric() or (value[1:].islower() and value[1:].isalnum()))

    elif field == 'ecl': # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        return value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    elif field == 'pid': # pid (Passport ID) - a nine-digit number, including leading zeroes.
        return len(value) == 9 and value.isnumeric()

    elif field == 'cid': # cid (Country ID) - ignored, missing or not.
        return True
    else:
        print(f"Unknown field: {field}\twith value: {value}")

if __name__ == "__main__":
    passports = parse_input_file()
    ans1 = validate_passports1(passports)
    print(ans1)

    ans2 = validate_passports2(passports)
    print(ans2)