import logging
import sys
from pathlib import Path

from pypdf import PdfMerger, PdfReader, PdfWriter


def pdf_split(pdf_path, file_pages, filename: str = "output.pdf"):
    input_pdf = PdfReader(pdf_path)
    output_pdf = PdfWriter()

    total_pages = len(input_pdf.pages) - 1
    for page in file_pages:
        if int(page) > total_pages:
            logging.error("invalid page index : %s", page)
            exit(3)
        output_pdf.add_page(input_pdf.pages[int(page)])
    output_pdf.write(filename)


def pdf_merge(pdf_paths, filename: str = "output.pdf"):
    pdf_merger = PdfMerger()
    for path in pdf_paths:
        if not Path(path).exists:
            logging.error("invalid pdf file path : %s", path)
            exit(2)
        pdf_merger.append(path)
    pdf_merger.write(filename)


if __name__ == "__main__":
    match len(sys.argv):
        case 1:
            USAGE = "Usage: \n\tGet specific pages: pdf.py <pdf_file>\n\tMerge file: pdf.py <pdf_file> <pdf_file> <pdf_file>"
            logging.warning(USAGE)
            exit(1)
        case 2:
            pages = input("Pages to keep separate by coma: ").split(",")
            pdf_split(sys.argv[1], pages)
        case _:
            pdf_merge(sys.argv[1:])
    logging.info("output.pdf created or overwrited")
