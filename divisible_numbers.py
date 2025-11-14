from typing import List, Tuple

def find_divisible_numbers(min_number: int, max_number: int, divisor: int) -> Tuple[List[int], int]:
    
    if min_number > max_number:
        raise ValueError(f"min_number ({min_number}) cannot be greater than max_number ({max_number}).")
    if divisor == 0:
        raise ValueError("divisor cannot be zero.")

    divisible_numbers: List[int] = []
    for number in range(min_number, max_number + 1):
        if number % divisor == 0:
            divisible_numbers.append(number)

    total_count = max_number - min_number + 1
    return divisible_numbers, total_count


divisible, count = find_divisible_numbers(1, 50, 5)
print("Fully divisible numbers:", divisible)
print("Total number of values in the range:", count)
