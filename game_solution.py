import argparse
import random

CODON_TO_AA = {
    'UUU': 'F', 'UUC': 'F',
    'UUA': 'L', 'UUG': 'L',
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'UAU': 'Y', 'UAC': 'Y',
    'UAA': 'STOP', 'UAG': 'STOP',
    'UGU': 'C', 'UGC': 'C',
    'UGA': 'STOP',
    'UGG': 'W',
    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAU': 'H', 'CAC': 'H',
    'CAA': 'Q', 'CAG': 'Q',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I',
    'AUG': 'M',
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAU': 'N', 'AAC': 'N',
    'AAA': 'K', 'AAG': 'K',
    'AGU': 'S', 'AGC': 'S',
    'AGA': 'R', 'AGG': 'R',
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAU': 'D', 'GAC': 'D',
    'GAA': 'E', 'GAG': 'E',
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

AA_NAMES = {
    'F': 'Fenilalanina', 'L': 'Leucina',  'S': 'Serina',           'Y': 'Tirosina',
    'C': 'Cisteina',     'W': 'Triptofano','P': 'Prolina',          'H': 'Histidina',
    'Q': 'Glutamina',    'R': 'Arginina',  'I': 'Isoleucina',       'M': 'Metionina',
    'T': 'Treonina',     'N': 'Asparagina','K': 'Lisina',           'V': 'Valina',
    'A': 'Alanina',      'D': 'Ac. aspartico','E': 'Ac. glutamico', 'G': 'Glicina',
}

TATA = "TATAAA"

# Cada secuencia tiene una caja TATA y un ATG corriente abajo
SEQUENCES = [
    "GCTATAAACGGATGAAAGCTTAA",
    "CTATAAATTTCGGATGCGTGAATAA",
    "AAGCTATAAAGCGATGCCTTTTGAATAG",
]


def show_table():
    print("\n=== CODIGO GENETICO ===")
    print(f"{'Codon':<7} {'AA':<5} {'Nombre'}")
    print("-" * 32)
    for codon, aa in CODON_TO_AA.items():
        name = 'Stop' if aa == 'STOP' else AA_NAMES.get(aa, '')
        print(f"{codon:<7} {aa:<5} {name}")
    print("=" * 32 + "\n")


def transcribe(dna):
    return dna.replace('T', 'U')


def ask(prompt, correct, lives, difficulty):
    max_tries = 3 if difficulty == 'facil' else 1
    attempts = 0
    while attempts < max_tries and lives > 0:
        answer = input(prompt).strip()
        if answer.lower() == 'tabla':
            show_table()
            continue
        if answer.upper() == correct.upper():
            return True, lives
        attempts += 1
        lives -= 1
        remaining = max_tries - attempts
        if remaining > 0 and lives > 0:
            print(f"  Incorrecto. Te quedan {remaining} intento(s) y {lives} vida(s).")
        else:
            print(f"  Incorrecto. La respuesta correcta era: {correct}")
    return False, lives


def part1_intro():
    print("\n" + "=" * 50)
    print("   RPG: EL VIAJE DE LA EXPRESION GENICA")
    print("=" * 50)
    print("""
El organismo detecta una situacion de estres.
El cortisol es liberado al torrente sanguineo.

El cortisol ingresa al nucleo celular y activa
los factores de transcripcion, que reclutan a
la ARN Polimerasa II...

Ese sos VOS.

Tu mision: transcribir el gen del estres y
fabricar la proteina que salvara al organismo.
""")
    input("Presiona ENTER para comenzar...")


def part2_transcription(dna, lives, difficulty):
    print("\n" + "=" * 50)
    print("   PARTE II: TRANSCRIPCION")
    print("=" * 50)
    print(f"\nSecuencia de ADN:")
    print(f"  {dna}")
    print(f"  {''.join(str(i % 10) for i in range(len(dna)))}")
    print("\nComo ARN Polimerasa, debes encontrar la caja TATA")
    print("para unirte al promotor e iniciar la transcripcion.\n")
    print("(Podes escribir 'tabla' en cualquier momento para consultar el codigo genetico)\n")

    tata_pos = str(dna.find(TATA))
    ok, lives = ask(f"En que posicion empieza la caja TATA? (0-{len(dna)-1}): ", tata_pos, lives, difficulty)

    if not ok:
        return None, lives

    print(f"\nCorrecto! La caja TATA esta en la posicion {tata_pos}.")
    print("La ARN Polimerasa se une al promotor...")
    print("Iniciando transcripcion...\n")

    mrna = transcribe(dna)
    print(f"ARNm sintetizado:")
    print(f"  {mrna}")
    print(f"  {''.join(str(i % 10) for i in range(len(mrna)))}\n")

    return mrna, lives


def part3_translation(mrna, lives, difficulty):
    print("\n" + "=" * 50)
    print("   PARTE III: TRADUCCION")
    print("=" * 50)
    print("\nEl ARNm viaja al ribosoma.")
    print("Buscando el codon de inicio AUG...\n")
    print(f"ARNm: {mrna}")
    print(f"      {''.join(str(i % 10) for i in range(len(mrna)))}\n")

    aug_pos = str(mrna.find('AUG'))
    ok, lives = ask(f"En que posicion esta el codon AUG? (0-{len(mrna)-1}): ", aug_pos, lives, difficulty)

    if not ok:
        return [], lives

    aug_idx = int(aug_pos)
    print(f"\nCorrecto! Iniciando traduccion desde la posicion {aug_pos}.\n")

    protein = []
    i = aug_idx
    while i + 3 <= len(mrna):
        codon = mrna[i:i+3]
        aa = CODON_TO_AA.get(codon)

        if aa == 'STOP':
            print(f"Codon: {codon} -> STOP. Traduccion terminada!")
            break

        ok, lives = ask(f"Codon {codon} -> Que aminoacido es? (letra o 'tabla'): ", aa, lives, difficulty)

        if not ok:
            break

        name = AA_NAMES.get(aa, aa)
        print(f"  Correcto! {aa} = {name}\n")
        protein.append(aa)
        i += 3

    return protein, lives


def main():
    parser = argparse.ArgumentParser(description='RPG de Expresion Genica')
    parser.add_argument('--dificultad', choices=['facil', 'dificil'], default='facil',
                        help='Dificultad del juego (default: facil)')
    args = parser.parse_args()

    difficulty = args.dificultad
    lives = 5 if difficulty == 'facil' else 3

    print(f"\nDificultad: {difficulty.upper()} | Vidas: {lives}")

    part1_intro()

    dna = random.choice(SEQUENCES)

    mrna, lives = part2_transcription(dna, lives, difficulty)
    if lives <= 0 or mrna is None:
        print("\nGame over. Te quedaste sin vidas.")
        return

    protein, lives = part3_translation(mrna, lives, difficulty)
    if lives <= 0:
        print("\nGame over. Te quedaste sin vidas.")
        return

    print("\n" + "=" * 50)
    print("   MISION CUMPLIDA!")
    print("=" * 50)
    print(f"\nProteina sintetizada: {''.join(protein)}")
    print("El organismo pudo responder al estres. Ganaste!")
    print(f"Vidas restantes: {lives}\n")


if __name__ == '__main__':
    main()
