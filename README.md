# Pioneering Women in American Mathematics: The Pre-1940 PhD’s

This is an analysis of the biographies included in the book [Pioneering Women in American Mathematics: The Pre-1940 PhD’s](https://bookstore.ams.org/hmath-34) by Judy Green and Jeanne LaDuke, which includes comprehensive biographies written about every single American woman who received a PhD in the mathematics before the 1940s.

The tasks are run in the following order:
1. split: splits the PDF of the book's [supplementary materials](https://www.ams.org/publications/authors/books/postpub/hmath-34-PioneeringWomen.pdf) into chapters.
2. extract: extracts plain text from each chapter PDF.
3. parse: uses the OpenAI API to parse each chapter text, pulling out biographical information like degrees and employment.
4. join: joins the parsed data together into CSVs.
5. analyze: looks at the parsed data.
