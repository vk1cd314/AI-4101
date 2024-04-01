import random

def generate_random_piles(size=3, max_stones=10):
    return [random.randint(1, max_stones) for _ in range(size)]
