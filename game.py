import argparse
import random

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

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
    'F': 'Fenilalanina', 'L': 'Leucina',      'S': 'Serina',         'Y': 'Tirosina',
    'C': 'Cisteina',     'W': 'Triptofano',   'P': 'Prolina',        'H': 'Histidina',
    'Q': 'Glutamina',    'R': 'Arginina',     'I': 'Isoleucina',     'M': 'Metionina',
    'T': 'Treonina',     'N': 'Asparagina',   'K': 'Lisina',         'V': 'Valina',
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
    table = Table(title="Tabla del codigo genetico", box=box.ROUNDED, style="cyan")
    table.add_column("Codon", style="bold yellow")
    table.add_column("Letra", style="bold white")
    table.add_column("Aminoacido", style="green")
    for codon, letra in CODON_TO_AA.items():
        nombre = "Stop" if letra == "STOP" else AA_NAMES.get(letra, "")
        style = "red" if letra == "STOP" else ""
        table.add_row(codon, letra, nombre, style=style)
    console.print(table)


def transcribe(dna):
    return dna.replace('T', 'U')


def anticodon(codon):
    return ''.join(COMPLEMENT[b] for b in codon)


def ask(prompt, correct, lives):
    while lives > 0:
        answer = console.input(f"[bold cyan]{prompt}[/bold cyan]").strip().upper()
        if answer == 'TABLA':
            show_table()
            continue
        if answer == correct.upper():
            if lives == 1:
                console.print("  [bold green]Por poco! El organismo resiste.[/bold green]")
            return True, lives
        lives -= 1
        if lives == 0:
            console.print(f"  [red]Incorrecto. La respuesta era: [bold]{correct}[/bold][/red]")
        elif lives == 1:
            console.print("  [red]Incorrecto. El organismo se debilita... es tu ultima oportunidad.[/red]")
        else:
            console.print(f"  [yellow]Incorrecto. Te quedan {lives} vida(s).[/yellow]")
    return False, lives


def show_sequence(seq, label, show_indices=True):
    if show_indices:
        table = Table(title=label, box=box.SIMPLE, style="dim")
        table.add_column("Pos", style="dim")
        for i in range(len(seq)):
            table.add_column(str(i), style="bold yellow", justify="center")
        table.add_row("Base", *list(seq))
        console.print(table)
    else:
        console.print(f"\n[bold]{label}:[/bold] [yellow]{seq}[/yellow]")


def choose_sequence(solved):
    options = random.sample(SEQUENCES, 3)
    console.print(Panel(
        "[bold]Se detectaron 3 genes que requieren ser expresados.[/bold]\n"
        "Como ARN Polimerasa II, solo podras transcribir uno.\n"
        "Elige con sabiduria:",
        style="cyan", box=box.ROUNDED
    ))
    for i, seq in enumerate(options, 1):
        resuelto = " [bold green](Resuelto)[/bold green]" if seq['nombre'] in solved else ""
        console.print(f"  [bold]{i}.[/bold] [white]{seq['nombre']}[/white]{resuelto}")
        console.print(f"     [dim]{seq['intro']}[/dim]\n")

    while True:
        choice = console.input("[bold cyan]Que gen transcribes? (1-3): [/bold cyan]").strip()
        if choice in ('1', '2', '3'):
            return options[int(choice) - 1]
        console.print("  [red]Ingresa 1, 2 o 3.[/red]")


def part1_intro():
    console.print(Panel(
        "[bold white]RPG: TRAVESIA GENICA[/bold white]",
        style="bold cyan", box=box.DOUBLE, expand=False
    ))
    console.print("""
Una alarma silenciosa recorre el organismo.

Las señales quimicas llegan al nucleo celular.
Los factores de transcripcion se activan
y se unen al promotor del gen,
reclutando a la [bold cyan]ARN Polimerasa II[/bold cyan]...

[bold white]Esa sos vos.[/bold white]

El organismo depende de que hagas tu trabajo.
""")
    console.input("[dim]Presiona ENTER para comenzar...[/dim]")


