# Rubik's cube solver

## Overview
Thistlethwaite's Algorithm is an efficient method for solving the Rubik's Cube by systematically reducing its complexity through five well-defined subgroups (G0 to G4, G4 being the solved state). The original Thistlethwaite's Algorithm requires a maximum of 52 moves a solve however this project uses modified Thistlethwaite algorithm to solve the cube in a maximum of 45 moves.

### **Program Statistics**
- **Average Solve Length:** 30 moves
- **Average Solve Time:** 30 ms

### **Key Features**
- The algorithm splits the problem into smaller, simpler sub-problems (subgroups) that are progressively solved.
- Uses precomputed pattern databases to store possible cube states for efficient computation.
- Ensures that each step simplifies the puzzle while maintaining legality within defined movesets.

---

## Subgroup Transitions

### **G0 → G1**
- **Initial State:** Any scrambled cube (4.33 × 10¹⁹ positions)
- **Target:** Solve edge orientations.
- **Unique States:** 2¹¹ = 2048
- **Legal Moves:** All moves

In G1, the orientation of all 12 edges is corrected such that an edge can be solved without requiring a 90-degree Up or Down move. Only 2¹² / 2 = 2048 unique states are stored in a database, as edge orientation parity ensures that only half of all possible states are reachable.

---

### **G1 → G2**
- **Initial State:** 2.11 × 10¹⁶ positions
- **Target:** Solve M-slice edges and corner orientations.
- **Unique States:** 12C4 × 3⁷ = 1,082,565
- **Legal Moves:** 90-degree Up/Down turns are excluded

In G2, all the M-slice edges are restored to their home slice, and all corners are oriented correctly. Corner orientation states are reduced by their parity constraints (only 3⁸ / 3 states are reachable).

---

### **G2 → G3**
- **Initial State:** 1.95 × 10¹⁰ positions
- **Target:** Solve edges and corners to enable solutions using only 180-degree moves.
- **Unique States:** 8C4² × 2 × 3 = 29,400
- **Legal Moves:** 90-degree Up/Down and Front/Back turns are excluded

In G3, all edges are restricted to their home slices, and all corners are within their natural orbits. Additional factors include parity and restrictions from lone 3-cycles.

---

### **G3 → G4**
- **Initial State:** 6.63 × 10⁵ positions
- **Target:** Fully solve the cube.
- **Unique States:** 4!^2 / 6 × 4!^3 / 2 = 663,552
- **Legal Moves:** Only 180-degree moves are allowed

In this final stage, the cube is separated into 3 edge slices and 2 corner tetrads. Permutations are restricted by parity, preventing certain corner and edge combinations. The total number of states is reduced to 663,552, which are precomputed for database storage.

---

## How It Works
1. **G0:** Start with a scrambled cube.
2. **G1:** Fix edge orientations.
3. **G2:** Restore M-slice edges and correct corner orientations.
4. **G3:** Ensure the cube can be solved using only 180-degree moves.
5. **G4:** Solve the cube completely.
Note - A how to use guide will be attached once the project is fully complete.
---

## Features and Implementation
- **Optimized Subgroup Transitions:** Reduced the maximum solution length to 45 moves (from 52 moves) by refining subgroup transitions.
- **IDA* Algorithm:** Implemented for efficient pathfinding, leveraging heuristic data from pattern databases.
- **State Modeling:** Modeled cube states across 5 subgroups (G0 to G4), with G4 as the solved state, to generate pattern databases.
- **Automated Input:** Utilized OpenCV for capturing and processing Rubik's Cube face images.
- **Efficient Storage:** Optimized state storage using efficient hashing for subgroups:
  - G0: 2048 states
  - G1: 1,082,565 states
  - G2: 29,400 states
  - G3: 663,552 states
- **Performance:** Achieved an average solution of 30 moves with a solve time of 30 ms.

---


## Future Work
- Implement heuristic improvements for even faster solve times.
- Extend the algorithm to handle larger cubes (e.g., 4x4x4, 5x5x5).

---

## References
https://www.jaapsch.net/puzzles/thistle.htm

https://github.com/itaysadeh/rubiks-cube-solver(Help me in understanding G3 state and its implementation)

https://stackoverflow.com/questions/58860280/how-to-create-a-pattern-database-for-solving-rubiks-cube