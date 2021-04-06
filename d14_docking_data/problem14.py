from typing import List, Tuple, Union
import re

def parse_input_file(test: int = 0):
    if test == 0 :
        with open("./d14_docking_data/input.txt", 'r') as file:
            lines = file.read().splitlines()
    if test == 1 :
        with open("./d14_docking_data/test_input.txt", 'r') as file:
            lines = file.read().splitlines()
    if test == 2 :
        with open("./d14_docking_data/test_input2.txt", 'r') as file:
            lines = file.read().splitlines()

    instructions = [] # mix of mask and mem instructions
    for l in lines:
        if l[:4] == 'mask':
            # parse mask instruction as string
            instructions.append(l.split('=')[1].strip())

        elif l[:3] == 'mem':
            # parse mem instruction as tuple
            mem_instr = re.search('\[(\d+)\].+?([\d]+)', l)
            addr, val = mem_instr.group(1), mem_instr.group(2)
            instructions.append((addr, val))

    return instructions


class MaskingDict(dict):
    """Extends dict with a binary masking function upon insertion

    Mask can be updated with set_mask method.
    """
    def __init__(self, n_bits: int = 36, *args, **kw,):
        super(MaskingDict, self).__init__(*args, **kw)
        self.mask_OR = int('0'*n_bits, 2) # interpret binary values
        self.mask_AND = int('1'*n_bits, 2)# as base 10
        self.n_bits = n_bits

    # override setitem function to mask value upon insertion
    def __setitem__(self, key, value):
        # modify value, then insert in super dict
        masked_val = value | self.mask_OR
        masked_val = masked_val & self.mask_AND
        super(MaskingDict, self).__setitem__(key, masked_val)

    def set_mask(self, mask):
        mask_OR = ['0' for _ in range(self.n_bits)]
        mask_AND =  ['1' for _ in range(self.n_bits)]
        for i, char in enumerate(mask):
            if char == 'X':
                continue
            if char == '0':
                mask_AND[i] = '0'
            elif char == '1':
                mask_OR[i] = '1'

        self.mask_OR = int(''.join(mask_OR), 2)
        self.mask_AND = int(''.join(mask_AND), 2)

def exec_instructions_part1(instructions: List[Union[Tuple[int], str]]) -> int:
    """Given set of instructions, returns sum of values in memory at termination


    Instructions either update the bitmask or write a value to memory, e.g.:
        - set bitwise mask to the following:
            mask = 001X11X1X010X1X1010XX10X100101011000
        where there's a 0 or a 1, replace inserted value bit with it,
        leave bits unmodified in correspondence of Xs

        - set value at given address (value is masked upon insertion), e.g.:
            mem[43398] = 563312 (mem[addr] = value)

    Args:
        instructions (List[Tuple[int], str]): instructions of insertion or mask update,
            example given above.

    Returns:
        int: sum of values in memory at termination of instruction list.
    """
    masking_dict = MaskingDict()

    for instr in instructions:
        # if instruction is a tuple of two values -> store value at addr
        if isinstance(instr, tuple):
            addr, val = int(instr[0]), int(instr[1])
            masking_dict[addr] = val

        # if it's a mask -> set new mask
        elif isinstance(instr, str):
            masking_dict.set_mask(instr)

    # sum all values at termination
    s = 0
    for val in masking_dict.values():
        s += val
    return s


class MaskingDictV2(dict):
    """Extends dict with a version 2 decoder chip emulation

    Modify values at different addresses as follows:
        - If the bitmask bit is 0, the corresponding memory address bit is unchanged.
        - If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
        - If the bitmask bit is X, the corresponding memory address bit is floating.

    Mask can be updated with set_mask method.
    """
    def __init__(self, n_bits: int = 36, *args, **kw,):
        super(MaskingDictV2, self).__init__(*args, **kw)
        self.mask = '0'*n_bits # initialise mask as not doing anything
        self.n_bits = n_bits

    def fill_leading_zeros(self, binary_n: str):
        return '0'*(self.n_bits - len(binary_n))+binary_n

    def get_addresses_recurse(self, curr_addr: str, curr_mask: str, constructed_addr: str) -> List[str]:
        # given fill_leading zeros, both params have n_bits bits,
        # so consider always [-1] bit of both and shorten both at each step
        # therefore the base case is if they both reach length 0, so the constructed address
        # is the address to be returned

        # Base Case
        if len(curr_addr) == 0:
            assert len(curr_mask) == 0, 'curr_mask has no 0 length while curr_addr does'
            return [constructed_addr]

        if curr_mask[-1] == '0': # address bit unchanged
            new_constr_addr = curr_addr[-1] + constructed_addr
            new_addr = curr_addr[:-1]
            new_mask = curr_mask[:-1]
            return self.get_addresses_recurse(new_addr, new_mask, new_constr_addr)

        elif curr_mask[-1] == '1':
            new_constr_addr = '1' + constructed_addr
            new_addr = curr_addr[:-1]
            new_mask = curr_mask[:-1]
            return self.get_addresses_recurse(new_addr, new_mask, new_constr_addr)

        elif curr_mask[-1] == 'X':
            new_constr_addr_0 = '0' + constructed_addr
            new_constr_addr_1 = '1' + constructed_addr
            new_addr = curr_addr[:-1]
            new_mask = curr_mask[:-1]
            return self.get_addresses_recurse(new_addr, new_mask, new_constr_addr_0) +\
                self.get_addresses_recurse(new_addr, new_mask, new_constr_addr_1)



    # override setitem function to mask address(es) upon insertion
    def __setitem__(self, key, value):
        # get all corresponding addresses, then set values to those addresses
        binary_repr_key = self.fill_leading_zeros(bin(key)[2:]) # fill of 0s until n_bits met
        addresses = self.get_addresses_recurse(binary_repr_key, self.mask, '')
        for addr in addresses:
            super(MaskingDictV2, self).__setitem__(addr, value)

    def set_mask(self, mask):
        self.mask = mask


def exec_instructions_part2(instructions: List[Union[Tuple[int], str]]) -> int:
    """Given set of instructions, returns sum of values in memory at termination


    Instructions either update the bitmask or write a value to memory, e.g.:
        - set bitwise mask to the following:
            mask = 001X11X1X010X1X1010XX10X100101011000
        where there's a 0 or a 1, replace inserted value bit with it,
        leave unmodified bits corresponding to X

        - set value at given address (value is masked upon insertion), e.g.:
            mem[43398] = 563312 (mem[addr] = value)

    Args:
        instructions (List[Tuple[int], str]): instructions of insertion or mask update,
            example given above.

    Returns:
        int: sum of values in memory at termination of instruction list.
    """
    masking_dict = MaskingDictV2()

    for instr in instructions:
        # if instruction is a tuple of two values -> store value at addr
        if isinstance(instr, tuple):
            addr, val = int(instr[0]), int(instr[1])
            masking_dict[addr] = val

        # if it's a mask -> set new mask
        elif isinstance(instr, str):
            masking_dict.set_mask(instr)

    # sum all values at termination
    s = 0
    for val in masking_dict.values():
        s += val
    return s


if __name__ == "__main__":
    instructions = parse_input_file()

    ans1 = exec_instructions_part1(instructions)
    print(ans1)

    instructions = parse_input_file()
    ans2 = exec_instructions_part2(instructions)
    print(ans2)