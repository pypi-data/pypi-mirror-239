### TECHREPORT ###
TECHREPORT_REQUIRED_TEMPLATE = """@techreport{{{citekey},
  author      = {{{author}}},
  title       = {{{title}}},
  institution = {{{institution}}},
  year        = {{{year}}}
}}"""


def make_techreport(citekey, author, title, institution, year, export=False):
    bib = TECHREPORT_REQUIRED_TEMPLATE.format(
        **{
            "citekey": citekey,
            "author": author,
            "title": title,
            "institution": institution,
            "year": year,
        }
    )
    if export:
        with open(f"`{citekey}`.bib", "w") as my_bib:
            my_bib.write(bib)

    return bib
