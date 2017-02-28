from two_phase_simplex import Simplex2

if __name__ == "__main__":
    print("Solve the first solution.\n")

    t = Simplex2('min', [-3, -1, -3])
    t.add_constraint([2, 1, 1], 2, "<=")
    t.add_constraint([1, 1, 3], 5, "<=")
    t.add_constraint([2, 2, 1], 6, "<=")
    t.solve()

    print("\n\n\nSolve the second solution.\n")
    t = Simplex2("min", [-9, 12, 41])
    t.add_constraint([1, -1, -5], 17, "<=")
    t.add_constraint([1, -2, -8], -36, "<=")
    t.add_constraint([1, -2, -5], 28, "<=")
    t.solve()
