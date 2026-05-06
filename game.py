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
    'F': 'Fenilalanina', 'L': 'Leucina',     'S': 'Serina',          'Y': 'Tirosina',
    'C': 'Cisteina',     'W': 'Triptofano',  'P': 'Prolina',         'H': 'Histidina',
    'Q': 'Glutamina',    'R': 'Arginina',    'I': 'Isoleucina',      'M': 'Metionina',
    'T': 'Treonina',     'N': 'Asparagina',  'K': 'Lisina',          'V': 'Valina',
    'A': 'Alanina',      'D': 'Ac. aspartico','E': 'Ac. glutamico',  'G': 'Glicina',
}

COMPLEMENT = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}

SEQUENCES = [
    {
        "nombre": "Gen de reparacion de ADN",
        "dna": "GCTATAAACGGATGGTAACAGAAAGCTTAA",
        "intron": "GUAACAG",
        "incorrectas": ["GUAAACAG", "GUACCAG"],
        "intro": "Este gen codifica una enzima que detecta y repara errores en el ADN.",
        "ending": "La enzima de reparacion recorre el genoma, sellando cada fractura.\nEl ADN danado fue restaurado. El organismo sobrevive gracias a vos."
    },
    {
        "nombre": "Gen de receptor de membrana",
        "dna": "CTATAAATTTCGGATGGTCCAGCGTGAATAA",
        "intron": "GUCCAG",
        "incorrectas": ["GUACAG", "GUCAAG"],
        "intro": "Este gen codifica un receptor que permite a la celula detectar seniales del entorno.",
        "ending": "El receptor se ancla en la membrana y capta las seniales quimicas.\nLas comunicaciones celulares se restauran. El organismo responde al entorno."
    },
    {
        "nombre": "Gen de proteina de defensa",
        "dna": "AAGCTATAAAGCGATGGTCCAGCCTTTTGAATAG",
        "intron": "GUCCAG",
        "incorrectas": ["GUACAG", "GUUUAG"],
        "intro": "Este gen codifica una proteina del sistema inmune frente a una amenaza detectada.",
        "ending": "La proteina de defensa identifica al agente extrano y lo neutraliza.\nEl sistema inmune triunfa. El organismo queda protegido."
    },
    {
        "nombre": "Gen estructural",
        "dna": "GGATGGTACAGCATCCGGAATAA",
        "intron": "GUACAG",
        "incorrectas": ["GUAACAG", "GUAGCAG"],
        "intro": "Este gen codifica una proteina que refuerza la estructura del citoesqueleto celular.",
        "ending": "La proteina estructural se ensambla en filamentos que sostienen la celula.\nLas celulas recuperan su forma y su resistencia."
    },
    {
        "nombre": "Gen de transporte",
        "dna": "TTCGGATGGTAAAGGTACCCAAATGA",
        "intron": "GUAAAG",
        "incorrectas": ["GUACAG", "GUAAACAG"],
        "intro": "Este gen codifica una proteina que transporta moleculas esenciales a traves de la celula.",
        "ending": "La proteina de transporte carga su molecula y recorre la celula.\nLos nutrientes llegan a donde se necesitan. El metabolismo se reactiva."
    },
    {
        "nombre": "Gen hormonal",
        "dna": "CCCATGGTCAGAAGTTCGACTAA",
        "intron": "GUCAG",
        "incorrectas": ["GUACAG", "GUCCAG"],
        "intro": "Este gen codifica una hormona peptidica que regula el equilibrio interno del organismo.",
        "ending": "La hormona es liberada al torrente sanguineo y llega a sus celulas blanco.\nEl organismo recupera su equilibrio. La homeostasis se restaura."
    },
    {
        "nombre": "Gen regulador",
        "dna": "AAATGGTTTAGCGCAAAGAATGA",
        "intron": "GUUUAG",
        "incorrectas": ["GUUUUAG", "GUUAG"],
        "intro": "Este gen codifica una proteina reguladora que controla la expresion de otros genes.",
        "ending": "La proteina reguladora se une al ADN y activa los genes silenciados.\nLa expresion genica del organismo se estabiliza. El ciclo celular continua."
    },
    {
        "nombre": "Gen de choque termico",
        "dna": "CCATGGTGCAGCCGCAAGCTTAA",
        "intron": "GUGCAG",
        "incorrectas": ["GUACAG", "GUGCAAG"],
        "intro": "Este gen se activa cuando las proteinas del organismo estan danadas por el calor.",
        "ending": "La proteina de choque termico envuelve a las proteinas danadas y las repliega.\nLas proteinas recuperan su forma funcional. La celula sobrevive al estres termico."
    },
    {
        "nombre": "Gen de factor de transcripcion",
        "dna": "CCATGGTCCAGATTAAAAGAGAATAG",
        "intron": "GUCCAG",
        "incorrectas": ["GUACAG", "GUCAAG"],
        "intro": "Este gen codifica una proteina que activa la lectura de otros genes en el nucleo.",
        "ending": "El factor de transcripcion ingresa al nucleo y se une al ADN.\nNuevos genes se activan en cascada. El organismo se adapta al nuevo entorno."
    },
    {
        "nombre": "Gen metabolico",
        "dna": "TATGGTCAGAAACCCGGCTAG",
        "intron": "GUCAG",
        "incorrectas": ["GUACAG", "GUCCAG"],
        "intro": "Este gen codifica una enzima clave para la produccion de energia celular.",
        "ending": "La enzima metabolica cataliza la reaccion que desbloquea la energia almacenada.\nLas mitocondrias recuperan su ritmo. El organismo vuelve a la vida."
    },
]