def part2_transcription(dna, lives):
    console.print(Panel("[bold]PARTE II: TRANSCRIPCION[/bold]", style="cyan", box=box.ROUNDED))
    console.print("\nTe posicionas en el promotor. La doble hebra de ADN se abre ante vos.")
    console.print("Tu trabajo es sintetizar el ARN mensajero copiando la secuencia de ADN.")
    console.print(Panel(
        "[bold]Regla de transcripcion:[/bold]\n"
        "La [bold red]Timina (T)[/bold red] del ADN se reemplaza por [bold yellow]Uracilo (U)[/bold yellow] en el ARNm.\n"
        "El resto de las bases (A, G, C) se copian igual.\n\n"
        "[dim]Ejemplo: ATGCAT  ->  AUGCAU[/dim]",
        box=box.ROUNDED, style="dim"
    ))

    pre_mrna = transcribe(dna)

    while lives > 0:
        show_sequence(dna, "ADN a transcribir", show_indices=False)
        answer = console.input("\n[bold cyan]Escribi el ARNm resultante: [/bold cyan]").strip().upper()

        if answer == pre_mrna:
            console.print(f"\n[bold green]Correcto! ARN pre-maduro sintetizado:[/bold green] [yellow]{pre_mrna}[/yellow]")
            console.print("[dim]Pero el ARN aun no esta listo para salir del nucleo. Debe ser procesado...[/dim]\n")
            return pre_mrna, lives

        lives -= 1
        if lives == 0:
            console.print(f"  [red]Incorrecto. La respuesta era: [bold]{pre_mrna}[/bold][/red]")
            return None, lives

        errors = [i for i in range(min(len(answer), len(pre_mrna))) if answer[i] != pre_mrna[i]]
        if len(answer) != len(pre_mrna):
            console.print(f"  [yellow]Incorrecto. La longitud no coincide (esperaba {len(pre_mrna)} bases, escribiste {len(answer)}).[/yellow]")
        else:
            console.print(f"  [yellow]Incorrecto. Hay {len(errors)} error(es) en las posiciones: {errors}[/yellow]")
        if lives == 1:
            console.print("  [red]El organismo se debilita... es tu ultima oportunidad.[/red]")
        else:
            console.print(f"  [yellow]Te quedan {lives} vida(s).[/yellow]")

    return None, lives


def part2b_splicing(pre_mrna, intron):
    console.print(Panel("[bold]PARTE III: SPLICING[/bold]", style="cyan", box=box.ROUNDED))
    console.print("\nEl ARN pre-maduro no puede salir del nucleo todavia.")
    console.print("El [bold]espliceosoma[/bold], una maquinaria molecular gigante, lo reconoce")
    console.print("e identifica las regiones no codificantes llamadas [bold red]intrones[/bold red].")
    console.print(f"\n[bold]Intron detectado:[/bold] [red]{intron}[/red]")
    console.print("El spliceosoma lo elimina y une los [bold green]exones[/bold green] entre si.")

    mature_mrna = pre_mrna.replace(intron, '', 1)
    console.print(f"\n[dim]ARN pre-maduro:[/dim] [yellow]{pre_mrna}[/yellow]")
    console.print(f"[dim]ARNm maduro:   [/dim] [bold green]{mature_mrna}[/bold green]")
    console.print("\n[dim]El ARNm maduro sale del nucleo hacia el ribosoma...[/dim]\n")
    console.input("[dim]Presiona ENTER para continuar...[/dim]")

    return mature_mrna


