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
from typing import List, Tuple
from numpy import mat
import rich
import typer

app = typer.Typer(short_help="Pre-processa arquivos de C, C++ e Java para enviar para o Verde")

class SuportedLanguages(str, Enum):
    Java = 'java'
    C = 'c'
    Cpp = 'cpp'


def _includeJava (fp: Path, dependecies_path: List[Path] = []) -> str:

    if not fp.is_file():
        raise FileNotFoundError(f'Arquivo {fp} não pode ser encontrado')

    rich.print(":yellow_circle:", f"[yellow]Lendo arquivo: [bold purple]{fp}[/bold purple] ...[/yellow]")

    saida = ""


    with open(fp) as arquivo:

        for dep in dependecies_path:
            if dep.is_file():
                deps = [dep]
            elif dep.is_dir():
                deps = [x for x in dep.iterdir()]
            else:
                raise FileNotFoundError(f'Arquivo ou pasta {fp} não pode ser encontrado')
        
            for d in deps:
                with open(d) as dep_file:
                    saida += f"""
//-----------------------Inicio da lib: {dep_file.name}-----------------------//
{_includeJava(dep_file)}
//-----------------------Fim da lib: {dep_file.name}-----------------------//"""
    
        for linha in arquivo:
            saida += linha

    return saida

    
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
def Precompilar (
    arquivo: Path,
    arquivo_saida: typer.FileTextWrite,
    dependencia : List[Path] = [],
    lang: SuportedLanguages = typer.Option(default=None, show_default=False, help="Qual linguagem vai ser preprocessada (será considerada a extensão do arquivo se não especificado).")) -> None:

    if lang == None:
        lang = arquivo.name.split('.')[-1]

    rich.print("[bold yellow]Tipo de arquivo:[/bold yellow]", f"[blue].{lang}[/blue]")

    rich.print("[bold green]Juntando arquivos...[/bold green]", ":page_facing_up:")


    match lang:
        case SuportedLanguages.C, SuportedLanguages.Cpp:
            arquivo_saida.write(_includeC(arquivo))
        case SuportedLanguages.Java:
            arquivo_saida.write(_includeJava(arquivo, dependecies_path=dependencia))
    
    

    rich.print("[bold green]Arquivos unidos com sucesso[/bold green]", ":white_check_mark:")


if __name__ == "__main__":
    app()