def show_table():
    print("\n" + "=" * 50)
    print("Tabla del codigo genetico:")
    print(f"{'CODON':<8} {'Letra':<8} {'Nombre'}")
    print("-" * 50)
    for codon, letra in CODON_TO_AA.items():
        nombre = 'Stop' if letra == 'STOP' else AA_NAMES.get(letra, '')
        print(f"{codon:<8} {letra:<8} {nombre}")
    print("=" * 50 + "\n")


def transcribe(dna):
    return dna.replace('T', 'U')


def anticodon(codon):
    return ''.join(COMPLEMENT[b] for b in codon)


def ask(prompt, correct, lives):
    while lives > 0:
        answer = input(prompt).strip().upper()
        if answer == 'TABLA':
            show_table()
            continue
        if answer == correct.upper():
            if lives == 1:
                print("  Por poco! El organismo resiste.")
            return True, lives
        lives -= 1
        if lives == 0:
            print(f"  Incorrecto. La respuesta era: {correct}")
        elif lives == 1:
            print(f"  Incorrecto. El organismo se debilita... es tu ultima oportunidad.")
        else:
            print(f"  Incorrecto. Te quedan {lives} vida(s).")
    return False, lives


def show_sequence(seq, label, show_indices=True):
    print(f"\n{label}:")
    if show_indices:
        header = "Pos: | " + " | ".join(f"{i:<2}" for i in range(len(seq))) + " |"
        bases  = "Base:| " + " | ".join(f"{b:<2}" for b in seq) + " |"
        print(header)
        print(bases)
    else:
        print(f"  {seq}")


def choose_sequence(solved):
    options = random.sample(SEQUENCES, 3)
    print("\nSe detectaron 3 genes que requieren ser expresados.")
    print("Como ARN Polimerasa II, solo podras transcribir uno.")
    print("Elige con sabiduria:\n")
    for i, seq in enumerate(options, 1):
        resuelto = " (Resuelto)" if seq['nombre'] in solved else ""
        print(f"  {i}. {seq['nombre']}{resuelto}")
        print(f"     {seq['intro']}\n")

    while True:
        choice = input("Que gen transcribes? (1-3): ").strip()
        if choice in ('1', '2', '3'):
            return options[int(choice) - 1]
        print("  Ingresa 1, 2 o 3.")


