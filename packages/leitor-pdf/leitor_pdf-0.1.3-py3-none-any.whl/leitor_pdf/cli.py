from rich.console import Console
from typer import Typer

from leitor_pdf.main import LeitorPdf

console = Console()
app = Typer()


leitor = LeitorPdf()


@app.command('read_file')
def leitor_pdf(tipo_leitor: str, path: str):
    print(leitor.extract_text_from_file(path, True, tipo_leitor))


@app.command('list_options')
def leitor_pdf():
    for index, opcao in enumerate(leitor.opcoes_de_extracao, 1):
        print('{} - {}'.format(index, opcao))
