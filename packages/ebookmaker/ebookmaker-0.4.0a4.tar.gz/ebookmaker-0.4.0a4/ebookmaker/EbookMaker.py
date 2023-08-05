#!/usr/bin/env python
#  -*- mode: python; indent-tabs-mode: nil; -*- coding: iso-8859-1 -*-

"""

EbookMaker.py

Copyright 2009-2014 by Marcello Perathoner

Distributable under the GNU General Public License Version 3 or newer.

Stand-alone application to build EPUB and others out of html or rst.

"""

import argparse
import configparser
import collections
import datetime
import hashlib
import logging
import os.path
import sys

import six
from six.moves import builtins, cPickle

from libgutenberg.GutenbergGlobals import SkipOutputFormat
import libgutenberg.GutenbergGlobals as gg
from libgutenberg.Logger import debug, warning, error, exception
from libgutenberg import Logger, DublinCore
from libgutenberg import MediaTypes as mt

from ebookmaker import parsers
from ebookmaker import ParserFactory
from ebookmaker import Spider
from ebookmaker import WriterFactory
from ebookmaker.packagers import PackagerFactory
from ebookmaker import CommonCode

from ebookmaker.Version import VERSION


CONFIG_FILES = ['/etc/ebookmaker.conf', os.path.expanduser ('~/.ebookmaker')]

DEPENDENCIES = collections.OrderedDict ((
    ('all',             ('html', 'epub', 'kindle', 'pdf', 'txt', 'rst')),
    ('html',            ('html.images',    'html.noimages')),
    ('epub',            ('epub.images',    'epub.noimages')),
    ('kindle',          ('kindle.images',  'kindle.noimages')),
    ('pdf',             ('pdf.images',     'pdf.noimages')),
    ('txt',             ('txt.utf-8',      'txt.iso-8859-1', 'txt.us-ascii')),
    ('rst',             ('rst.gen', )),
    ('kindle.noimages', ('epub.noimages', )),
    ('kindle.images',   ('epub.images', )),
    ('html.noimages',   ('picsdir.noimages', )),
    ('html.images',     ('picsdir.images', )),
    ('pdf.noimages',    ('picsdir.noimages', )),
    ('pdf.images',      ('picsdir.images', )),
    ('rst.gen',         ('picsdir.images', )),
))

BUILD_ORDER = """
picsdir.images picsdir.noimages
rst.gen
txt.utf-8 txt.iso-8859-1 txt.us-ascii
html.images html.noimages
epub.images epub.noimages
kindle.images kindle.noimages
cover.small cover.medium
pdf.images pdf.noimages
qrcode rdf facebook twitter null""".split ()

FILENAMES = {
    'html.noimages':    '{id}-noimages-h.html',
    'html.images':      '{id}-h.html',

    'epub.noimages':    '{id}-epub.epub',
    'epub.images':      '{id}-images-epub.epub',

    'kindle.noimages':  '{id}-kindle.mobi',
    'kindle.images':    '{id}-images-kindle.mobi',

    'pdf.noimages':     '{id}-pdf.pdf',
    'pdf.images':       '{id}-images-pdf.pdf',

    'txt.utf-8':        '{id}-0.txt',
    'txt.iso-8859-1':   '{id}-8.txt',
    'txt.us-ascii':     '{id}.txt',

    'rst.gen':          '{id}-rst.rst',

    'picsdir.noimages': '{id}-noimages.picsdir',   # do we need this ?
    'picsdir.images':   '{id}-images.picsdir',     # do we need this ?
}

COVERPAGE_MIN_AREA = 200 * 200

def make_output_filename (dc, type_):
    """ Make a suitable filename for output type. """

    if dc.project_gutenberg_id:
        # PG book: use PG naming convention
        return FILENAMES[type_].format (id = dc.project_gutenberg_id)
    else:
        # not a PG ebook
        return FILENAMES[type_].format (id = gg.string_to_filename (dc.title)[:65])


def elect_coverpage (spider):
    """ Find first coverpage candidate that is not too small. """

    coverpage_found = False

    for p in spider.parsers:
        if 'coverpage' in p.attribs.rel:
            if coverpage_found:
                # keep the first one found, reset all others
                p.attribs.rel.remove ('coverpage')
                continue
            if hasattr (p, 'get_image_dimen'):
                dimen = p.get_image_dimen ()
                if (dimen[0] * dimen[1]) < COVERPAGE_MIN_AREA:
                    p.attribs.rel.remove ('coverpage')
                    warning ("removed coverpage candidate %s because too small (%d x %d)" %
                             (p.url, dimen[0], dimen[1]))
                    continue
            coverpage_found = True


