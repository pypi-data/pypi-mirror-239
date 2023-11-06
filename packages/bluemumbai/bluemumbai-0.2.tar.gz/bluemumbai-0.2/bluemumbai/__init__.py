import pyperclip

def greet_and_copy():
    choice = input("Enter 1 or 2: ")
    if choice == '1':
        message = '''# Function to check whether a queen can be placed in the current position or not
def place(pos, a):
    for i in range(1, pos):
        if (a[i] == a[pos]) or (abs(a[i] - a[pos]) == abs(i - pos)):
            return False
    return True

# Function to print out the chessboard
def print_sol(N, cnt, a):
    cnt += 1
    print("\n\nSolution", cnt, "\n")
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if a[i] == j:
                print("\tQ", end="")
            else:
                print("\t.", end="")
        print("")

# Function to place N queens on an N*N chessboard such that no queen attacks each other
def solve_n_queens(N):
    a = [0] * (N + 1)
    cnt = 0
    solve(1, N, cnt, a)

def solve(k, N, cnt, a):
    for i in range(1, N + 1):
        a[k] = i
        if place(k, a):
            if k == N:
                print_sol(N, cnt, a)
            else:
                solve(k + 1, N, cnt, a)

# Driver Code
N = 4
solve_n_queens(N) '''
    elif choice == '2':
        message = '''def tower_of_hanoi(n, source, auxiliary, target):
    if n == 1:
        print("Move disk 1 from", source, "to", target)
        return
    tower_of_hanoi(n - 1, source, target, auxiliary)
    print("Move disk", n, "from", source, "to", target)
    tower_of_hanoi(n - 1, auxiliary, source, target)

# Example usage
n = 3  # Number of disks
source_peg = "A"
auxiliary_peg = "B"
target_peg = "C"
tower_of_hanoi(n, source_peg, auxiliary_peg, target_peg) '''
    else:
        message = "Invalid choice"

    print(message)
    pyperclip.copy(message)

greet_and_copy()

__all__ = []
