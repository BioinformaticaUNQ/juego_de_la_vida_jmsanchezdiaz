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

def show_lives(lives, max_lives):
    hearts = "[bold red]♥[/bold red]" * lives + "[dim]♡[/dim]" * (max_lives - lives)
    console.print(f"  Vidas: {hearts}\n")

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


DNA_COMPLEMENT = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

def dna_complement(seq):
    return ''.join(DNA_COMPLEMENT[b] for b in seq)

def transcribe(dna):
    return dna.replace('T', 'U')


def anticodon(codon):
    return ''.join(COMPLEMENT[b] for b in codon)


def draw_helix(molde):
    n           = len(molde)
    full_width  = 2 * n - 1 + len("  5'─") + len("─3'  ← codificante (a descubrir)")
    chunk       = n if console.width >= 80 and full_width <= console.width else 10

    console.print()
    for start in range(0, n, chunk):
        m = molde[start:start + chunk]
        c_row = "─".join(["?"] * len(m))
        m_row = "─".join(m)
        conn  = " ".join(["│"] * len(m))
        console.print(f"  [bold]5'[/bold]─[dim]{c_row}[/dim]─[bold]3'[/bold]  [dim]← codificante (a descubrir)[/dim]")
        console.print(f"     [dim]{conn}[/dim]")
        console.print(f"  [bold]3'[/bold]─[cyan]{m_row}[/cyan]─[bold]5'[/bold]  [dim]← molde[/dim]")
        console.print()


def draw_splicing(pre_mrna, intron):
    idx   = pre_mrna.find(intron)
    exon1 = pre_mrna[:idx]
    exon2 = pre_mrna[idx + len(intron):]
    pad   = len("5'─[") + len(exon1)
    cut   = "✂" + "─" * (len(intron) - 2) + "✂"
    join  = "─" * (len(intron) + 2)

    console.print()
    console.print(f"  [dim]pre-mRNA:[/dim]  5'─[[bold green]{exon1}[/bold green]]─[[bold red]{intron}[/bold red]]─[[bold green]{exon2}[/bold green]]─3'")
    console.print(f"             {' ' * pad}[dim]{cut}[/dim]  [dim]espliceosoma[/dim]")
    console.print(f"             {' ' * pad}[dim]└{'─' * (len(intron) - 2)}┘[/dim]")
    console.print()
    console.print(f"  [dim]   mRNA:[/dim]  5'─[[bold green]{exon1}[/bold green]]{join}[[bold green]{exon2}[/bold green]]─3'")
    console.print()


def draw_trna(codon, anticodon_seq, aa_name):
    w     = max(len(aa_name), 9)
    name  = aa_name.center(w)
    anti  = " ─ ".join(list(anticodon_seq))
    cod   = " ─ ".join(list(codon))
    conn  = " │   │   │"
    wave  = "~" * (w + 4)

    console.print()
    console.print(f"  [bold cyan].─{'─' * w}─.[/bold cyan]")
    console.print(f"  [bold cyan]│ {name} │[/bold cyan]")
    console.print(f"  [bold cyan]'─{'─' * w}─'[/bold cyan]")
    console.print(f"  [dim]{'│'.center(w + 4)}[/dim]")
    console.print(f"  [yellow]{anti.center(w + 4)}[/yellow]   [dim]← anticodon[/dim]")
    console.print(f"  [dim]{conn.center(w + 4)}[/dim]")
    console.print(f"  [yellow]{cod.center(w + 4)}[/yellow]   [dim]← codon[/dim]")
    console.print(f"  [dim]{wave}[/dim]")
    console.print(f"  [dim]{'(ARNm)'.center(w + 4)}[/dim]")
    console.print()


def ask(prompt, correct, lives, max_lives=3):
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
        show_lives(lives, max_lives)
        if lives == 0:
            console.print(f"  [red]Incorrecto. La respuesta era: [bold]{correct}[/bold][/red]")
        elif lives == 1:
            console.print("  [red]El organismo se debilita... es tu ultima oportunidad.[/red]")
        else:
            console.print(f"  [yellow]Incorrecto.[/yellow]")
    return False, lives


