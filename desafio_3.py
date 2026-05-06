import sys


TATA = "TATAAA"

def get_promoted_regions(adn_seq):
    regions = []
    idx = adn_seq.find(TATA)
    while idx >= 0:
        last_idx = adn_seq.find(TATA, idx + 1)

        if last_idx >= 0:
            regions.append(adn_seq[idx:last_idx+ len(TATA)])

        idx = last_idx


    return regions

input_seq = input("ADN: \n")
regions = get_promoted_regions(input_seq)
print(regions)