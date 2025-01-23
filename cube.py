def generate():
    return [
        [0] * 9,
        [1] * 9,
        [2] * 9,
        [3] * 9,
        [4] * 9,
        [5] * 9,
    ]


def apply_moves(cube, move):
    if move == "R":
        # Side face
        temp = cube[1][6]
        cube[1][6], cube[1][8], cube[1][2], cube[1][0] = cube[1][8], cube[1][2], cube[1][0], temp
        temp = cube[1][3]
        cube[1][3], cube[1][7], cube[1][5], cube[1][1] = cube[1][7], cube[1][5], cube[1][1], temp

        # Rest four faces
        temp1 = [cube[0][2], cube[0][5], cube[0][8]]
        cube[0][2], cube[0][5], cube[0][8] = cube[5][2], cube[5][5], cube[5][8]
        cube[5][2], cube[5][5], cube[5][8] = cube[2][6], cube[2][3], cube[2][0]
        cube[2][6], cube[2][3], cube[2][0] = cube[4][2], cube[4][5], cube[4][8]
        cube[4][2], cube[4][5], cube[4][8] = temp1

    elif move == "L":
        # Side face
        temp = cube[3][6]
        cube[3][6], cube[3][8], cube[3][2], cube[3][0] = cube[3][8], cube[3][2], cube[3][0], temp
        temp = cube[3][3]
        cube[3][3], cube[3][7], cube[3][5], cube[3][1] = cube[3][7], cube[3][5], cube[3][1], temp

        # Rest four faces
        temp1 = [cube[0][0], cube[0][3], cube[0][6]]
        cube[0][0], cube[0][3], cube[0][6] = cube[4][0], cube[4][3], cube[4][6]
        cube[4][0], cube[4][3], cube[4][6] = cube[2][8], cube[2][5], cube[2][2]
        cube[2][8], cube[2][5], cube[2][2] = cube[5][0], cube[5][3], cube[5][6]
        cube[5][0], cube[5][3], cube[5][6] = temp1

    elif move == "U":
        # Top face
        temp = cube[4][6]
        cube[4][6], cube[4][8], cube[4][2], cube[4][0] = cube[4][8], cube[4][2], cube[4][0], temp
        temp = cube[4][3]
        cube[4][3], cube[4][7], cube[4][5], cube[4][1] = cube[4][7], cube[4][5], cube[4][1], temp

        # Rest four faces
        temp1 = [cube[0][0], cube[0][1], cube[0][2]]
        cube[0][0], cube[0][1], cube[0][2] = cube[1][0], cube[1][1], cube[1][2]
        cube[1][0], cube[1][1], cube[1][2] = cube[2][0], cube[2][1], cube[2][2]
        cube[2][0], cube[2][1], cube[2][2] = cube[3][0], cube[3][1], cube[3][2]
        cube[3][0], cube[3][1], cube[3][2] = temp1

    elif move == "D":
        # Bottom face
        temp = cube[5][6]
        cube[5][6], cube[5][8], cube[5][2], cube[5][0] = cube[5][8], cube[5][2], cube[5][0], temp
        temp = cube[5][3]
        cube[5][3], cube[5][7], cube[5][5], cube[5][1] = cube[5][7], cube[5][5], cube[5][1], temp

        # Rest four faces
        temp1 = [cube[0][6], cube[0][7], cube[0][8]]
        cube[0][6], cube[0][7], cube[0][8] = cube[3][6], cube[3][7], cube[3][8]
        cube[3][6], cube[3][7], cube[3][8] = cube[2][6], cube[2][7], cube[2][8]
        cube[2][6], cube[2][7], cube[2][8] = cube[1][6], cube[1][7], cube[1][8]
        cube[1][6], cube[1][7], cube[1][8] = temp1

    elif move == "F":
        # Front face
        temp = cube[0][6]
        cube[0][6], cube[0][8], cube[0][2], cube[0][0] = cube[0][8], cube[0][2], cube[0][0], temp
        temp = cube[0][3]
        cube[0][3], cube[0][7], cube[0][5], cube[0][1] = cube[0][7], cube[0][5], cube[0][1], temp

        # Rest four faces
        temp1 = [cube[1][0], cube[1][3], cube[1][6]]
        cube[1][0], cube[1][3], cube[1][6] = cube[4][6], cube[4][7], cube[4][8]
        cube[4][6], cube[4][7], cube[4][8] = cube[3][8], cube[3][5], cube[3][2]
        cube[3][8], cube[3][5], cube[3][2] = cube[5][2], cube[5][1], cube[5][0]
        cube[5][2], cube[5][1], cube[5][0] = temp1
    elif move == "B":
        # back face
        temp = cube[2][6]
        cube[2][6] = cube[2][8]
        cube[2][8] = cube[2][2]
        cube[2][2] = cube[2][0]
        cube[2][0] = temp

        temp = cube[2][3]
        cube[2][3] = cube[2][7]
        cube[2][7] = cube[2][5]
        cube[2][5] = cube[2][1]
        cube[2][1] = temp

        # rest four faces
        temp1 = [cube[1][2], cube[1][5], cube[1][8]]
        cube[1][2] = cube[5][8]
        cube[1][5] = cube[5][7]
        cube[1][8] = cube[5][6]
        cube[5][8] = cube[3][6]
        cube[5][7] = cube[3][3]
        cube[5][6] = cube[3][0]
        cube[3][6] = cube[4][0]
        cube[3][3] = cube[4][1]
        cube[3][0] = cube[4][2]
        cube[4][2] = temp1[2]
        cube[4][1] = temp1[1]
        cube[4][0] = temp1[0]

    elif move == "R'":
        # side face
        temp = cube[1][6]
        cube[1][6] = cube[1][0]
        cube[1][0] = cube[1][2]
        cube[1][2] = cube[1][8]
        cube[1][8] = temp

        temp = cube[1][3]
        cube[1][3] = cube[1][1]
        cube[1][1] = cube[1][5]
        cube[1][5] = cube[1][7]
        cube[1][7] = temp

        # rest four faces
        temp1 = [cube[0][2], cube[0][5], cube[0][8]]
        cube[0][2] = cube[4][2]
        cube[0][5] = cube[4][5]
        cube[0][8] = cube[4][8]
        cube[4][2] = cube[2][6]
        cube[4][5] = cube[2][3]
        cube[4][8] = cube[2][0]
        cube[2][6] = cube[5][2]
        cube[2][3] = cube[5][5]
        cube[2][0] = cube[5][8]
        cube[5][2] = temp1[0]
        cube[5][5] = temp1[1]
        cube[5][8] = temp1[2]

    elif move == "L'":
        # side face
        temp = cube[3][6]
        cube[3][6] = cube[3][0]
        cube[3][0] = cube[3][2]
        cube[3][2] = cube[3][8]
        cube[3][8] = temp

        temp = cube[3][3]
        cube[3][3] = cube[3][1]
        cube[3][1] = cube[3][5]
        cube[3][5] = cube[3][7]
        cube[3][7] = temp

        # rest four faces
        temp1 = [cube[0][0], cube[0][3], cube[0][6]]
        cube[0][0] = cube[5][0]
        cube[0][3] = cube[5][3]
        cube[0][6] = cube[5][6]
        cube[5][0] = cube[2][8]
        cube[5][3] = cube[2][5]
        cube[5][6] = cube[2][2]
        cube[2][8] = cube[4][0]
        cube[2][5] = cube[4][3]
        cube[2][2] = cube[4][6]
        cube[4][0] = temp1[0]
        cube[4][3] = temp1[1]
        cube[4][6] = temp1[2]

    elif move == "U'":
        # top face
        temp = cube[4][6]
        cube[4][6] = cube[4][0]
        cube[4][0] = cube[4][2]
        cube[4][2] = cube[4][8]
        cube[4][8] = temp

        temp = cube[4][3]
        cube[4][3] = cube[4][1]
        cube[4][1] = cube[4][5]
        cube[4][5] = cube[4][7]
        cube[4][7] = temp

        # rest four faces
        temp1 = [cube[0][0], cube[0][1], cube[0][2]]
        cube[0][0] = cube[3][0]
        cube[0][1] = cube[3][1]
        cube[0][2] = cube[3][2]
        cube[3][0] = cube[2][0]
        cube[3][1] = cube[2][1]
        cube[3][2] = cube[2][2]
        cube[2][0] = cube[1][0]
        cube[2][1] = cube[1][1]
        cube[2][2] = cube[1][2]
        cube[1][0] = temp1[0]
        cube[1][1] = temp1[1]
        cube[1][2] = temp1[2]

    elif move == "D'":
        # bottom face
        temp = cube[5][6]
        cube[5][6] = cube[5][0]
        cube[5][0] = cube[5][2]
        cube[5][2] = cube[5][8]
        cube[5][8] = temp

        temp = cube[5][3]
        cube[5][3] = cube[5][1]
        cube[5][1] = cube[5][5]
        cube[5][5] = cube[5][7]
        cube[5][7] = temp

        # rest four faces
        temp1 = [cube[0][6], cube[0][7], cube[0][8]]
        cube[0][6] = cube[1][6]
        cube[0][7] = cube[1][7]
        cube[0][8] = cube[1][8]
        cube[1][6] = cube[2][6]
        cube[1][7] = cube[2][7]
        cube[1][8] = cube[2][8]
        cube[2][6] = cube[3][6]
        cube[2][7] = cube[3][7]
        cube[2][8] = cube[3][8]
        cube[3][6] = temp1[0]
        cube[3][7] = temp1[1]
        cube[3][8] = temp1[2]

    elif move == "F'":
        # front face
        temp = cube[0][6]
        cube[0][6] = cube[0][0]
        cube[0][0] = cube[0][2]
        cube[0][2] = cube[0][8]
        cube[0][8] = temp

        temp = cube[0][3]
        cube[0][3] = cube[0][1]
        cube[0][1] = cube[0][5]
        cube[0][5] = cube[0][7]
        cube[0][7] = temp

        # rest four faces
        temp1 = [cube[1][0], cube[1][3], cube[1][6]]
        cube[1][0] = cube[5][2]
        cube[1][3] = cube[5][1]
        cube[1][6] = cube[5][0]
        cube[5][2] = cube[3][8]
        cube[5][1] = cube[3][5]
        cube[5][0] = cube[3][2]
        cube[3][8] = cube[4][6]
        cube[3][5] = cube[4][7]
        cube[3][2] = cube[4][8]
        cube[4][6] = temp1[0]
        cube[4][7] = temp1[1]
        cube[4][8] = temp1[2]

    elif move == "B'":
        # back face
        temp = cube[2][6]
        cube[2][6] = cube[2][0]
        cube[2][0] = cube[2][2]
        cube[2][2] = cube[2][8]
        cube[2][8] = temp

        temp = cube[2][3]
        cube[2][3] = cube[2][1]
        cube[2][1] = cube[2][5]
        cube[2][5] = cube[2][7]
        cube[2][7] = temp

        # rest four faces
        temp1 = [cube[1][2], cube[1][5], cube[1][8]]
        cube[1][2] = cube[4][0]
        cube[1][5] = cube[4][1]
        cube[1][8] = cube[4][2]
        cube[4][0] = cube[3][6]
        cube[4][1] = cube[3][3]
        cube[4][2] = cube[3][0]
        cube[3][0] = cube[5][6]
        cube[3][3] = cube[5][7]
        cube[3][6] = cube[5][8]
        cube[5][6] = temp1[2]
        cube[5][7] = temp1[1]
        cube[5][8] = temp1[0]

    elif move == "R2":
        # side face
        temp = cube[1][6]
        cube[1][6] = cube[1][2]
        cube[1][2] = temp

        temp = cube[1][7]
        cube[1][7] = cube[1][1]
        cube[1][1] = temp

        temp = cube[1][8]
        cube[1][8] = cube[1][0]
        cube[1][0] = temp

        temp = cube[1][5]
        cube[1][5] = cube[1][3]
        cube[1][3] = temp

        # rest four faces
        temp1 = [cube[0][2], cube[0][5], cube[0][8]]
        cube[0][2] = cube[2][6]
        cube[0][5] = cube[2][3]
        cube[0][8] = cube[2][0]
        cube[2][6] = temp1[0]
        cube[2][3] = temp1[1]
        cube[2][0] = temp1[2]

        temp1 = [cube[4][2], cube[4][5], cube[4][8]]
        cube[4][2] = cube[5][2]
        cube[4][5] = cube[5][5]
        cube[4][8] = cube[5][8]
        cube[5][2] = temp1[0]
        cube[5][5] = temp1[1]
        cube[5][8] = temp1[2]

    elif move == "L2":
        # side face
        temp = cube[3][6]
        cube[3][6] = cube[3][2]
        cube[3][2] = temp
        temp = cube[3][7]
        cube[3][7] = cube[3][1]
        cube[3][1] = temp
        temp = cube[3][8]
        cube[3][8] = cube[3][0]
        cube[3][0] = temp
        temp = cube[3][5]
        cube[3][5] = cube[3][3]
        cube[3][3] = temp

        # rest four faces
        temp1 = [cube[0][0], cube[0][3], cube[0][6]]
        cube[0][0] = cube[2][8]
        cube[0][3] = cube[2][5]
        cube[0][6] = cube[2][2]
        cube[2][8] = temp1[0]
        cube[2][5] = temp1[1]
        cube[2][2] = temp1[2]

        temp1 = [cube[4][0], cube[4][3], cube[4][6]]
        cube[4][0] = cube[5][0]
        cube[4][3] = cube[5][3]
        cube[4][6] = cube[5][6]
        cube[5][0] = temp1[0]
        cube[5][3] = temp1[1]
        cube[5][6] = temp1[2]

    elif move == "U2":
        # top face
        temp = cube[4][6]
        cube[4][6] = cube[4][2]
        cube[4][2] = temp
        temp = cube[4][7]
        cube[4][7] = cube[4][1]
        cube[4][1] = temp
        temp = cube[4][8]
        cube[4][8] = cube[4][0]
        cube[4][0] = temp
        temp = cube[4][5]
        cube[4][5] = cube[4][3]
        cube[4][3] = temp

        # rest four faces
        temp1 = [cube[0][0], cube[0][1], cube[0][2]]
        cube[0][0] = cube[2][0]
        cube[0][1] = cube[2][1]
        cube[0][2] = cube[2][2]
        cube[2][0] = temp1[0]
        cube[2][1] = temp1[1]
        cube[2][2] = temp1[2]

        temp1 = [cube[1][0], cube[1][1], cube[1][2]]
        cube[1][0] = cube[3][0]
        cube[1][1] = cube[3][1]
        cube[1][2] = cube[3][2]
        cube[3][0] = temp1[0]
        cube[3][1] = temp1[1]
        cube[3][2] = temp1[2]

    elif move == "D2":
        # bottom face
        temp = cube[5][6]
        cube[5][6] = cube[5][2]
        cube[5][2] = temp
        temp = cube[5][7]
        cube[5][7] = cube[5][1]
        cube[5][1] = temp
        temp = cube[5][8]
        cube[5][8] = cube[5][0]
        cube[5][0] = temp
        temp = cube[5][5]
        cube[5][5] = cube[5][3]
        cube[5][3] = temp

        # rest four faces
        temp1 = [cube[0][6], cube[0][7], cube[0][8]]
        cube[0][6] = cube[2][6]
        cube[0][7] = cube[2][7]
        cube[0][8] = cube[2][8]
        cube[2][6] = temp1[0]
        cube[2][7] = temp1[1]
        cube[2][8] = temp1[2]

        temp1 = [cube[1][6], cube[1][7], cube[1][8]]
        cube[1][6] = cube[3][6]
        cube[1][7] = cube[3][7]
        cube[1][8] = cube[3][8]
        cube[3][6] = temp1[0]
        cube[3][7] = temp1[1]
        cube[3][8] = temp1[2]

    elif move == "F2":
        # front face
        temp = cube[0][6]
        cube[0][6] = cube[0][2]
        cube[0][2] = temp
        temp = cube[0][7]
        cube[0][7] = cube[0][1]
        cube[0][1] = temp
        temp = cube[0][8]
        cube[0][8] = cube[0][0]
        cube[0][0] = temp
        temp = cube[0][5]
        cube[0][5] = cube[0][3]
        cube[0][3] = temp

        # rest four faces
        temp1 = [cube[1][0], cube[1][3], cube[1][6]]
        cube[1][0] = cube[3][8]
        cube[1][3] = cube[3][5]
        cube[1][6] = cube[3][2]
        cube[3][8] = temp1[0]
        cube[3][5] = temp1[1]
        cube[3][2] = temp1[2]

        temp1 = [cube[4][6], cube[4][7], cube[4][8]]
        cube[4][6] = cube[5][2]
        cube[4][7] = cube[5][1]
        cube[4][8] = cube[5][0]
        cube[5][2] = temp1[0]
        cube[5][1] = temp1[1]
        cube[5][0] = temp1[2]

    elif move == "B2":
        # back face
        temp = cube[2][6]
        cube[2][6] = cube[2][2]
        cube[2][2] = temp
        temp = cube[2][7]
        cube[2][7] = cube[2][1]
        cube[2][1] = temp
        temp = cube[2][8]
        cube[2][8] = cube[2][0]
        cube[2][0] = temp
        temp = cube[2][5]
        cube[2][5] = cube[2][3]
        cube[2][3] = temp

        # rest four faces
        temp1 = [cube[1][2], cube[1][5], cube[1][8]]
        cube[1][2] = cube[3][6]
        cube[1][5] = cube[3][3]
        cube[1][8] = cube[3][0]
        cube[3][6] = temp1[0]
        cube[3][3] = temp1[1]
        cube[3][0] = temp1[2]

        temp1 = [cube[4][0], cube[4][1], cube[4][2]]
        cube[4][0] = cube[5][8]
        cube[4][1] = cube[5][7]
        cube[4][2] = cube[5][6]
        cube[5][8] = temp1[0]
        cube[5][7] = temp1[1]
        cube[5][6] = temp1[2]
def num2color(num):
    if num == 0:
        return 'W'
    if num == 1:
        return 'G'
    if num == 2:
        return 'Y'
    if num == 3:
        return 'B'
    if num == 4:
        return 'R'
    if num == 5:
        return 'O'

def printcube(cube):
    print("Front Face   ", "Right Face   ", "Back Face    ", "Left Face    ", "Top Face     ", "Bottom Face   ")
    for i in range(54):
        k = (i // 3) % 6
        r = i // 18
        if i != 0 and i % 18 == 0:
            print()
        print(num2color(cube[k][3 * r + i % 3]), end=" ")
        if i % 3 == 2:
            print("       ", end="")