def show_sequence(seq, label, show_indices=True):
    if show_indices:
        console.print(f"\n[bold]{label}:[/bold]")
        chunk = 10
        for start in range(0, len(seq), chunk):
            bases = seq[start:start + chunk]
            pos_row   = "  ".join(f"{start + i:<2}" for i in range(len(bases)))
            bases_row = "  ".join(f"[bold yellow]{b}[/bold yellow] " for b in bases)
            console.print(f"  [dim]{pos_row}[/dim]")
            console.print(f"  {bases_row}")
            console.print()
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
    console.print(Panel("[bold]PARTE I: INTRODUCCION[/bold]", style="cyan", box=box.ROUNDED, expand=False))
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
    console.print(Panel("[bold]PARTE II: TRANSCRIPCION[/bold]", style="cyan", box=box.ROUNDED, expand=False))
    console.print("\nTe posicionas en el promotor. La doble hebra de ADN se abre ante vos.")
    console.print(Panel(
        "[bold]El ADN tiene dos hebras:[/bold]\n"
        "- [bold]Molde:[/bold] la hebra que lee la ARN Polimerasa II.\n"
        "- [bold]Codificante:[/bold] la complementaria a la molde (A↔T, G↔C).\n\n"
        "Paso 1: obtene la hebra codificante a partir de la molde.\n"
        "Paso 2: transcribila a ARNm reemplazando [bold red]T[/bold red] por [bold yellow]U[/bold yellow].\n\n"
        "[dim]Ejemplo  molde: TACGTA  ->  codificante: ATGCAT  ->  ARNm: AUGCAU[/dim]",
        box=box.ROUNDED, style="dim"
    ))

    molde = dna_complement(dna)
    pre_mrna = transcribe(dna)

    draw_helix(molde)

    def intentar(correct, paso, prompt_text, seq_label, seq):
        nonlocal lives
        console.print(f"\n[bold]Paso {paso}:[/bold]")
        show_sequence(seq, seq_label, show_indices=False)
        while lives > 0:
            answer = console.input(f"[bold cyan]{prompt_text}[/bold cyan]").strip().upper()
            if answer == correct:
                return True
            lives -= 1
            if lives == 0:
                console.print(f"  [red]Incorrecto. La respuesta era: [bold]{correct}[/bold][/red]")
            else:
                errors = [i for i in range(min(len(answer), len(correct))) if answer[i] != correct[i]]
                if len(answer) != len(correct):
                    console.print(f"  [yellow]Incorrecto. La longitud no coincide (esperaba {len(correct)} bases, escribiste {len(answer)}).[/yellow]")
                else:
                    console.print(f"  [yellow]Incorrecto. Hay {len(errors)} error(es) en las posiciones: {errors}[/yellow]")
                if lives == 1:
                    console.print("  [red]El organismo se debilita... es tu ultima oportunidad. Te queda 1 vida.[/red]")
                else:
                    console.print(f"  [yellow]Te quedan {lives} vida(s).[/yellow]")
        return False

    if not intentar(dna, 1, "Hebra codificante (A↔T, G↔C): ", "Hebra molde", molde):
        return None, lives
    console.print(f"  [bold green]Correcto![/bold green] Hebra codificante: [yellow]{dna}[/yellow]")

    if not intentar(pre_mrna, 2, "ARNm resultante (T→U): ", "Hebra codificante", dna):
        return None, lives
    console.print(f"\n[bold green]Correcto! ARN pre-maduro sintetizado:[/bold green] [yellow]{pre_mrna}[/yellow]")
    console.print("[dim]Pero el ARN aun no esta listo para salir del nucleo. Debe ser procesado...[/dim]\n")
    return pre_mrna, lives


