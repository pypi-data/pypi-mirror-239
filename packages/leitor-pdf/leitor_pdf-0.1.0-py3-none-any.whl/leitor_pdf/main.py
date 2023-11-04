from io import BufferedReader, StringIO
from pathlib import Path
from re import sub
from typing import List, Tuple, Union

import pdfplumber
from pdfminer.high_level import extract_text_to_fp
from PyPDF2 import PdfFileReader
from unidecode import unidecode

from leitor_pdf.exceptions import InvalidOptionException, TheFileIsnPdf


class LeitorPdf:
    @property
    def opcoes_de_extracao(self) -> Tuple[str]:
        """
        Returns:
            Opções de biblioteca para extrair o texto.
        """
        return (
            'pdfminer',
            'PyPDF2',
            'pdf_plumber',
        )

    def __clean_text(self, text: str) -> str:
        """
        Remove caracteres especiais do texto, acentuação, quebra de linha, cifrão, reduz espaçamento para um e deixa o texto minusculo

        Args:
            text (str): Texto que terá os caracteres removido.

        Returns:
            str: texto limpo
        """
        sem_acento: str = unidecode(text)
        sem_quebra_de_linha: str = sem_acento.replace('\n', '')
        tudo_minusculo: str = sem_quebra_de_linha.lower()
        unico_espacamento: str = sub(r'\s+', ' ', tudo_minusculo)
        sem_cifrao: str = sub(r'r\$', '', unico_espacamento)
        return sem_cifrao

    def extract_text_with_pypdf2(
        self, file_opened: BufferedReader, page_number: int = None
    ) -> str:
        """
        Extrai texto do PDF usando o lib PyPDF2

        Args:
            file_opened: path do pdf que terá o texto extraido
            page_number: caso deseje extrair uma pagina especifica, informar o numero, caso contrario o texto do PDF o texto do pdf todo

        Returns:
            texto do PDF

        Examples:
            >>> leitor = LeitorPdf()
            >>> BASE_DIR = Path(__file__).resolve().parent.parent
            >>> file = Path(BASE_DIR, 'tests', 'file_test', 'helloworld.pdf')
            >>> with open(file, "rb") as file_opened:     leitor.extract_text_with_pypdf2(file_opened)
            'Hello, world!\\n'
        """
        text_in_document: List[str] = []
        pdf_reader = PdfFileReader(file_opened)
        if not page_number:
            page_number = pdf_reader.numPages

        for i in range(page_number):
            page_obj = pdf_reader.getPage(i)
            text_in_document.append(page_obj.extractText())
        all_text = ' '.join(text_in_document)

        return all_text

    def _extract_text_with_pdfminer_high_level(
        self, file_opened: BufferedReader, page_number: List[int] = None
    ) -> str:
        """
        Extrai texto do PDF usando a lib pdfminer

        Args:
            file_opened: path do pdf que terá o texto extraido
            page_number: caso deseje extrair uma pagina especifica, informar o numero, caso contrario o texto do PDF o texto do pdf todo

        Returns:
            texto do PDF

        Examples:
            >>> leitor = LeitorPdf()
            >>> BASE_DIR = Path(__file__).resolve().parent.parent
            >>> file = Path(BASE_DIR, 'tests', 'file_test', 'helloworld.pdf')
            >>> with open(file, "rb") as file_opened:     leitor._extract_text_with_pdfminer_high_level(file_opened)
            'Hello, world!\\x0c'
        """
        output_string = StringIO()
        extract_text_to_fp(
            file_opened, output_string, page_numbers=page_number
        )
        return output_string.getvalue()

    def extract_text_with_pdfplumber(
        self, file_opened: BufferedReader, page_number: int = None
    ) -> str:
        """
        Extrai texto do PDF usando a lib pdfplumber

        Args:
            file_opened: path do pdf que terá o texto extraido
            page_number: caso deseje extrair uma pagina especifica, informar o numero, caso contrario o texto do PDF o texto do pdf todo

        Returns:
            str: texto extraido do pdf

        Examples:
            >>> leitor = LeitorPdf()
            >>> file = 'C:/Users/proc/GitHub/leitor_pdf/tests/file_test/helloworld.pdf'
            >>> with open(file, 'rb') as file:  leitor.extract_text_with_pdfplumber(file, 0)
            'Hello, world!'
        """
        text = ''
        with pdfplumber.open(file_opened) as pdf:
            if page_number:
                page = pdf.pages[page_number]
                text += page.extract_text()
            else:
                for page in pdf.pages:
                    text += page.extract_text()
        return text

    def _check_if_file_is_pdf(self, file: BufferedReader) -> None:
        """
        Checa se o arquivo é um pdf

        Args:
            file: arquivo que terá o texto extraído

        Returns:
            None: Se o arquivo for um PDF

        Raises:
            TheFileIsnPdf: Se o arquivo não for PDF
        """
        if not file.name.endswith('.pdf'):
            raise TheFileIsnPdf('O arquivo enviado nao é um pdf')

    def extract_text_from_file(
        self,
        file: Union[BufferedReader, str, Path],
        clean_text: bool,
        lib: str,
        page_number: int = None,
    ) -> str:
        """
        Extrai texto do PDF

        Args:
            file: arquivo que terá o texto extraído
            clean_text: se o texto sairá limpo (sem acento, espaco unico, texto em minusculo)
            lib: modo de extração de texto do PDF
            page_number: caso deseje extrair uma pagina especifica, informar o numero, caso contrario o texto do PDF o texto do pdf todo

        Returns:
            texto do PDF

        Examples:
            >>> BASE_DIR = Path(__file__).resolve().parent.parent
            >>> file = Path(BASE_DIR, 'tests', 'file_test', 'helloworld.pdf')
            >>> leitor = LeitorPdf()
            >>> leitor.extract_text_from_file(file, True, 'PyPDF2', 0)
            'hello, world!'
            >>> leitor.extract_text_from_file(file, False, 'pdfminer', 0)
            'Hello, world!\\x0c'
        """
        if type(file) == str or isinstance(file, Path):
            file = open(file, 'rb')
        try:
            self._check_if_file_is_pdf(file)
            text = self._extract_text(file, lib, page_number)
            return self.__clean_text(text) if clean_text else text
        finally:
            file.close()

    def _extract_text(
        self, file: BufferedReader, lib: str, page_number: int
    ) -> str:
        """
        Extrai texto do PDF de acordo com a lib escolhida

        Args:
            file: arquivo que terá o texto extraído
            lib: modo de extração de texto do PDF
            page_number: caso deseje extrair uma pagina especifica, informar o numero, caso contrario o texto do PDF o texto do pdf todo

        Returns:
            str: texto do PDF

        Raises:
            InvalidOptionException: Caso a lib escolhida nao esteja dentro das opcoes
        """
        if lib == 'PyPDF2':
            text: str = self.extract_text_with_pypdf2(file, page_number)
        elif lib == 'pdfminer':
            text: str = self._extract_text_with_pdfminer_high_level(
                file, [page_number]
            )
        elif lib == 'pdf_plumber':
            text: str = self.extract_text_with_pdfplumber(file, page_number)
        else:
            raise InvalidOptionException('Opção invalida')
        return text