def part1_intro():
    print("\n" + "=" * 50)
    print("   RPG: TRAVESIA GENICA")
    print("=" * 50)
    print("""
Una alarma silenciosa recorre el organismo.

Las seniales quimicas llegan al nucleo celular.
Los factores de transcripcion se activan.
El factor TFIID se une al promotor del gen
y recluta a la ARN Polimerasa II...

Esa sos vos.

El organismo depende de que hagas tu trabajo.
""")
    input("Presiona ENTER para comenzar...")


def part2_transcription(dna, lives):
    print("\n" + "=" * 50)
    print("   PARTE II: TRANSCRIPCION")
    print("=" * 50)
    print("\nTe posicionas en el promotor. La doble hebra de ADN se abre ante vos.")
    print("Tu trabajo es sintetizar el ARN mensajero copiando la secuencia de ADN.")
    print("\nRegla de transcripcion:")
    print("  La Timina (T) del ADN se reemplaza por Uracilo (U) en el ARNm.")
    print("  El resto de las bases (A, G, C) se copian igual.")
    print("\nEjemplo: ATGCAT  ->  AUGCAU\n")

    pre_mrna = transcribe(dna)

    while lives > 0:
        show_sequence(dna, "ADN a transcribir", show_indices=False)
        answer = input("\nEscribi el ARNm resultante: ").strip().upper()

        if answer == pre_mrna:
            print(f"\nCorrecto! ARN pre-maduro sintetizado: {pre_mrna}")
            print("Pero el ARN aun no esta listo para salir del nucleo. Debe ser procesado...\n")
            return pre_mrna, lives

        lives -= 1
        if lives == 0:
            print(f"  Incorrecto. La respuesta era: {pre_mrna}")
            return None, lives

        errors = [i for i in range(min(len(answer), len(pre_mrna))) if answer[i] != pre_mrna[i]]
        if len(answer) != len(pre_mrna):
            print(f"  Incorrecto. La longitud no coincide (esperaba {len(pre_mrna)} bases, escribiste {len(answer)}).")
        else:
            print(f"  Incorrecto. Hay {len(errors)} error(es) en las posiciones: {errors}")
        if lives == 1:
            print("  El organismo se debilita... es tu ultima oportunidad.")
        else:
            print(f"  Te quedan {lives} vida(s).")

    return None, lives


def part2b_splicing(pre_mrna, intron):
    print("\n" + "=" * 50)
    print("   PARTE III: SPLICING")
    print("=" * 50)
    print("\nEl ARN pre-maduro no puede salir del nucleo todavia.")
    print("El spliceosoma, una maquinaria molecular gigante, lo reconoce")
    print("e identifica las regiones no codificantes llamadas intrones.")
    print(f"\nIntron detectado: {intron}")
    print("El spliceosoma lo elimina y une los exones entre si.")

    mature_mrna = pre_mrna.replace(intron, '', 1)
    print(f"\nARN pre-maduro: {pre_mrna}")
    print(f"ARNm maduro:    {mature_mrna}")
    print("\nEl ARNm maduro sale del nucleo hacia el ribosoma...\n")
    input("Presiona ENTER para continuar...")

    return mature_mrna


