import math
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpInteger


def read_tsplib(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    coords = []
    in_node_section = False
    for line in lines:
        if "NODE_COORD_SECTION" in line:
            in_node_section = True
            continue
        if "EOF" in line:
            break
        if in_node_section:
            parts = line.strip().split()
            if len(parts) >= 3:
                coords.append((float(parts[1]), float(parts[2])))
    return coords

def euclidean_distance(c1, c2):
    return round(math.hypot(c1[0] - c2[0], c1[1] - c2[1]))

def generate_distance_matrix(coords):
    n = len(coords)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = euclidean_distance(coords[i], coords[j])
    return dist

def generate_lp_file(dist, filename="tsp_model.lp"):
    n = len(dist)
    with open(filename, 'w') as f:
        # Objective
        f.write("min: ")
        terms = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    terms.append(f"{dist[i][j]} x{i+1}_{j+1}")
        f.write(" + ".join(terms) + ";\n\n")

        # Constraints: one outgoing edge per node
        for i in range(n):
            cons = [f"x{i+1}_{j+1}" for j in range(n) if i != j]
            f.write(" + ".join(cons) + " = 1;\n")

        # Constraints: one incoming edge per node
        for j in range(n):
            cons = [f"x{i+1}_{j+1}" for i in range(n) if i != j]
            f.write(" + ".join(cons) + " = 1;\n")

        f.write("\n")

        # Subtour elimination (MTZ)
        for i in range(2, n+1):
            f.write(f"u{i} >= 2;\n")
            f.write(f"u{i} <= {n};\n")
        for i in range(2, n+1):
            for j in range(2, n+1):
                if i != j:
                    f.write(f"u{i} - u{j} + {n} x{i}_{j} <= {n - 1};\n")
        f.write("\n")

        # Declare binary variables
        bin_vars = [f"x{i+1}_{j+1}" for i in range(n) for j in range(n) if i != j]
        f.write("bin " + ", ".join(bin_vars) + ";\n")

        # Declare integer variables
        int_vars = [f"u{i}" for i in range(2, n+1)]
        f.write("int " + ", ".join(int_vars) + ";\n")

    print(f"LP model written to {filename}")

def write_ampl_dat_file(dist, filename="tsp_data.dat"):
    n = len(dist)
    with open(filename, 'w') as f:
        # Set of nodes
        f.write("set NODES := ")
        f.write(" ".join(str(i+1) for i in range(n)) + ";\n\n")

        # Distance matrix
        f.write("param dist :\n")
        f.write("     " + "  ".join(str(j+1) for j in range(n)) + " :=\n")
        for i in range(n):
            f.write(f"{i+1}   " + "  ".join(str(dist[i][j]) for j in range(n)) + "\n")
        f.write(";\n")

    print(f"AMPL .dat file written to {filename}")

def euclidean(c1, c2):
    return round(math.hypot(c1[0] - c2[0], c1[1] - c2[1]))

def tsp_to_mps(tsp_filename, mps_filename):
    coords = read_tsplib(tsp_filename)
    n = len(coords)
    dist = [[euclidean(coords[i], coords[j]) if i != j else 0 for j in range(n)] for i in range(n)]

    prob = LpProblem("TSP_MTZ", LpMinimize)

    # Decision variables x[i,j] = 1 if path goes from i to j
    x = {(i,j): LpVariable(f"x_{i}_{j}", cat=LpBinary)
         for i in range(n) for j in range(n) if i != j}

    # MTZ variables u[i] for subtour elimination
    u = {i: LpVariable(f"u_{i}", lowBound=2, upBound=n, cat=LpInteger)
         for i in range(1, n)}  # node 0 is the depot

    # Objective: minimize total distance
    prob += lpSum(dist[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j)

    # Outdegree = 1
    for i in range(n):
        prob += lpSum(x[i, j] for j in range(n) if i != j) == 1, f"Out_{i}"

    # Indegree = 1
    for j in range(n):
        prob += lpSum(x[i, j] for i in range(n) if i != j) == 1, f"In_{j}"

    # Subtour elimination (MTZ)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                prob += u[i] - u[j] + n * x[i, j] <= n - 1, f"MTZ_{i}_{j}"

    # Export to MPS
    prob.writeMPS(mps_filename, mpsSense=1)
    print(f"MPS file written: {mps_filename}")

import numpy as np

def assignment_problem(excel_path, name, big_M=1e6):
    # Load the Excel file
    df = pd.read_excel(excel_path, header=None)
    cost = df.values

    # Substituir NaN e Inf por um valor grande (big_M)
    cost = np.nan_to_num(cost, nan=big_M, posinf=big_M, neginf=big_M)

    num_workers, num_tasks = cost.shape

    prob = LpProblem("Assignment_Problem", LpMinimize)

    # Decision variables: x[i][j] = 1 if worker i is assigned to task j
    x = {(i, j): LpVariable(f"x_{i}_{j}", cat=LpBinary)
         for i in range(num_workers) for j in range(num_tasks)}

    # Objective: minimize total cost
    prob += lpSum(cost[i][j] * x[i, j] for i in range(num_workers) for j in range(num_tasks)), "Total_Cost"

    # Constraints: each worker is assigned to exactly one task
    for i in range(num_workers):
        prob += lpSum(x[i, j] for j in range(num_tasks)) == 1, f"Worker_{i}_assigned_once"

    # Constraints: each task is assigned to exactly one worker
    for j in range(num_tasks):
        prob += lpSum(x[i, j] for i in range(num_workers)) == 1, f"Task_{j}_assigned_once"

    # Export to LP and MPS formats
    prob.writeLP(f"lp/{name}.lp")
    prob.writeMPS(f"mps/{name}.mps")
    print(f"Assignment LP written to: lp/{name}.lp")
    print(f"Assignment MPS written to: mps/{name}.mps")

    with open(f"dat/{name}.dat", "w") as f:
        f.write("set WORKERS := " + " ".join(f"w{i+1}" for i in range(num_workers)) + ";\n")
        f.write("set TASKS := " + " ".join(f"t{j+1}" for j in range(num_tasks)) + ";\n\n")

        f.write("param cost : " + " ".join(f"t{j+1}" for j in range(num_tasks)) + " :=\n")
        for i in range(num_workers):
            row = "w" + str(i+1) + " " + " ".join(str(cost[i][j]) for j in range(num_tasks))
            f.write(row + "\n")
        f.write(";\n")
    print(f"Assignment DAT written to: dat/{name}.dat")


def create_all(name):
    coords = read_tsplib(f"tsp/{name}.tsp")
    dist = generate_distance_matrix(coords)
    generate_lp_file(dist, f"lp/{name}.lp")
    write_ampl_dat_file(dist, f"dat/{name}.dat")
    tsp_to_mps(f"tsp/{name}.tsp", f"mps/{name}.mps")

def main():
    #create_all("a280")
    #create_all("berlin52")
    #create_all("ulysses16")
    #assignment_problem("joao_victor/Assignment100.xlsx", "Assignment100")
    assignment_problem("joao_victor/Assignment200.xlsx", "Assignment200")
    assignment_problem("joao_victor/Assignment400.xlsx", "Assignment400")
    assignment_problem("joao_victor/Assignment600.xlsx", "Assignment600")
    

if __name__ == "__main__":
    main()