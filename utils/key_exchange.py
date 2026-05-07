def dh_generate_public(prime: int, generator: int, private_key: int) -> int:
    return pow(generator, private_key, prime)


def dh_generate_shared_secret(peer_public: int, private_key: int, prime: int) -> int:
    return pow(peer_public, private_key, prime)
