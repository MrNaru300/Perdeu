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


import re
import sys
import os
import typer


def FormatarCaminho(start: str, relpath: str):
    """
    Junta o caminho inicial com o caminho relativo
    """


    while "../" in relpath:
        relpath = relpath.split("/")[1:]
        relpath = "/".join(relpath)
        start = os.path.split(start)[0]

    while "./" in relpath:
        relpath = relpath.split("/")[1:]
        relpath = "/".join(relpath)


    return os.path.join(start, relpath)


def AcharLib (linha: str, fp: str) -> str:
    match = re.match(r"^#\s*include\s*\"(.*)\"", linha)

    saida = ""

    if match:

        biblioteca = match.group(1)

        caminho = FormatarCaminho(os.path.split(os.path.abspath(fp))[0], biblioteca)

        saida += f"//-----------------------Inicio da lib: {biblioteca}-----------------------//\n"
        saida += f"{LerArquivo(caminho)}\n"
        saida += f"//-----------------------Fim da lib: {biblioteca}-----------------------//\n"

    return saida



        
def LerArquivo (fp: str) -> str:

    if not os.path.exists(fp):
        raise FileNotFoundError(f'Arquivo {fp} não pode ser encontrado')

    saida = ""

    
    print(f"Lendo arquivo: {fp} ...")

    with open(fp) as arquivo:
        if not arquivo.readable():
            raise IOError(f'O Arquivo {fp} não pode ser lido')


        for linha in arquivo:

            saida += AcharLib(linha, fp) or linha

    return saida



def Precompilar (arquivo: str, arquivo_saida: str, overwrite: bool = False) -> None:

    if not overwrite and os.path.exists(arquivo_saida):
        raise FileExistsError(f'O arquivo "{arquivo_saida}" já existe')


    with open(arquivo_saida, 'w') as saida:
        if not saida.writable():
            raise IOError(f'O Arquivo "{arquivo_saida}" não pode ser escrito')

        texto = LerArquivo(arquivo)

        saida.write(texto)
            




if __name__ == "__main__":
        
    if len(sys.argv) < 2:
        raise ValueError("Nome do arquivo não foi fornecido")

    NomeArquivo = sys.argv[1]

    if not os.path.exists(NomeArquivo):
        raise FileNotFoundError(f"O arquivo {NomeArquivo} não existe")

    NomeSaida = "out.cpp" if len(sys.argv) < 3 else sys.argv[2]

    


    print(__doc__)


    print("Juntando arquivos...")
    
    Precompilar(NomeArquivo, NomeSaida, True)

    print("Arquivos unidos com sucesso")

