"""
Utilities for working with GFF3 files.

"""


from petl.io import fromtsv
from petl.transform import skipcomments, rowlenselect, convert, pushheader
from urllib import unquote_plus
from petl.util import HybridRow, RowContainer
from petlx.interval import facetintervallookup, intervaljoin, intervalleftjoin
from petlx.tabix import fromtabix
import sys


def gff3_parse_attributes(attributes_string):
    """
    Parse a string of GFF3 attributes ('key=value' pairs delimited by ';') 
    and return a dictionary.
  
    .. versionadded:: 0.2
      
    """
    
    attributes = dict()
    fields = attributes_string.split(';')
    for f in fields:
        if '=' in f:
            key, value = f.split('=')
            attributes[unquote_plus(key).strip()] = unquote_plus(value.strip())
        elif len(f) > 0:
            # not strictly kosher
            attributes[unquote_plus(f).strip()] = True            
    return attributes


def convertgff3(tbl):

    # push header
    t1 = pushheader(tbl, ('seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes'))

    # skip comments
    t2 = skipcomments(t1, '#')

    # ignore any row not 9 values long (e.g., trailing fasta)
    t3 = rowlenselect(t2, 9)

    # parse attributes into a dict
    t4 = convert(t3, 'attributes', gff3_parse_attributes)

    # parse coordinates
    t5 = convert(t4, ('start', 'end'), int)

    return HybridRowView(t5)


def fromgff3(filename, region=None):
    """
    Extract feature rows from a GFF3 file. 

    .. versionadded:: 0.2

    .. versionchanged:: 0.15

    A region query string of the form '[seqid]' or '[seqid]:[start]-[end]' may be given
    for the ``region`` argument. If given, requires the GFF3 file to be bgzipped and
    tabix indexed.

    """

    if region is None:

        # parse file as tab-delimited
        tbl = fromtsv(filename)

    else:

        # extract via tabix
        tbl = fromtabix(filename, region=region)

    return convertgff3(tbl)


# TODO move this to petl.base?
class HybridRowView(RowContainer):
    
    def __init__(self, wrapped):
        self.wrapped = wrapped
        
    def cachetag(self):
        return self.wrapped.cachetag()
    
    def __iter__(self):
        it = iter(self.wrapped)
        fields = it.next()
        yield fields
        for row in it:
            yield HybridRow(row, fields, missing=None)
            
            
def gff3lookup(features, facet='seqid'):
    """
    Build a GFF3 feature lookup based on interval trees. See also 
    :func:`petlx.interval.facetintervallookup`.
    
    .. versionadded:: 0.2
    
    """
    
    return facetintervallookup(features, facet=facet, start='start', stop='end')


def gff3join(table, features, seqid='seqid', start='start', end='end', proximity=1):
    """
    Join with a table of GFF3 features. See also :func:`petlx.interval.intervaljoin`.
    
    .. versionadded:: 0.2
    
    """
    
    return intervaljoin(table, features, lstart=start, lstop=end, lfacet=seqid,
                        rstart='start', rstop='end', rfacet='seqid', 
                        proximity=proximity)

    
def gff3leftjoin(table, features, seqid='seqid', start='start', end='end', proximity=1):
    """
    Left join with a table of GFF3 features. See also :func:`petlx.interval.intervalleftjoin`.
    
    .. versionadded:: 0.2
    
    """
    
    return intervalleftjoin(table, features, lstart=start, lstop=end, lfacet=seqid,
                            rstart='start', rstop='end', rfacet='seqid', 
                            proximity=proximity)


from petlx.integration import integrate
integrate(sys.modules[__name__])