def part3_translation(arnm, lives):
    print("\n" + "=" * 50)
    print("   PARTE IV: TRADUCCION")
    print("=" * 50)
    print("\nEl ARNm maduro llega al ribosoma. La maquinaria de traduccion se ensambla.")
    print("El ribosoma recorre el ARNm en busca del codon de inicio AUG...\n")

    show_sequence(arnm, "ARNm")

    aug_pos = str(arnm.find('AUG'))
    ok, lives = ask(f"\nEn que posicion encontras el codon AUG? (0-{len(arnm)-1}): ", aug_pos, lives)

    if not ok:
        return [], lives

    aug_idx = int(aug_pos)
    print(f"\nCorrecto! El ribosoma se ancla en la posicion {aug_pos}.")
    print("La traduccion comienza. Cada codon reclutara a un ARNt portador de su aminoacido...\n")

    protein = []
    i = aug_idx
    while i + 3 <= len(arnm):
        codon = arnm[i:i+3]
        aa = CODON_TO_AA.get(codon)

        if aa == 'STOP':
            print(f"Codon {codon} -> STOP.")
            print("El ribosoma reconoce la senal de fin y se disocia del ARNm.")
            print("La cadena polipeptidica es liberada y comienza a plegarse...\n")
            break

        print(f"\n--- Codon: {codon} ---")
        print("Un ARNt se acerca al ribosoma...")
        ok, lives = ask(f"Codon {codon}: que aminoacido trae el ARNt? (letra o 'tabla'): ", aa, lives)
        if not ok:
            break

        print(f"  Correcto! {aa} = {AA_NAMES.get(aa, aa)}")

        anticodon_correcto = anticodon(codon)
        print(f"  El ARNt tiene un anticodon complementario al codon del ARNm.")
        print(f"  Regla de complementariedad: A <-> U  |  G <-> C")
        ok, lives = ask(f"Codon {codon}: cual es el anticodon del ARNt? ", anticodon_correcto, lives)
        if not ok:
            break

        print(f"  Correcto! El ARNt con anticodon {anticodon_correcto} deposita {AA_NAMES.get(aa, aa)} en la cadena.\n")
        protein.append(aa)
        i += 3

    return protein, lives


def main():
    parser = argparse.ArgumentParser(description='RPG de Expresion Genica')
    parser.add_argument('--dificultad', choices=['facil', 'dificil'], default='facil',
                        help='Dificultad del juego (default: facil)')
    args = parser.parse_args()

    difficulty = args.dificultad
    lives = 3 if difficulty == 'facil' else 1

    print(f"\nDificultad: {difficulty.upper()} | Vidas: {lives}")

    part1_intro()

    solved = set()

    while True:
        seq = choose_sequence(solved)

        print(f"\nElegiste: {seq['nombre']}")
        input("Presiona ENTER para iniciar la transcripcion...")

        current_lives = lives
        pre_mrna, current_lives = part2_transcription(seq['dna'], current_lives)
        if current_lives <= 0 or pre_mrna is None:
            print("\n" + "=" * 50)
            print("   GAME OVER")
            print("=" * 50)
            print("\nLa transcripcion fallo. El ARN nunca fue sintetizado.")
            print("El organismo no pudo responder. La mision fracaso.\n")
        else:
            mature_mrna = part2b_splicing(pre_mrna, seq['intron'])

            protein, current_lives = part3_translation(mature_mrna, current_lives)
            if current_lives <= 0:
                print("\n" + "=" * 50)
                print("   GAME OVER")
                print("=" * 50)
                print("\nLa traduccion fue interrumpida. La proteina quedo incompleta.")
                print("El organismo no pudo recuperarse. La mision fracaso.\n")
            else:
                print("\n" + "=" * 50)
                print("   MISION CUMPLIDA!")
                print("=" * 50)
                print(f"\nProteina sintetizada: {''.join(protein)}")
                print("\nAminoacidos:")
                for aa in protein:
                    print(f"  {aa} -> {AA_NAMES.get(aa, aa)}")
                print(f"\n{seq['ending']}")
                print(f"\nVidas restantes: {current_lives}\n")
                solved.add(seq['nombre'])

        again = input("Queres jugar de nuevo? (s/n): ").strip().lower()
        if again != 's':
            print("\nHasta la proxima. El organismo te lo agradece.\n")
            break
        print()


if __name__ == '__main__':
    main()
