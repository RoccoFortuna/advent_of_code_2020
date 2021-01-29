from typing import List, Tuple


def parse_input_file():
    input_path = "./d8_handheld_halting/input.txt"
    with open(input_path, "r") as file:
        lines = file.read().strip().split("\n")

    instructions = []
    for line in lines:
        instr, arg = line.split()
        instructions.append((instr, int(arg)))

    return instructions


def exec_instr(instrs: List[Tuple[str, int]], i: int, acc: int) -> Tuple[int, int]:
    """execute instruction at index i

    possible instructions are:
        - acc: increases or decreases a single global value
            called the accumulator (acc) by the value given
            in the argument. Instruction immediately after is
            executed next, so index i increases by 1.
        - jmp: jumps to a new instruction relative to itself.
            The next instruction to execute is found using the
            argument as an offset from the jmp instruction;
        - nop: No OPeration - it does nothing. The instruction
            immediately below it is executed next, so index i
            increases by 1.

    Args:
        instrs (List[Tuple[str, int]]): contains tuples with first value
            in ['nop', 'jmp', 'acc'] and second value the argument of
            the instruction.
        i (int): index of instruction to execute
        acc (int): current value of accumulator.

    Returns:
        Tuple[int, int]: pair of new index and new accumulator value.
    """
    curr_instr = instrs[i]
    if curr_instr[0] == "nop":
        return (i+1, acc)

    elif curr_instr[0] == "jmp":
        return (i+curr_instr[1], acc)

    elif curr_instr[0] == "acc":
        return (i+1, acc+curr_instr[1])

    else:
        print("whoooooops this command doesn't exist...")


def find_instrs_loop(instrs: List[Tuple[str, int]]) -> int:
    """Given instructions, starting from idx 0, finds instr loop

    Instruction loop occurs when the same instruction is executed
    a second time. (i.e. an instruction at the same index as one
    previously executed)

    Args:
        instrs (List[Tuple[str, int]]): instructions as tuples of
            command and argument. Instruction strings are
            in ['nop', 'jmp', 'acc'].

    Returns:
        int: the acc value at loop occurrence.
    """
    i = 0
    acc = 0
    idx_executed = set()
    while i < len(instrs):
        if i in idx_executed:
            break # before already exec instr is eec again
        # otherwise keep going and keep track of exec instrs
        idx_executed.add(i)
        i, acc = exec_instr(instrs, i, acc)

    return acc


def find_loop_instr_fix(instrs: List[Tuple[str, int]], i, acc, replaced: bool, instrs_seen: set) -> Tuple[bool, int]:
    """Given instructions, starting from idx 0, finds instr loop

    Instruction loop occurs when the same instruction is executed
    a second time. (i.e. an instruction at the same index as one
    previously executed)

    Args:
        instrs (List[Tuple[str, int]]): instructions as tuples of
            command and argument.

    Returns:
        int: the acc value at loop occurrence
    """
    # base case: correct termination
    if i == len(instrs):
        return True, acc # we had a run that terminates correctly
    # base case2: incorrect termination, went over last line + 1
    elif i > len(instrs):
        return False, -1
    # base case3: looped instruction, terminate
    elif i in instrs_seen:
        return False, -1

    #### Execute instructions
    instrs_seen.add(i)

    ## WithOut Swapping (wos)
    wos_i, wos_acc = exec_instr(instrs, i, acc)
    not_swapping = find_loop_instr_fix(instrs, wos_i, wos_acc, replaced, instrs_seen)

    if not_swapping[0]:
        return not_swapping

    # if instruction is jmp or nop, try the swap
    if instrs[i][0] in ['jmp', 'nop'] and not replaced: # if we haven't replaced yet
        # replace instruction
        instrs[i] = ('jmp' if instrs[i][0]=='nop' else 'nop', instrs[i][1]) # modify only instr command, not param
        ws_i, ws_acc = exec_instr(instrs, i, acc)
        swapping = find_loop_instr_fix(instrs, ws_i, ws_acc, True, instrs_seen) # set replaced to true, can't replace twice
        if swapping[0]:
            return swapping
        instrs[i] = ('jmp' if instrs[i][0]=='nop' else 'nop', instrs[i][1]) # revert change for future recursions

    instrs_seen.remove(i)
    return False, -1


if __name__ == "__main__":
    instrs = parse_input_file()
    ans1 = find_instrs_loop(instrs)
    print(ans1)

    ans2 = find_loop_instr_fix(instrs, 0, 0, False, set())[1]
    print(ans2)