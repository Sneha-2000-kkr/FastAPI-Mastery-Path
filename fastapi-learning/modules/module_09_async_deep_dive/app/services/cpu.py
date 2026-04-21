def count_primes(upto: int) -> int:
    """Naive prime counter — pure CPU work, perfect for a process pool."""
    if upto < 2:
        return 0
    sieve = bytearray([1]) * (upto + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(upto ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return sum(sieve)
