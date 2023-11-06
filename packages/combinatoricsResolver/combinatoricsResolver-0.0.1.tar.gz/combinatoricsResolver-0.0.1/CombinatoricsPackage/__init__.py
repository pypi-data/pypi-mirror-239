from itertools import permutations
from itertools import combinations

def fact(n):
    if n == 1: 
        return 1
    else:
        return n * fact(n-1)

def nCr(n, r):
    num = 1
    num1 = 1
    for i in range(n-r+1,n+1):
        num *= i
    for i in range(1,r+1):
        num1 *= i
    return num / num1

def nPr(n, r):
    num = nCr(n, r)
    return num * fact(r)

def catalan(n):
    num = nCr(2*n,n)
    return num / (n+1)

def printPermutations(n):
    num = list(range(1,n+1))
    permutationsList = permutations(num)
    for i in permutationsList:
        print(i)

def generateCombinations(elements):
    all_combinations = []
    for r in range(len(elements) + 1):
        combinations_r = list(combinations(elements, r))
        all_combinations.extend(combinations_r)
    for i in all_combinations:
        print(i)


def permutations_without_repetition(elements, k):
    perms = list(permutations(elements, k))
    print(f"Permutations without repetition of {k} elements:", perms)

def combinations_without_repetition(elements, k):
    combs = list(combinations(elements, k))
    print(f"Combinations without repetition of {k} elements:", combs)

def permutations_with_repetition(elements, k):
    from itertools import product
    perms_repetition = list(product(elements, repeat=k))
    print(f"Permutations with repetition of {k} elements:", perms_repetition)

def combinations_with_repetition(elements, k):
    from itertools import combinations_with_replacement
    combs_repetition = list(combinations_with_replacement(elements, k))
    print(f"Combinations with repetition of {k} elements:", combs_repetition)

def pascals_triangle(n):
    triangle = []
    for i in range(n):
        row = [1]
        if i > 0:
            for j in range(1, i):
                row.append(triangle[i - 1][j - 1] + triangle[i - 1][j])
            row.append(1)
        triangle.append(row)
    print("Pascal's Triangle (first", n, "rows):")
    for row in triangle:
        print(row)

def fibonacci_sequence(n):
    fibonacci = [0, 1]
    while len(fibonacci) < n:
        next_num = fibonacci[-1] + fibonacci[-2]
        fibonacci.append(next_num)
    print("Fibonacci Sequence (first", n, "elements):", fibonacci)

def lucas_sequence(n):
    lucas = [2, 1]
    while len(lucas) < n:
        next_num = lucas[-1] + lucas[-2]
        lucas.append(next_num)
    print("Lucas Sequence (first", n, "elements):", lucas)
    