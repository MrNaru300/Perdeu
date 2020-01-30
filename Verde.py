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

    


def AcharLibs_C (fp: str, recursive:bool = True) -> tuple:
    """

    Retorna uma tupla de bibliotecas locais
    de um arquivo escrito na liguagem C ou C++

    Args:
     fp (str): O caminho do arquivo para ser lido
     recursive (bool): Procura As bibliotecas locais dentro das bibliotecas importadas

    Return:
     Retorna uma tupla dos cominhos absolutos das bibliotecas

     """
    
    if not os.path.exists(fp):
        raise FileNotFoundError(f"Arquivo {fp} não encontrado")

    bibliotecas = []

    fpDir = os.path.split(os.path.abspath(fp))[0]

    with open(fp, "r") as arquivo:
        
        for linha in arquivo:
            match = re.match(r"^#\s*include\s*\"(.*)\"", linha)

            if match:

                biblioteca = match.group(1)

                libDir = FormatarCaminho(fpDir, biblioteca)

                if not libDir in bibliotecas:
                    bibliotecas.append(libDir)

                    if recursive:
                        
                        bibliotecas = [*bibliotecas, *filter(lambda x: not x in bibliotecas, AcharLibs_C(libDir, recursive=True))]
                   

    return tuple(bibliotecas)


def _JuntarArquivos(fp: str, overwrite: bool = False, *arquivos:str) -> None:
    """
    Junta todos os arquivos em um único arquivos para pré-compilação

    Args:
        fp (str): o local do arquivo final
        overwrite (bool) = False: Sobreescrever o arquivo se já existir
        *arquivos (str): Os caminhos dos arquivos
    """

    with open(fp, "w") as saida:
        for arquivoDir in arquivos:

            with open(arquivoDir, "r") as arquivo:

                saida.write(f"//----------------{os.path.split(arquivoDir)[1]}----------------//\n\n")

                for linha in arquivo:
                    if not re.match(r"^#\s*include\s*\"(.*)\"", linha):
                        saida.write(linha)
                saida.write("\n\n")



if __name__ == "__main__":
        
    if len(sys.argv) < 2:
        raise ValueError("Nome do arquivo não foi fornecido")

    NomeArquivo = sys.argv[1]

    if not os.path.exists(NomeArquivo):
        raise FileNotFoundError(f"O arquivo {NomeArquivo} não existe")

    LocalArquivo = os.path.split(os.path.abspath(NomeArquivo))[0]
    NomeSaida = "out.cpp" if len(sys.argv) < 3 else sys.argv[2]

    


    print(__doc__)


    bibliotecas = AcharLibs_C(NomeArquivo, True)

    print("Bibliotecas encontradas:", end='\n\n')
    for lib in bibliotecas:
        print(f"*{os.path.relpath(lib, LocalArquivo)}")

    print("")
    print("Juntando arquivos...")
    
    _JuntarArquivos(NomeSaida, True, *bibliotecas, os.path.join(LocalArquivo, NomeArquivo))

    print("Arquivos unidos com sucesso")