def get_dc (parser):
    """ Get DC for book. """

    dc = DublinCore.GutenbergDublinCore ()
    try:
        dc.load_from_rstheader (parser.unicode_content ())
    except (ValueError, UnicodeError):
        try:
            debug ("No RST header found.")
            dc.load_from_parser (parser)
        except (ValueError, AttributeError, UnicodeError):
            try:
                debug ("No HTML/PG header found.")
                dc.load_from_pgheader (parser.unicode_content ())
            except (ValueError, UnicodeError):
                debug ("No PG header found.")

    if dc.project_gutenberg_id is None:
        # not a PG book, try DC metadata in HTML header
        dc = DublinCore.DublinCore ()
        dc.project_gutenberg_id = None
        try:
            dc.load_from_parser (parser)
        except (ValueError, UnicodeError):
            pass

    dc.source = parser.attribs.url
    dc.title = options.title or dc.title or 'NA'

    if options.author:
        dc.add_author (options.author, 'cre')
    if not dc.authors:
        dc.add_author ('NA', 'cre')

    dc.project_gutenberg_id = options.ebook or dc.project_gutenberg_id
    if dc.project_gutenberg_id:
        dc.opf_identifier = ('http://www.gutenberg.org/ebooks/%d' % dc.project_gutenberg_id)
    else:
        dc.opf_identifier = ('urn:mybooks:%s' %
                             hashlib.md5 (dc.source.encode ('utf-8')).hexdigest ())

    # We need a language to build a valid epub, so just make one up.
    if not dc.languages:
        dc.add_lang_id ('en')

    return dc


def add_local_options (ap):
    """ Add local options to commandline. """

    ap.add_argument (
        '--version',
        action='version',
        version = "%%(prog)s %s" % VERSION
    )

    ap.add_argument (
        "--make",
        dest    = "types",
        choices = CommonCode.add_dependencies (['all'], DEPENDENCIES),
        default = ['all'],
        action  = 'append',
        help    = "output type (default: all)")

    ap.add_argument (
        "--max-depth",
        metavar = "LEVELS",
        dest    = "max_depth",
        type    = int,
        default = 1,
        help    = "go how many levels deep while recursively retrieving pages. " +
        "(0 == infinite) (default: %(default)s)")

    ap.add_argument (
        "--include",
        metavar = "GLOB",
        dest    = "include_urls",
        default = [],
        action  = "append",
        help    = "include urls (repeat for more) (default: urls under the same directory)")

    ap.add_argument (
        "--exclude",
        metavar = "GLOB",
        dest    = "exclude_urls",
        default = [],
        action  = "append",
        help    = "exclude urls from included urls (repeat for more) (default: none)")

    ap.add_argument (
        "--include-mediatype",
        metavar = "GLOB/GLOB",
        dest    = "include_mediatypes",
        default = mt.TEXT_MEDIATYPES | mt.AUX_MEDIATYPES,
        action  = "append",
        help    = "include mediatypes (repeat for more) (eg. 'image/*') " +
        "(default: most common text mediatypes)")

    ap.add_argument (
        "--exclude-mediatype",
        metavar = "GLOB/GLOB",
        dest    = "exclude_mediatypes",
        default = [],
        action  = "append",
        help    = "exclude this mediatype from included mediatypes " +
        "(repeat for more)")

    ap.add_argument (
        "--input-mediatype",
        metavar = "MEDIATYPE",
        dest    = "input_mediatype",
        default = None,
        help    = "mediatype of input url (default: http response else file extension)")

    ap.add_argument (
        "--mediatype-from-extension",
        dest    = "mediatype_from_extension",
        action  = "store_true",
        default = False,
        help    = "guess all mediatypes from file extension, overrides http response")

    ap.add_argument (
        "--rewrite",
        metavar = "from>to",
        dest    = "rewrite",
        default = [],
        action  = "append",
        help    = "rewrite url eg. 'http://www.example.org/>http://www.example.org/index.html'")

    ap.add_argument (
        "--title",
        dest    = "title",
        default = None,
        help    = "ebook title (default: from meta)")

    ap.add_argument (
        "--author",
        dest    = "author",
        default = None,
        help    = "author (default: from meta)")

    ap.add_argument (
        "--ebook",
        dest    = "ebook",
        type    = int,
        default = 0,
        help    = "ebook no. (default: from meta)")

    ap.add_argument (
        "--output-dir",
        metavar  = "OUTPUT_DIR",
        dest    = "outputdir",
        default = "./",
        help    = "output directory (default: ./)")

    ap.add_argument (
        "--output-file",
        metavar  = "OUTPUT_FILE",
        dest    = "outputfile",
        default = None,
        help    = "output file (default: <title>.epub)")

    ap.add_argument (
        "--validate",
        dest     = "validate",
        action   = "count",
        help     = "validate epub through epubcheck")

    ap.add_argument (
        "--section",
        metavar  = "TAG.CLASS",
        dest     = "section_tags",
        default  = [],
        action   = "append",
        help     = "split epub on TAG.CLASS")

    ap.add_argument (
        "--packager",
        dest    = "packager",
        choices = ['ww', 'gzip'],
        default = None,
        help    = "PG internal use only: which packager to use (default: none)")

    ap.add_argument (
        "--jobs",
        dest    = "is_job_queue",
        action  = "store_true",
        help    = "PG internal use only: read pickled job queue from stdin")

    ap.add_argument (
        "--extension-package",
        metavar  = "PYTHON_PACKAGE",
        dest    = "extension_packages",
        default = [],
        action  = "append",
        help    = "PG internal use only: load extensions from package")

    ap.add_argument (
        "url",
        help    = "url of file to convert")


