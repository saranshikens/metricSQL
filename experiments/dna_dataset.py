import random

DNA_CHARS = ["A", "C", "G", "T"]

def random_dna(length=60):

    return "".join(
        random.choice(DNA_CHARS)
        for _ in range(length)
    )

dataset = [

    random_dna()

    for _ in range(3000)
]

if __name__ == "__main__":

    print("\nSample DNA Sequences:\n")

    for seq in dataset[:5]:

        print(seq)