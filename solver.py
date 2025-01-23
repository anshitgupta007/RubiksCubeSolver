import cube
import hash
import util
import time
import cam
from collections import defaultdict


def ida_star(mycube, lookup_table, solution, stage):
    moves = []
    if stage == 0:
        moves = ["R2", "L2", "U2", "D2", "F2", "B2", "R'", "L'", "U'", "D'", "F'", "B'", "R", "L", "U", "D", "F", "B"]
        initial_hash = hash.hash_stage0(mycube)
    elif stage == 1:
        moves = ["R2", "L2", "U2", "D2", "F2", "B2", "R'", "L'", "F'", "B'", "R", "L", "F", "B"]
        initial_hash = hash.hash_stage1(mycube)
    elif stage == 2:
        moves = ["R2", "L2", "U2", "D2", "F2", "B2", "R'", "L'", "R", "L"]
        initial_hash = hash.hash_stage2(mycube)
    elif stage == 3:
        moves = ["R2", "L2", "U2", "D2", "F2", "B2"]
        initial_hash = hash.hash_stage3(mycube)

    bound = lookup_table.get(initial_hash, float('inf'))  # Initial heuristic

    def search(state, g, bound):
        if stage == 0:
            state_hash = hash.hash_stage0(state)
        elif stage == 1:
            state_hash = hash.hash_stage1(state)
        elif stage == 2:
            state_hash = hash.hash_stage2(state)
        elif stage == 3:
            state_hash = hash.hash_stage3(state)

        h = lookup_table.get(state_hash, float('inf'))  # Heuristic
        f = g + h

        if f > bound:
            return f  # Prune paths exceeding current bound
        if h == 0:
            return -1  # Goal reached

        min_cost = float('inf')
        for move in moves:
            cube.apply_moves(state, move)
            solution.append(move)

            t = search(state, g + 1, bound)
            if t == -1:
                return -1  # Solution found
            if t < min_cost:
                min_cost = t

            solution.pop()
            # Undo the move
            cube.apply_moves(state, move)
            cube.apply_moves(state, move)
            cube.apply_moves(state, move)

        return min_cost

    while True:
        t = search(mycube, 0, bound)
        if t == -1:
            return True  # Solution found
        if t == float('inf'):
            return False  # No solution exists
        bound = t  # Increase the bound

def main():
    mycube = cam.getcube()
    cube.printcube(mycube)
    # Initialize lookup tables
    lookup_table0 = {}
    lookup_table1 = {}
    lookup_table2 = {}
    lookup_table3 = {}

    # Load lookup tables from files
    def load_lookup_table(filename):
        table = {}
        try:
            with open(filename, "r") as file:
                for line in file:
                    hash_val, depth = map(int, line.split())
                    table[hash_val] = depth
        except FileNotFoundError:
            print(f"File {filename} not found.")
        return table

    lookup_table0 = load_lookup_table("G0.txt")
    lookup_table1 = load_lookup_table("G1.txt")
    lookup_table2 = load_lookup_table("G2.txt")
    lookup_table3 = load_lookup_table("G3.txt")

    solution = []
    
    start_time = time.time()

    if ida_star(mycube, lookup_table0, solution, 0):
     
        print()
        print("Stage 0 solved")
    else:
        print("No solution found")

    if ida_star(mycube, lookup_table1, solution, 1):
        print("Stage 1 solved")
    else:
        print("No solution found")

    if ida_star(mycube, lookup_table2, solution, 2):
        print("Stage 2 solved")
    else:
        print("No solution found")

    if ida_star(mycube, lookup_table3, solution, 3):
        print("Stage 3 solved")
        print(f"Solved in {len(solution)} moves")
        print("Solution:", " ".join(solution))
    else:
        print("No solution found")

    cube.printcube(mycube)
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.5f} seconds")

if __name__ == "__main__":
    main()


