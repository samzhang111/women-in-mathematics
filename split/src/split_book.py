"""
Given a PDF, this code splits the PDF so that each set of pages between
bookmarks becomes its own PDF, with title given by the bookmark title.
"""

import fitz
import PyPDF2
import os
from pyprojroot.here import here
import re


def format_name(name: str) -> str:
    # Remove content in parentheses
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r"'", '', name)

    # Extract last and first name, assuming format "LAST, First"
    parts = name.split(',')
    if len(parts) < 2:
        return ""

    last_name = parts[0].strip(' .').lower()
    first_name = parts[1].strip(' .').split()[0].lower().strip(' .')

    return f"{last_name}_{first_name}"


def extract_bookmarks(pdf_path):
    doc = fitz.open(pdf_path)
    bookmarks = []

    for toc in doc.get_toc():
        level, title, page = toc
        bookmarks.append((title, page))  # Store title and page number

    return bookmarks


def split_pdf_by_bookmarks(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract bookmarks
    bookmarks = extract_bookmarks(pdf_path)

    if not bookmarks:
        print("No bookmarks found!")
        return

    # Load the PDF using PyPDF2
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        for i, (title, start_page) in enumerate(bookmarks):
            if start_page < 6:
                continue

            if len(title) == 1:
                continue

            # Normalize filename
            title = format_name(title)
            if len(title) == 0:
                continue

            # Determine the end page
            end_page = bookmarks[i + 1][1] if i + 1 < len(bookmarks) else total_pages

            # Create a new PDF writer
            writer = PyPDF2.PdfWriter()
            for page_num in range(start_page - 1, end_page - 1):  # PyPDF2 is zero-indexed
                writer.add_page(reader.pages[page_num])

            output_filename = os.path.join(output_folder, f"{title}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)

            print(f"Saved: {output_filename}")

# Usage
pdf_path = here("split/input/PioneeringWomenSupplement.pdf")
output_folder = here("split/output/")
split_pdf_by_bookmarks(pdf_path, output_folder)

