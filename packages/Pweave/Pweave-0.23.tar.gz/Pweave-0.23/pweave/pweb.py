from __future__ import print_function, division, unicode_literals, absolute_import
import sys
import re
import copy
import io

from . import readers
from . import formatters
from .processors import PwebProcessors
from .config import rcParams

# unicode string type (from the six library)
if sys.version_info[0] == 2:
    text_type = unicode
else:
    text_type = str


class Pweb(object):
    """Processes a complete document

    :param file: ``string`` name of the input document.
    :param format: ``string`` output format from supported formats. See: http://mpastell.com/pweave/formats.html
    """

    # Shared across class instances
    chunkformatters = []
    chunkprocessors = []

    #: Pweave cache directory
    cachedir = 'cache'

    _mpl_imported = False

    def __init__(self, file=None, format="tex", shell="python"):

        #The source document
        self.source = file
        self.sink = None
        self.doctype = format
        self.parsed = None
        self.executed = None
        self.formatted = None
        self.isparsed = False
        self.isexecuted = False
        self.isformatted = False

        if "python" not in shell:
            rcParams["chunk"]["defaultoptions"]["engine"] = shell

        #: Use documentation mode?
        self.documentationmode = False

        self.Reader = readers.PwebReader
        self.setformat(self.doctype)

    def setformat(self, doctype='tex', Formatter=None):
        """Set output format for the document

        :param doctype: ``string`` output format from supported formats. See: http://mpastell.com/pweave/formats.html
        :param Formatter: Formatter class, can be used to specify custom formatters. See: http://mpastell.com/pweave/subclassing.html

        """
        #Formatters are needed  when the code is executed and formatted
        if Formatter is not None:
            self.formatter = Formatter(self.source)
            return
        #Get formatter class from available formatters
        try:
            self.formatter = formatters.PwebFormats.formats[doctype]['class'](self.source)
        except KeyError as e:
            raise Exception("Pweave: Unknown output format")

    def setreader(self, Reader=readers.PwebReader):
        """Set class reading for reading documents,
        readers can be used to implement different input markups"""
        if type(Reader) == str or type(Reader) == text_type:
            self.Reader = readers.PwebReaders.formats[Reader]['class']
        else:
            self.Reader = Reader

    def getformat(self):
        """Get current format dictionary. See: http://mpastell.com/pweave/customizing.html"""
        return self.formatter.formatdict

    def updateformat(self, dict):
        """Update existing format, See: http://mpastell.com/pweave/customizing.html"""
        self.formatter.formatdict.update(dict)

    def parse(self, string=None, basename="string_input"):
        """Parse document"""
        if string is None:
            parser = self.Reader(file=self.source)
        else:
            parser = self.Reader(string=string)
            self.source = basename
        parser.parse()
        self.parsed = parser.getparsed()
        self.isparsed = True

    def run(self, shell="python"):
        """Execute code in the document"""
        if type(shell) == str or type(shell) == text_type:
            Runner = PwebProcessors.formats[shell]['class']
        else:
            Runner = shell

        runner = Runner(copy.deepcopy(self.parsed), self.source, self.documentationmode, self.formatter.getformatdict())
        runner.run()
        self.executed = runner.getresults()
        self.isexecuted = True

    def format(self):
        """Format the code for writing"""
        if not self.isexecuted:
            self.run()
        self.formatter.setexecuted(copy.deepcopy(self.executed))
        self.formatter.format()
        self.formatted = self.formatter.getformatted()
        self.isformatted = True

    def write(self, action="Pweaved"):
        """Write formatted code to file"""
        if not self.isformatted:
            self.format()
        if self.sink is None:
            self.sink = self._basename() + '.' + self.formatter.getformatdict()['extension']
        f = io.open(self.sink, 'wt', encoding='utf-8')
        data = self.formatted.replace("\r", "")
        f.write(data)
        f.close()
        sys.stdout.write('%s %s to %s\n' % (action, self.source, self.sink))

    def _basename(self):
        return re.split("\.+[^\.]+$", self.source)[0]

    def weave(self, shell="python"):
        """Weave the document, equals -> parse, run, format, write"""
        if not self.isparsed:
            self.parse()
        self.run(shell)
        self.format()
        self.write()

    def tangle(self):
        """Tangle the document"""
        self.parse()
        target = self._basename() + '.py'
        code = [x for x in self.parsed if x['type'] == 'code']
        code = [x['content'] for x in code]
        f = open(target, 'w')
        f.write('\n'.join(code))
        f.close()
        sys.stdout.write('Tangled code from %s to %s\n' % (self.source, target))

    def _getformatter(self, chunk):
        """Call code from pweave.formatters and user provided formatters
        allows overriding default options for doc and code chunks
        the function needs to return a string"""
        #Check if there are custom functions in Pweb.chunkformatter
        f = [x for x in Pweb.chunkformatters if x.__name__ == (
            'format%(type)schunk' % chunk)]
        if f:
            return f[0](chunk)
        #Check built-in formatters from pweave.formatters
        if hasattr(formatters, ('format%(type)schunk' % chunk)):
            result = getattr(formatters, ('format%(type)schunk' % chunk))(chunk)
            return result
        #If formatter is not found
        if chunk['type'] == 'code' or chunk['type'] == 'doc':
            return chunk
        sys.stderr.write('UNKNOWN CHUNK TYPE: %s \n' % chunk['type'])
        return None