def open_log (path):
    """ Open a logfile in the output directory. """

    handler = logging.FileHandler (path, "a")
    handler.setFormatter (Logger.CustomFormatter (Logger.LOGFORMAT))
    handler.setLevel (logging.DEBUG)
    logging.getLogger ().addHandler (handler)
    return handler


def close_log (handler):
    """ Close logfile handler. """

    logging.getLogger ().removeHandler (handler)
    handler.close ()


def do_job (job):
    """ Do one job. """

    log_handler = None
    Logger.ebook = job.ebook

    for job.type in job.types:

        debug ('=== Building %s ===' % job.type)
        if job.logfile:
            log_handler = open_log (os.path.join (job.outputdir, job.logfile))

        job.maintype, job.subtype = os.path.splitext (job.type)

        try:
            if job.url:
                spider = Spider.Spider ()
                spider.include_urls += (options.include_urls or
                                        [os.path.dirname (job.url) + '/*'])

                spider.include_mediatypes += options.include_mediatypes
                if job.subtype == '.images' or job.type == 'rst.gen':
                    spider.include_mediatypes.append ('image/*')

                spider.exclude_urls += options.exclude_urls

                spider.exclude_mediatypes += options.exclude_mediatypes

                spider.max_depth = options.max_depth or six.MAXSIZE

                for rewrite in options.rewrite:
                    from_url, to_url = rewrite.split ('>')
                    spider.add_redirection (from_url, to_url)

                attribs = parsers.ParserAttributes ()
                attribs.url = job.url
                attribs.id = 'start'
                if options.input_mediatype:
                    attribs.orig_mediatype = attribs.HeaderElement.from_str (
                        options.input_mediatype)

                spider.recursive_parse (attribs)
                elect_coverpage (spider)
                job.url = spider.redirect (job.url)
                job.base_url = job.url
                job.dc = job.dc or get_dc (spider.parsers[0]) # or id == 'start'
                job.spider = spider

            # FIXME: job should not contain temporary entries like outputfile or type
            if len (job.types) > 1:
                job.outputfile = None
            job.outputfile = job.outputfile or make_output_filename (job.dc, job.type)

            writer = WriterFactory.create (job.maintype)
            writer.build (job)

            if options.validate:
                writer.validate (job)

            packager = PackagerFactory.create (options.packager, job.type)
            if packager:
                packager.package (job)

            if job.type == 'html.images':
                # FIXME: hack for push packager
                job.html_images_list = list (job.spider.aux_file_iter ())

        except SkipOutputFormat as what:
            warning ("%s" % what)

        except Exception as what:
            exception ("%s" % what)

        if log_handler:
            close_log (log_handler)
            log_handler = None


def config ():
    """ Process config files and commandline params. """

    ap = argparse.ArgumentParser (prog = 'EbookMaker')
    CommonCode.add_common_options (ap, CONFIG_FILES[1])
    add_local_options (ap)

    options = CommonCode.parse_config_and_args (
        ap,
        CONFIG_FILES[0],
        {
            'proxies' : None,
            'xelatex' : 'xelatex',
            'mobigen' : 'kindlegen',
            'groff'   : 'groff',
            'rhyming_dict': None,
            'timestamp': datetime.datetime.today ().isoformat ()[:19],
        }
    )

    builtins.options = options
    builtins._ = CommonCode.null_translation

    if '://' not in options.url:
        options.url = os.path.abspath (options.url)


def main ():
    """ Main program. """

    try:
        config ()
    except configparser.Error as what:
        error ("Error in configuration file: %s", str (what))
        return 1

    Logger.set_log_level (options.verbose)

    options.types = CommonCode.add_dependencies (options.types, DEPENDENCIES, BUILD_ORDER)
    debug ("Building types: %s" % ' '.join (options.types))

    ParserFactory.load_parsers ()
    WriterFactory.load_writers ()
    PackagerFactory.load_packagers ()

    if options.is_job_queue:
        job_queue = cPickle.load (sys.stdin.buffer) # read bytes
    else:
        j = CommonCode.Job ()
        j.ebook = options.ebook
        j.url = options.url
        j.types = options.types
        j.outputdir = options.outputdir
        j.outputfile = options.outputfile
        j.html_images_list = []
        job_queue = [j]

    for j in job_queue:
        do_job (j)

    packager = PackagerFactory.create (options.packager, 'push')
    if packager:
        # HACK: the WWers ever only convert one ebook at a time
        job = job_queue[0]
        job.outputfile = '%d-final.zip' % (job.dc.project_gutenberg_id)
        packager.package (job)

    return 0


if __name__ == "__main__":
    sys.exit (main ())
