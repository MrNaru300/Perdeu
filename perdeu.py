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


from calendar import c
from enum import Enum
from io import TextIOWrapper
from pathlib import Path
import re
from typing import List, Tuple
import rich
import typer
import subprocess

app = typer.Typer(short_help="Pre-processa arquivos de C, C++ e Java para enviar para o Verde")

class SuportedLanguages(str, Enum):
    Java = 'java'
    C = 'c'
    Cpp = 'cpp'


def _includeJava (arquivo: TextIOWrapper, output: TextIOWrapper, dependecies_path: List[Path] = []):


    rich.print(":yellow_circle:", f"[yellow]Lendo arquivo: [bold purple]{arquivo.name}[/bold purple] ...[/yellow]")

    if not arquivo.readable():
        raise IOError(f"Arquivo {arquivo.name} não pode ser lido")
    
    arquivo_completo = arquivo.read()

    #classes_re = re.compile(r'(?:((?:public)|(?:abstract)|(?:final))\s+)?(class\s+([\w\d]+)\s+(?:[\w\d]+\s+)*{(?:[^{}]*(?:{[^{}]*})*)+\s*})')
    imports_re = re.compile(r'import +((?:(?:[\w\d*]+)\.?)*);')

    dep_classes = {}
    imports = set(re.findall(imports_re, arquivo_completo))

    while dependecies_path:
        dependecy_path = dependecies_path.pop()
        if dependecy_path.is_dir():
            dependecies_path.extend(dependecy_path.iterdir())
            continue
        elif not dependecy_path.is_file():
            raise FileNotFoundError(f'Arquivo ou pasta {arquivo} não pode ser encontrado')

        with open(dependecy_path) as dependency_file:
            file_content = dependency_file.read()
            rich.print(":yellow_circle:", f"[yellow]Lendo arquivo: [bold purple]{Path.resolve(dependecy_path)}[/bold purple] ...[/yellow]")

            dep_classes[dependecy_path] = re.finditer(classes_re, file_content)
            imports.update(re.findall(imports_re, file_content))


    for imp in imports:
        if imp.startswith('java'):
            output.write(f'import {imp};\n')

    for line in arquivo_completo:
        if not line.startswith('import'):
            output.write(line)
       

    for dependecy_path, classes in dep_classes.items():
        for _class in classes:
            output.write(_class.group(0) + '\n\n')


    
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
    arquivo: typer.FileText,
    arquivo_saida: typer.FileTextWrite = typer.Option(None, '-o', '--output'),
    dependencia : List[Path] = typer.Option([], '--dependencia', '-d', help="Arquivos ou pastas contendo dependencias para serem incluidas no arquivo"),
    lang: SuportedLanguages = typer.Option(None, '--lang', '-l', show_default=False, help="Qual linguagem vai ser preprocessada (será considerada a extensão do arquivo se não especificado).")
    ) -> None:

    if lang == None:
        lang = arquivo.name.split('.')[-1]

    if arquivo_saida == None:
        arquivo_saida = open("saida."+lang, "w")


    rich.print("[bold yellow]Tipo de arquivo:[/bold yellow]", f"[blue].{lang}[/blue]")
    rich.print("[bold yellow]Arquivo de saida:[/bold yellow]", f"[blue]{arquivo_saida.name}[/blue]")

    rich.print("[bold green]Juntando arquivos...[/bold green]", ":page_facing_up:")


    match lang:
        case SuportedLanguages.C, SuportedLanguages.Cpp:
            arquivo_saida.write(_includeC(arquivo))
        case SuportedLanguages.Java:
            _includeJava(arquivo, arquivo_saida, dependecies_path=dependencia)
    
    

    rich.print("[bold green]Arquivos unidos com sucesso[/bold green]", ":white_check_mark:")

@app.command(help="compila ")
def compilar(
    path : Path,
    output_file: Path = "",
    CCompiler : str ='gcc',
    CppCompiler : str = 'g++',
    JavaCompiler : str ='java',
    ):

    paths = [path]

    while paths:
        file = paths.pop()
        if file.is_dir():
            paths.extend(file.resolve().iterdir())
        elif file.is_file():
            match file.suffix.lstrip('.'):
                case SuportedLanguages.Java:
                    subprocess.call([JavaCompiler, path]
                    .extend((['-d', output_file]) if output_file != "" else []))
                case SuportedLanguages.C:
                    subprocess.call([CCompiler, path]
                    .extend((['-o', output_file]) if output_file != "" else []))
                case SuportedLanguages.Cpp:
                    subprocess.call([CppCompiler, path]
                    .extend((['-o', output_file]) if output_file != "" else []))
                    
            



@app.command(help="observa atualização dos diretórios e recompila os arquivos")
def watch(
    CCompiler : str ='gcc',
    CppCompiler : str = 'g++',
    JavaCompiler='java'
    ):
    pass

if __name__ == "__main__":
    app()