def part3_translation(arnm, lives):
    console.print(Panel("[bold]PARTE IV: TRADUCCION[/bold]", style="cyan", box=box.ROUNDED))
    console.print("\nEl ARNm maduro llega al ribosoma. La maquinaria de traduccion se ensambla.")
    console.print("El ribosoma recorre el ARNm en busca del codon de inicio [bold yellow]AUG[/bold yellow]...\n")

    show_sequence(arnm, "ARNm")

    aug_pos = str(arnm.find('AUG'))
    ok, lives = ask(f"\nEn que posicion encontras el codon AUG? (0-{len(arnm)-1}): ", aug_pos, lives)

    if not ok:
        return [], lives

    aug_idx = int(aug_pos)
    console.print(f"\n[bold green]Correcto![/bold green] El ribosoma se ancla en la posicion {aug_pos}.")
    console.print("La traduccion comienza. Cada codon reclutara a un ARNt portador de su aminoacido...\n")

    protein = []
    i = aug_idx
    while i + 3 <= len(arnm):
        codon = arnm[i:i+3]
        aa = CODON_TO_AA.get(codon)

        if aa == 'STOP':
            console.print(f"[bold red]Codon {codon} -> STOP.[/bold red]")
            console.print("El ribosoma reconoce la senal de fin y se disocia del ARNm.")
            console.print("[dim]La cadena polipeptidica es liberada y comienza a plegarse...[/dim]\n")
            break

        console.print(f"\n[bold cyan]--- Codon: {codon} ---[/bold cyan]")
        console.print("Un ARNt se acerca al ribosoma...")
        ok, lives = ask(f"Codon {codon}: que aminoacido trae el ARNt? (letra o 'tabla'): ", aa, lives)
        if not ok:
            break

        console.print(f"  [green]Correcto! {aa} = {AA_NAMES.get(aa, aa)}[/green]")

        anticodon_correcto = anticodon(codon)
        console.print("  El ARNt tiene un anticodon [bold]complementario[/bold] al codon del ARNm.")
        console.print("  Regla de complementariedad: [bold]A[/bold] <-> [bold]U[/bold]  |  [bold]G[/bold] <-> [bold]C[/bold]")
        ok, lives = ask(f"Codon {codon}: cual es el anticodon del ARNt? ", anticodon_correcto, lives)
        if not ok:
            break

        console.print(f"  [green]Correcto! El ARNt con anticodon {anticodon_correcto} deposita {AA_NAMES.get(aa, aa)} en la cadena.[/green]\n")
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

    console.print(f"\n[bold]Dificultad:[/bold] {difficulty.upper()} | [bold]Vidas:[/bold] {lives}")

    part1_intro()

    solved = set()

    while True:
        seq = choose_sequence(solved)

        console.print(f"\n[bold]Elegiste:[/bold] [cyan]{seq['nombre']}[/cyan]")
        console.input("[dim]Presiona ENTER para iniciar la transcripcion...[/dim]")

        current_lives = lives
        pre_mrna, current_lives = part2_transcription(seq['dna'], current_lives)
        if current_lives <= 0 or pre_mrna is None:
            console.print(Panel(
                "[bold]GAME OVER[/bold]\n\n"
                "La transcripcion fallo. El ARN nunca fue sintetizado.\n"
                "El organismo no pudo responder. La mision fracaso.",
                style="bold red", box=box.DOUBLE
            ))
        else:
            mature_mrna = part2b_splicing(pre_mrna, seq['intron'])

            protein, current_lives = part3_translation(mature_mrna, current_lives)
            if current_lives <= 0:
                console.print(Panel(
                    "[bold]GAME OVER[/bold]\n\n"
                    "La traduccion fue interrumpida. La proteina quedo incompleta.\n"
                    "El organismo no pudo recuperarse. La mision fracaso.",
                    style="bold red", box=box.DOUBLE
                ))
            else:
                table = Table(title="Proteina sintetizada", box=box.ROUNDED, style="green")
                table.add_column("Letra", style="bold white", justify="center")
                table.add_column("Aminoacido", style="green")
                for aa in protein:
                    table.add_row(aa, AA_NAMES.get(aa, aa))

                console.print(Panel(
                    f"[bold]MISION CUMPLIDA![/bold]\n\n{seq['ending']}",
                    style="bold green", box=box.DOUBLE
                ))
                console.print(table)
                console.print(f"\n[dim]Vidas restantes: {current_lives}[/dim]\n")
                solved.add(seq['nombre'])

        again = console.input("[bold cyan]Queres jugar de nuevo? (s/n): [/bold cyan]").strip().lower()
        if again != 's':
            console.print(Panel(
                "[bold]Hasta la proxima.[/bold]\nEl organismo te lo agradece.",
                style="cyan", box=box.ROUNDED
            ))
            break
        console.print()


if __name__ == '__main__':
    main()
