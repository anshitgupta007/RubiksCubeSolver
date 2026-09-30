def getcolor(cube, i):
    f = i // 100000
    e = (i // 10000) % 10
    d = (i // 1000) % 10
    c = (i // 100) % 10
    b = (i // 10) % 10
    a = i % 10

    colors = [cube[f][e], cube[d][c], cube[b][a]]
    colors.sort()
    return colors[0] * 100 + colors[1] * 10 + colors[2]
def imitate_move(move, tetrads_perm):
    indices = []
    positions = [-1] * 4  # Initialize positions to avoid undefined behavior

    # Map the move to the corresponding indices
    if move == "U2":
        indices = [0, 6, 1, 7]
    elif move == "D2":
        indices = [2, 4, 3, 5]
    elif move == "L2":
        indices = [0, 2, 1, 3]
    elif move == "R2":
        indices = [4, 6, 5, 7]
    elif move == "F2":
        indices = [2, 6, 1, 5]
    elif move == "B2":
        indices = [0, 4, 3, 7]
    else:
        raise ValueError(f"Invalid move: {move}")

    # Find the positions of the affected indices
    for i in range(8):
        for j in range(4):
            if tetrads_perm[i] == indices[j] and positions[j] == -1:
                positions[j] = i
                break

    # Perform swaps to simulate the move
    tetrads_perm[positions[0]], tetrads_perm[positions[1]] = (
        tetrads_perm[positions[1]],
        tetrads_perm[positions[0]],
    )
    tetrads_perm[positions[2]], tetrads_perm[positions[3]] = (
        tetrads_perm[positions[3]],
        tetrads_perm[positions[2]],
    )

def hash_stage0(cube):
    # Edges represented as compressed positions
    reqedgelist = [2757, 2533, 2315, 2141, 147, 335, 513, 751, 4331, 4511, 5337, 5517]

    num = 0

    for i in reqedgelist:
        a = i % 10
        b = (i // 10) % 10
        c = (i // 100) % 10
        d = i // 1000

        # Bounds checking
        if d >= len(cube) or c >= len(cube[d]) or b >= len(cube) or a >= len(cube[b]):
            raise IndexError("Invalid edge index in reqedgelist")

        num = num << 1  # Shift left to make space for the new bit

        # Determine edge orientation
        if cube[d][c] in {1, 3}:
            num = num | 1
        elif cube[d][c] in {4, 5}:
            if cube[b][a] in {0, 2}:
                num = num | 1
            else:
                num = num | 0
        else:
            num = num | 0

    return num
def hash_stage1(cube):
    # Corners represented as compressed positions
    reqcornerlist = [302240, 122042, 100248, 320046, 362856, 182658, 160852, 380650]
    reqedgelist = [2757, 2533, 2315, 2141, 147, 335, 513, 751, 4331, 4511, 5337, 5517]
    reqedgescolor = [42, 40, 52, 50]

    num = 0  # Use int in Python; handles large integers

    # Process corners
    for i in reqcornerlist:
        f = (i // 100000)
        e = (i // 10000) % 10
        d = (i // 1000) % 10
        c = (i // 100) % 10

        if cube[f][e] in {1, 3}:
            orientation = 0
        elif cube[d][c] in {1, 3}:
            orientation = 1
        else:
            orientation = 2

        num = (num << 2) | orientation  # Pack 2 bits for each corner

    # Process edges
    for i in reqedgelist:
        color = cube[i // 1000][(i // 100) % 10] * 10 + cube[(i // 10) % 10][i % 10]

        # Determine edge orientation
        matches = any(
            color == rc or (color % 10) * 10 + (color // 10) == rc
            for rc in reqedgescolor
        )

        num = (num << 1) | (0 if matches else 1)  # Pack 1 bit for each edge

    return num


def hash_stage2(cube):
    reqcornerlist = [302240, 320046, 380650, 362856, 182658, 160852, 100248, 122042]
    color = [234, 34, 35, 235, 125, 15, 14, 124]
    reqedgelist = [2757, 2533, 2315, 2141, 147, 335, 513, 751, 4331, 4511, 5337, 5517]
    reqedgescolor = [43, 41, 53, 51]
    num = 0
    actual = [-1] * 8
    k = 0

    # Process corners
    for i in reqcornerlist:
        value = getcolor(cube, i)
        for j in range(8):
            if value == color[j]:
                actual[k] = j
                k += 1
                break

    # Process corner parity
    for i in range(8):
        if actual[i] % 2 == 0:
            num = (num << 1) | 1
        else:
            num = (num << 1) | 0

    # Process edges
    for i in reqedgelist:
        edge_color = cube[i // 1000][(i // 100) % 10] * 10 + cube[(i // 10) % 10][i % 10]
        matches = any(
            edge_color == color or (edge_color % 10) * 10 + (edge_color // 10) == color
            for color in reqedgescolor
        )
        num = (num << 1) | (0 if matches else 1)

    # Additional setup for tetrad operations
    even_tetrad_solving_moves = [["U2", "L2", "B2"], ["D2", "F2"], ["R2"]]
    odd_tetrad_solving_moves = [
        ["F2", "L2", "F2", "U2"],
        ["U2", "F2", "U2", "L2"],
        ["L2", "U2", "L2", "F2"],
    ]

    c_pos_comb = [0] * 4
    c_e_tetrad, c_o_tetrad = [], []
    c_tetrads_perm = [0] * 8
    c_map = [0, 2, 4, 6, 1, 3, 5, 7]

    # Group corners into even and odd tetrads
    for i in range(8):
        if actual[c_map[i]] % 2 == 0:
            c_pos_comb.append(i + 1)
        if actual[i] % 2 == 0:
            c_e_tetrad.append(actual[i])
        else:
            c_o_tetrad.append(actual[i])

    for i in range(8):
        c_tetrads_perm[i] = (
            c_o_tetrad[i // 2] if i % 2 else c_e_tetrad[i // 2]
        )

    # Solve even tetrads
    for i in range(0, 6, 2):
        if c_tetrads_perm[i] == i:
            continue
        for move in even_tetrad_solving_moves[i // 2]:
            imitate_move(move, c_tetrads_perm)
            if c_tetrads_perm[i] == i:
                break
            imitate_move(move, c_tetrads_perm)

    # Solve one corner in the odd tetrad
    move_sequence = 0
    while c_tetrads_perm[1] != 1:
        for move in odd_tetrad_solving_moves[move_sequence]:
            imitate_move(move, c_tetrads_perm)
        if c_tetrads_perm[1] == 1:
            break
        for move in reversed(odd_tetrad_solving_moves[move_sequence]):
            imitate_move(move, c_tetrads_perm)
        move_sequence += 1

    # Store the permutation of remaining corners in the odd tetrad
    c_tetrad_twist = [
        (c_tetrads_perm[3] // 2) - 1,
        (c_tetrads_perm[5] // 2) - 1,
        (c_tetrads_perm[7] // 2) - 1,
    ]
    for twist in c_tetrad_twist:
        num = (num << 2) | twist

    return num
def hash_stage3(cube):
    reqcornerlist = [302240, 320046, 380650, 362856, 182658, 160852, 100248, 122042]
    color = [234, 34, 35, 235, 125, 15, 14, 124]
    E_slice = [147, 751, 2141, 2757]
    E_color = [42, 40, 52, 50]
    S_slice = [4331, 4511, 5337, 5517]
    S_color = [43, 41, 53, 51]
    M_slice = [335, 513, 2315, 2533]
    M_color = [30, 10, 21, 23]
    
    # Process corners
    actual = [-1] * 8
    k = 0
    for i in reqcornerlist:
        value = getcolor(cube, i)
        for j in range(8):
            if value == color[j]:
                actual[k] = j
                k += 1
                break
    
    num = 0
    # Process corner positions
    for i in range(0, 8, 2):
        num = (num << 2) | (actual[i] // 2)
    for i in range(1, 8, 2):
        num = (num << 2) | (actual[i] // 2)

    # Process E slice
    for i in range(4):
        edge_color = cube[E_slice[i] // 1000][(E_slice[i] // 100) % 10] * 10 + cube[(E_slice[i] // 10) % 10][E_slice[i] % 10]
        for j in range(4):
            if edge_color == E_color[j] or (edge_color % 10) * 10 + (edge_color // 10) == E_color[j]:
                num = (num << 2) | j
                break

    # Process S slice
    for i in range(4):
        edge_color = cube[S_slice[i] // 1000][(S_slice[i] // 100) % 10] * 10 + cube[(S_slice[i] // 10) % 10][S_slice[i] % 10]
        for j in range(4):
            if edge_color == S_color[j] or (edge_color % 10) * 10 + (edge_color // 10) == S_color[j]:
                num = (num << 2) | j
                break

    # Process M slice
    for i in range(4):
        edge_color = cube[M_slice[i] // 1000][(M_slice[i] // 100) % 10] * 10 + cube[(M_slice[i] // 10) % 10][M_slice[i] % 10]
        for j in range(4):
            if edge_color == M_color[j] or (edge_color % 10) * 10 + (edge_color // 10) == M_color[j]:
                num = (num << 2) | j
                break

    return num
