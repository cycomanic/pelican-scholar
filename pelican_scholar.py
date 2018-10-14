"""
Pelican Scholar
==============

A Pelican plugin that populates the context with Google Scholar information.

"""
# Author of Pelican-Scholar: Jochen Schroeder <cycomanic@gmail.com>
# BSD

import logging
logger = logging.getLogger(__name__)
import os
import datetime
import scholarly

from pelican import signals

__version__ = '0.1.0'


def add_scholar(generator, metadata):
    """
    Populates context google scholar information

    Configuration
    -------------
    metadata['scholar_id']
        the google scholar id (can be found from the URL) to get information for

    Output
    ------
    generator.context['scholar_affiliation'] : str
    generator.context['scholar_cites_per_year']: list(tuple)
    generator.context['scholar_hindex']: int
    generator.context['scholar_hindex5y']: int
    generator.context['scholar_i10index']: int
    generator.context['scholar_i10index5y']: int
    generator.context['scholar_interests']: str
    generator.context['scholar_name']: str
    """

    author = scholarly.Author(metadata["scholar_id"])
    author = author.fill(get_publications=False)

    generator.context['scholar_affiliation'] = author.affiliation
    citations = [ (year, num) for year, num in author.cites_per_year.items()]
    generator.context['scholar_cites_per_year'] = citations
    cites_total = 0
    for i in range(len(citations)):
        cites_total += citations[i][1]
    generator.context['scholar_cites_total'] = cites_total
    generator.context['scholar_hindex']  = author.hindex
    generator.context['scholar_hindex5y'] = author.hindex5y
    generator.context['scholar_i10index'] = author.i10index
    generator.context['scholar_i10index5y'] = author.i10index5y
    generator.context['scholar_interests']  = author.interests
    generator.context['scholar_name'] = author.name
    generator.context['scholar_date'] = datetime.date.today().strftime("%m/%Y")

def register():
    signals.page_generator_context.connect(add_scholar)
