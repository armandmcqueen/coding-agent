def generate_triangle_numbers(n):
    triangle_numbers = []
    for i in range(1, n + 1):
        triangle_number = (i * (i + 1)) // 2
        triangle_numbers.append(triangle_number)
    return triangle_numbers

def main():
    first_7_triangle_numbers = generate_triangle_numbers(7)
    print("The first 7 triangle numbers are:")
    for i, number in enumerate(first_7_triangle_numbers, start=1):
        print(f"{i}: {number}")

if __name__ == "__main__":
    main()