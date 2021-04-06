def parse_input_file(test: int = 0):
    if test:
        with open(f"./d25_combo_breaker/test_input{test}.txt", 'r') as f:
            card_pk = f.readline()
            door_pk = f.readline()
    else:
        with open("./d25_combo_breaker/input.txt", 'r') as f:
            card_pk = f.readline()
            door_pk = f.readline()

    return int(card_pk), int(door_pk)


def get_loopsize(pk: int, subj_num: int = 7, mod: int = 20201227) -> int:
    val = 1
    loop_size = 0
    while val != pk:
        val = val * subj_num
        val = val % mod
        loop_size += 1
    return loop_size

def transform(pk_subj_num: int, loop_size: int, mod: int = 20201227) -> int:
    val = 1
    for _ in range(loop_size):
        val = val * pk_subj_num
        val = val % mod
    return val


def get_hs_enc_key(card_pk: int, door_pk: int):
    card_loopsize = get_loopsize(card_pk)
    door_loopsize = get_loopsize(door_pk)

    enc_key1 = transform(card_pk, door_loopsize)
    enc_key2 = transform(door_pk, card_loopsize)
    assert enc_key1 == enc_key2, f"enc_keys found were different: {enc_key1} / {enc_key2}"

    return enc_key1


if __name__ == "__main__":
    card_pk, door_pk = parse_input_file(test=0)

    ans1 = get_hs_enc_key(card_pk, door_pk)
