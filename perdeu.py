"""
    O Arquivo de Pré-compilação para o site do Verde-Puc

    Authors:
        Lusantisuper:
            GitHub: https://github.com/lusantisuper
            Youtube: https://www.youtube.com/user/MrNaru300

        MrNaru300:
            GitHub: https://github.com/MrNaru300


    @@@@@@@@@@@@@@@@@`.--::////::--.`@@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@./+oooooooooooooooo+/.@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@`+oooooooooooooooooo+`@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@-oooooooooooooooooo-@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@:oooooooooooooooo/@@@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@+oooooooooooooo+`@@@@@@@@@@@@@@@@
    @@@`/`@@@@@@@@@@@.oooooooooooooo.@@@@@@@@@@@`/`@@@
    @@`+o/@@@@@@@@@@@@-oooooooooooo:@@@@@@@@@@@@/o+`@@
    @@+ooo/@@@@@@@@@@@@/oooooooooo/@@@@@@@@@@@@:ooo+@@
    @-ooooo:@@@@@@@@@@@`+oooooooo+`@@@@@@@@@@@-ooooo-@
    @+oooooo.@@@@@@@@@@@.oooooooo-@@@@@@@@@@@.oooooo+@
    `ooooooo+.@@@@@@@@@@@:oooooo/@@@@@@@@@@@`+ooooooo`
    `oooooooo+`@@@@@@@@@@@+oooo+`@@@@@@@@@@`+oooooooo`
    `ooooooooo/@@@@@@@@@@@.+ooo.@@@@@@@@@@@/ooooooooo`
    @/ooooooooo/@@@@@@@@@@@:oo:@@@@@@@@@@@/ooooooooo/@
    @.oooooooooo:@@@@@@@@@@@++`@@@@@@@@@@-oooooooooo.@
    @@/oooooooooo-@@@@@@@@@@-:@@@@@@@@@@.oooooooooo/@@
    @@`+ooooooooo+.@@@@@@@@@@`@@@@@@@@@.+ooooooooo+`@@
    @@@`/ooooooooo+`@@@@@@@@@@@@@@@@@@`+ooooooooo/`@@@
    @@@@@:ooooooooo+@@@@@@@@@@@@@@@@@@/ooooooooo:@@@@@
    @@@@@@`/oooooooo/@@@@@@@@@@@@@@@@/oooooooo/`@@@@@@
    @@@@@@@@`:+oooooo:@@@@@@@@@@@@@@:oooooo+:`@@@@@@@@
    @@@@@@@@@@`-/+oooo-@@@@@@@@@@@@-oooo+/-`@@@@@@@@@@
    @@@@@@@@@@@@@@.-/++.@@@@@@@@@@.++/-.@@@@@@@@@@@@@@
    @@@@@@@@@@@@@@@@@@@`@@@@@@@@@@`@@@@@@@@@@@@@@@@@@@
"""


from enum import Enum
from pathlib import Path
import re
import os
from typing import List
import rich
import typer

app = typer.Typer(epilog=__doc__, help="Pre-processa arquivos de C, C++ e Java para enviar para o Verde")
precomile = typer.Typer()

class SuportedLanguages(str, Enum):
    Java = 'Java'
    C = 'C'
    Cpp = 'C++'




        
def _includeC (fp: Path) -> str:

    if not fp.is_file():
        raise FileNotFoundError(f'Arquivo {fp} não pode ser encontrado')

    saida = ""

    
    rich.print(":yellow_circle:", f"[yellow]Lendo arquivo: [bold purple]{fp}[/bold purple] ...[/yellow]")

    with open(fp) as arquivo:
        if not arquivo.readable():
            raise IOError(f'O Arquivo {fp} não pode ser lido')


        for linha in arquivo:
            match = re.match(r"^#\s*include\s*\"([^\"]*)\"", linha)

            if match:

                biblioteca = match.group(1)

                caminho = fp.parent.joinpath(biblioteca).resolve()

                saida += f"//-----------------------Inicio da lib: {biblioteca}-----------------------//\n"
                saida += f"{_includeC(caminho)}\n"
                saida += f"//-----------------------Fim da lib: {biblioteca}-----------------------//\n"

            else:
                saida += linha

    return saida


@app.command(help="Pre-processa o arquivo adicionando as depencencias")
def Precompilar (arquivo: Path,
    arquivo_saida: typer.FileTextWrite,
    dependencias : List[Path] = [],
    lang: SuportedLanguages = SuportedLanguages.C) -> None:
        


    rich.print("[bold green]Juntando arquivos...[/bold green]", ":page_facing_up:")


    match lang:
        case SuportedLanguages.C, SuportedLanguages.Cpp:
            arquivo_saida.write(_includeC(arquivo))
        case SuportedLanguages.Java:
            raise NotImplementedError("Java ainda não implementado")
    
    

    rich.print("[bold green]Arquivos unidos com sucesso[/bold green]", ":white_check_mark:")


if __name__ == "__main__":
    app()

