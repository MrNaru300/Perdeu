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
from io import TextIOWrapper
from pathlib import Path
import re
from typing import List
import rich
import typer
import subprocess
import javalang

app = typer.Typer(short_help="Pre-processa arquivos de C, C++ e Java para enviar para o Verde")



class SuportedLanguages(str, Enum):
    Java = 'java'
    C = 'c'
    Cpp = 'cpp'


def _includeJava (arquivo: typer.FileText, output: typer.FileTextWrite, dependecies_path: List[Path] = []):


    rich.print(":yellow_circle:", f"[yellow]Lendo arquivo: [bold purple]{arquivo.name}[/bold purple] ...[/yellow]")

    #All package names maped to source files
    dependecies_srcs = {}


    #Find all dependencies source files
    for dp in dependecies_path:
        if dp.is_dir():
            for src_path in dp.glob('*/*.java'):
                #Maps a path into a package name
                dependecies_srcs[src_path.relative_to(dp).with_suffix('').replace('/', '.')] = src_path
        

    classes = [] #All classes
    imported = set() #All already imported packages
    tree = javalang.parse.parse(arquivo.read())

    for imp in tree.imports:

        if imp.path not in imported:
            if not imp.path.startswith("java."):
                if imp.path in dependecies_srcs:
                    with open(dependecies_srcs[imp.path], 'r') as dep_arq:
                        rich.print(":yellow_circle:", f"[yellow]Lendo arquivo: [bold purple]{Path.resolve(imp.path)}[/bold purple] ...[/yellow]")
                        #TODO Recursive imports
                else:
                    raise FileNotFoundError(f"Importação do Pacote {imp.path} não encontrado no CLASSPATH!")
        else:
            imported.add(imp.path)

    classes.extend(tree)


    
def _includeC (fp: Path, output : typer.FileTextWrite):

    if not fp.is_file():
        raise FileNotFoundError(f'Arquivo {fp} não pode ser encontrado')

    
    rich.print(":yellow_circle:", f"[yellow]Lendo arquivo: [bold purple]{fp}[/bold purple] ...[/yellow]")

    with open(fp) as arquivo:
        if not arquivo.readable():
            raise IOError(f'O Arquivo {fp} não pode ser lido')


        for linha in arquivo:
            match = re.match(r"^#\s*include\s*\"([^\"]*)\"", linha)

            if match:

                biblioteca = match.group(1)

                caminho = fp.parent.joinpath(biblioteca).resolve()

                output.write(f"//----------------------- Lib: {biblioteca}-----------------------//\n")
                _includeC(caminho, output)
                output.write("\n\n")

            else:
                output.write(linha)


@app.command(help="Pre-processa o arquivo adicionando as depencencias")
def Precompilar (
    arquivo: typer.FileText,
    arquivo_saida: typer.FileTextWrite = typer.Option(None, '-o', '--output'),
    dependencias : List[Path] = typer.Option([], '--dependencias', '-d',  help="Arquivos ou pastas contendo dependencias para serem incluidas no arquivo", envvar='CLASSPATH'),
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
            _includeC(arquivo, arquivo_saida)
        case SuportedLanguages.Java:
            _includeJava(arquivo, arquivo_saida, dependecies_path=dependencias)

    arquivo_saida.close()
    
    

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