def part2b_splicing(pre_mrna, intron, lives):
    console.print(Panel("[bold]PARTE III: SPLICING[/bold]", style="cyan", box=box.ROUNDED, expand=False))
    console.print("\nEl ARN pre-maduro no puede salir del nucleo todavia.")
    console.print("Una maquinaria molecular gigante lo reconoce")
    console.print("e identifica las regiones no codificantes llamadas [bold red]intrones[/bold red].\n")

    opciones = [
        "Eliminar los intrones y unir los exones",
        "Replicar el ADN en el nucleo",
        "Sintetizar proteinas en el ribosoma",
    ]
    random.shuffle(opciones)
    correcta = str(opciones.index("Eliminar los intrones y unir los exones") + 1)

    console.print("[bold]Pregunta:[/bold] Cual es la funcion del [bold cyan]espliceosoma[/bold cyan]?\n")
    for i, op in enumerate(opciones, 1):
        console.print(f"  {i}. {op}")

    ok, lives = ask("\nElegí (1-3): ", correcta, lives)
    if not ok:
        return None, lives

    console.print(f"\n[bold]Intron detectado:[/bold] [red]{intron}[/red]")
    console.print("El espliceosoma lo elimina y une los [bold green]exones[/bold green] entre si.")

    mature_mrna = pre_mrna.replace(intron, '', 1)
    draw_splicing(pre_mrna, intron)
    console.print("\n[dim]El ARNm maduro sale del nucleo hacia el ribosoma...[/dim]\n")
    console.input("[dim]Presiona ENTER para continuar...[/dim]")

    return mature_mrna, lives


def part3_translation(arnm, lives):
    console.print(Panel("[bold]PARTE IV: TRADUCCION[/bold]", style="cyan", box=box.ROUNDED, expand=False))
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
        prev = arnm[max(0, i-3):i]
        nxt  = arnm[i+3:i+6]
        console.print(f"  [dim]...{prev}[/dim][bold yellow]|{codon}|[/bold yellow][dim]{nxt}...[/dim]")
        console.print("  Un ARNt se acerca al ribosoma...")
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

        draw_trna(codon, anticodon_correcto, AA_NAMES.get(aa, aa))
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

    max_lives = lives
    console.print(f"\n[bold]Dificultad:[/bold] {difficulty.upper()} | ", end="")
    show_lives(lives, max_lives)

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
            mature_mrna, current_lives = part2b_splicing(pre_mrna, seq['intron'], current_lives)
            if current_lives <= 0 or mature_mrna is None:
                console.print(Panel(
                    "[bold]GAME OVER[/bold]\n\n"
                    "El espliceosoma no pudo procesar el ARN.\n"
                    "El organismo no pudo responder. La mision fracaso.",
                    style="bold red", box=box.DOUBLE
                ))
            else:
                protein, current_lives = part3_translation(mature_mrna, current_lives)
                if current_lives <= 0:
                    console.print(Panel(
                        "[bold]GAME OVER[/bold]\n\n"
                        "La traduccion fue interrumpida. La proteina quedo incompleta.\n"
                        "El organismo no pudo recuperarse. La mision fracaso.",
                        style="bold red", box=box.DOUBLE
                    ))
                else:
                    chain = "-".join(f"[bold white][{aa}][/bold white]" for aa in protein)
                    table = Table(title="Proteina sintetizada", box=box.ROUNDED, style="green")
                    table.add_column("Letra", style="bold white", justify="center")
                    table.add_column("Aminoacido", style="green")
                    for aa in protein:
                        table.add_row(aa, AA_NAMES.get(aa, aa))

                    console.print(Panel(
                        f"[bold]MISION CUMPLIDA![/bold]\n\n{seq['ending']}",
                        style="bold green", box=box.DOUBLE
                    ))
                    console.print(f"\n  {chain}\n")
                    console.print(table)
                    console.print(f"\n[dim]Vidas restantes: {current_lives}[/dim]\n")
                    solved.add(seq['nombre'])

        again = console.input("[bold cyan]Queres jugar de nuevo? (s/n): [/bold cyan]").strip().lower()
        if again != 's':
            console.print(Panel(
                "[bold]Hasta la proxima.[/bold]\nGracias por jugar :D",
                style="cyan", box=box.ROUNDED
            ))
            break
        console.print()


if __name__ == '__main__':
    main()
