"""
C interface to Easel
"""

from libc.stdio cimport FILE
from libc.stdint cimport int64_t, uint16_t

__all__ = ['read_seq_file', 'create_ssi', 'open_ssi', 'FMT_UNKNOWN',
           'FMT_FASTA', 'read_fasta', 'write_fasta', 'EaselSequence']

# External declarations
cdef extern from "unistd.h":
    ctypedef unsigned off_t

cdef extern from "easel.h":
    ctypedef int ESL_DSQ

cdef extern from "esl_sq.h":
    ctypedef struct ESL_SQ:
        char *name
        char *acc
        char *desc
        char *seq
        ESL_DSQ *dsq
        char *ss
        int64_t n # Length of sequence and ss
        int64_t L # Source sequence length
        int64_t idx

        # Offsets
        off_t doff
        off_t roff

    ESL_SQ *esl_sq_Create()
    ESL_SQ *esl_sq_CreateFrom(char *name, char *seq, char *desc,
            char *acc, char *ss)
    int esl_sq_Reuse(ESL_SQ *sq)
    void esl_sq_Destroy(ESL_SQ *sq)

    # Manipulations
    int esl_sq_ReverseComplement(ESL_SQ *sq)
    int esl_sq_Copy(ESL_SQ *src, ESL_SQ *dst)

    # Setters
    int esl_sq_SetName(ESL_SQ *sq,  char *name)
    int esl_sq_SetAccession(ESL_SQ *sq,  char *acc)
    int esl_sq_SetDesc(ESL_SQ *sq,  char *desc)
    int esl_sq_SetSource(ESL_SQ *sq,  char *source)

cdef extern from "esl_sqio.h":
    ctypedef struct ESL_SQASCII_DATA:
        ESL_SSI *ssi
    ctypedef union ESL_SQDATA:
        ESL_SQASCII_DATA ascii

    ctypedef struct ESL_SQFILE:
        char *filename
        int format
        ESL_SQDATA data

    int esl_sqfile_Open(char *seqfile, int fmt, char *env,
            ESL_SQFILE **ret_sqfp)
    int esl_sqfile_OpenSSI(ESL_SQFILE *sqfp, char *ssifile_hint)
    void esl_sqfile_Close(ESL_SQFILE *sqfp)

    int esl_sqio_Fetch(ESL_SQFILE *sqfp, char *key, ESL_SQ *sq)
    int esl_sqio_Read(ESL_SQFILE *sqfp, ESL_SQ *sq)
    int esl_sqio_ReadInfo(ESL_SQFILE *sqfp, ESL_SQ *sq)
    int esl_sqio_Write(FILE *fp, ESL_SQ *s, int format, int update)

cdef extern from "esl_ssi.h":
    ctypedef struct ESL_SSI:
        pass

    ctypedef struct ESL_NEWSSI:
        char *ssifile
        FILE *ssifp

    # Creating
    int esl_newssi_Open(char *ssifile, int allow_overwrite,
            ESL_NEWSSI **ret_newssi)
    int esl_newssi_AddFile(ESL_NEWSSI *ns, char *filename, int fmt,
            uint16_t* ret_fh)
    int esl_newssi_AddKey(ESL_NEWSSI *ns, char *key, int fh, int r_off,
            int d_off, long L)
    int esl_newssi_Write(ESL_NEWSSI *ns)
    void esl_newssi_Close(ESL_NEWSSI *ns)

cdef enum EaselErrors:
    eslOK = 0    # no error/success
    eslFAIL = 1    # failure
    eslEOL = 2    # end-of-line (often normal)
    eslEOF = 3    # end-of-file (often normal)
    eslEOD = 4    # end-of-data (often normal)
    eslEMEM = 5    # malloc or realloc failed
    eslENOTFOUND = 6    # file or key not found
    eslEFORMAT = 7    # file format not correct
    eslEAMBIGUOUS = 8    # an ambiguity of some sort
    eslEDIVZERO = 9    # attempted div by zero
    eslEINCOMPAT = 10    # incompatible parameters
    eslEINVAL = 11    # invalid argument/parameter
    eslESYS = 12    # generic system call failure
    eslECORRUPT = 13    # unexpected data corruption
    eslEINCONCEIVABLE = 14    # "can't happen" error
    eslESYNTAX = 15    # invalid user input syntax
    eslERANGE = 16    # value out of allowed range
    eslEDUP = 17    # saw a duplicate of something
    eslENOHALT = 18    # a failure to converge
    eslENORESULT = 19    # no result was obtained
    eslENODATA = 20    # no data provided, file empty
    eslETYPE = 21    # invalid type of argument
    eslEOVERWRITE = 22    # attempted to overwrite data
    eslENOSPACE = 23    # ran out of some resource
    eslEUNIMPLEMENTED = 24    # feature is unimplemented

cdef int SQFILE_UNKNOWN = 0
cdef int SQFILE_FASTA = 1
cdef int SQFILE_EMBL = 2
cdef int SQFILE_GENBANK = 3
cdef int SQFILE_NCBI = 6
# END DEFS

# BEGIN IMPLEMENTATION
FMT_FASTA = SQFILE_FASTA
FMT_GENBANK = SQFILE_GENBANK
FMT_UNKNOWN = SQFILE_UNKNOWN

class EaselError(ValueError):
    pass

class EaselMissingIndexError(IOError):
    pass

cdef class EaselSequence:
    """
    Wrapper for the Easel ESL_SQ object
    """
    cdef ESL_SQ *_sq

    def __init__(self):
        raise ValueError("This class cannot be instantiated from Python")

    def __dealloc__(self):
        if self._sq is not NULL:
            esl_sq_Destroy(self._sq)

    property name:
        def __get__(self):
            return self._sq.name
        def __set__(self, bytes name):
            esl_sq_SetName(self._sq, name)
    property accession:
        def __get__(self):
            return self._sq.acc
        def __set__(self, bytes acc):
            esl_sq_SetAccession(self._sq, acc)
    property description:
        def __get__(self):
            return self._sq.desc
        def __set__(self, bytes desc):
            esl_sq_SetDesc(self._sq, desc)
    property seq:
        def __get__(self):
            return self._sq.seq
    def __len__(self):
        return self._sq.n

    def write(self, fp):
        """
        Write the sequence to open file handle f, in FASTA format

        :param file fp: File-like object, open for writing.
        """
        fp.write('>' + self.name)
        if self.description:
            fp.write(' ' + self.description)
        fp.write('\n')
        fp.write(self.seq)
        fp.write('\n')

    def reverse_complement(self):
        """
        Reverse complements the sequence, in place
        """
        cdef int res = esl_sq_ReverseComplement(self._sq)

        if res != eslOK:
            raise EaselError("Error reverse complementing ({0})".format(res))

    def copy(self):
        """
        Make a copy of this sequence
        """
        cdef int res

        cdef ESL_SQ *s = esl_sq_Create()
        cdef EaselSequence sq
        try:
            res = esl_sq_Copy(self._sq, s)
            if res != eslOK:
                raise EaselError("Error Copying ({0})".format(res))
            sq = EaselSequence.__new__(EaselSequence)
            sq._sq = s
            return sq
        except:
            esl_sq_Destroy(s)
            raise

    def __getitem__(self, slice s):
        """
        Slice the sequence

        :param slice s: Slice to get, e.g. ``s[1:3]``
        :returns: :class:`EaselSequence` sliced to the specified residues.
        """
        cdef bytes seq

        seq = self._sq.seq
        seq = seq[s]
        return create_easel_sequence(
                esl_sq_CreateFrom(
                    self._sq.name, seq, self._sq.acc, self._sq.desc, NULL))

    def __repr__(self):
        return '<EaselSequence 0x%x [name="%s";description="%s";length=%d]>' \
                % (id(self), self.name, self.description, len(self))

    @classmethod
    def create(cls, bytes name, bytes seq, bytes acc, bytes desc):
        """
        Create a sequence

        :param str name: Sequence name
        :param str seq: Sequence residues
        :param str acc: Sequence accession number
        :param str desc: Sequence description
        :returns: A new :class:`EaselSequence`
        """
        return create_easel_sequence(
                esl_sq_CreateFrom(name, seq, acc, desc, NULL))

cdef create_easel_sequence(ESL_SQ *_sq):
    cdef EaselSequence s = EaselSequence.__new__(EaselSequence)
    s._sq = _sq
    return s

cdef ESL_SQFILE* open_sequence_file(bytes path,
        int sq_format=SQFILE_UNKNOWN) except NULL:
    cdef ESL_SQFILE *sq_fp = NULL
    cdef int status
    status = esl_sqfile_Open(path, 1, NULL, &sq_fp)
    if status == eslENOTFOUND:
        raise IOError("Not found: {0}".format(path))
    elif status != eslOK:
        raise IOError("Failed to create: {0}".format(status))
    return sq_fp

cdef int _open_ssi(ESL_SQFILE* sqfp, char* ssi_hint=NULL) except -1:
    cdef int status = esl_sqfile_OpenSSI(sqfp, ssi_hint)
    if status == eslENOTFOUND:
        raise IOError("SSI Index Not found.")
    if status == eslEFORMAT:
        raise IOError("Incorrect format!")
    if status == eslERANGE:
        raise IOError("Incorrect format (64-bit)!")
    elif status != eslOK:
        raise IOError("Failed to create: {0}".format(status))
    return 0

def read_seq_file(bytes path, int sq_format=SQFILE_UNKNOWN):
    """
    Read sequences from ``path``. This is a generator function.

    :param str path: Path to sequence file
    :returns: Generator of :class:`EaselSequence` objects.
    """
    cdef ESL_SQFILE *sq_fp = open_sequence_file(path, sq_format)
    cdef ESL_SQ *sq = esl_sq_Create()
    try:
        while esl_sqio_Read(sq_fp, sq) == eslOK:
            yield create_easel_sequence(sq)
            sq = esl_sq_Create()
    finally:
        esl_sq_Destroy(sq)
        esl_sqfile_Close(sq_fp)

def read_fasta(path):
    """
    Read sequences in FASTA format from a file.

    :param str path: Path to file containing sequences in FASTA format.
    :returns: A generator of :class:`EaselSequence` objects.
    """
    return read_seq_file(path, SQFILE_FASTA)

cdef class EaselSequenceIndex:
    """
    An open sequence index. Supports dict-like sequence lookups by name.
    """
    cdef ESL_SQFILE *_sq_fp
    cdef bytes file_path
    cdef int sq_format

    def __init__(self):
        raise ValueError("This class cannot be instantiated from Python")

    def __getitem__(self, bytes key):
        """
        Get a sequence from the indexed file

        :param slice key: Sequence name *or* accession
        :returns: :class:`EaselSequence` object.
        """
        cdef int status
        cdef ESL_SQ* sq = esl_sq_Create()

        try:
            status = esl_sqio_Fetch(self._sq_fp, key, sq)
            if status == eslENOTFOUND:
                raise KeyError(("Sequence {0} not found in index for "
                    "file {1}").format(key, self.file_path))
            elif status == eslEFORMAT:
                raise IOError(
                        "Failed to parse SSI index for {0}".format(self.file_path))
            elif status != eslOK:
                raise IOError(
                        "Failed to look up {0} in {1} [{2}]".format(
                            key, self.file_path, status))
            return create_easel_sequence(sq)
        except:
            esl_sq_Destroy(sq)
            raise

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __dealloc__(self):
        if self._sq_fp is not NULL:
            esl_sqfile_Close(self._sq_fp)

    def __repr__(self):
        return '<EaselSequenceIndex 0x%x [path="%s"]>' % (id(self), self.file_path)

def open_ssi(bytes file_path, bytes ssi_path=None, int sq_format=SQFILE_UNKNOWN):
    """
    Open a simple sequence index for a file.

    :param str file_path: Path to the sequence file
    :param str ssi_path: Path to the sequence SSI file. If not given, ``.ssi`` is
                         appended to ``file_path``.
    :param sq_format: File format.
    """
    cdef EaselSequenceIndex obj = EaselSequenceIndex.__new__(EaselSequenceIndex)
    obj.file_path = file_path
    obj.sq_format = sq_format

    obj._sq_fp = open_sequence_file(file_path, sq_format)

    # Set SSI path
    cdef char* cssi_path = NULL
    if ssi_path is not None:
        cssi_path = ssi_path

    _open_ssi(obj._sq_fp, cssi_path)

    if obj._sq_fp.data.ascii.ssi is NULL:
        raise EaselMissingIndexError(
                "no index exists for {0}".format(file_path))

    return obj


def create_ssi(bytes file_path, bytes ssi_name=None,
               int sq_format=SQFILE_UNKNOWN):
    """
    Create a Simple Sequence Index for a file.

    :param file_path: Path to the sequence file
    :param ssi_path: Path to the sequence SSI file. If not given, ``.ssi`` is
                     appended to ``file_path``.
    :param sq_format: File format.
    """
    cdef ESL_NEWSSI *ssi
    cdef ESL_SQFILE *sq_fp = NULL
    cdef ESL_SQ *sq = esl_sq_Create()
    cdef int status, count = 0
    cdef uint16_t fh

    if ssi_name is None:
        ssi_name = file_path + b'.ssi'

    status = esl_newssi_Open(ssi_name, 0, &ssi);

    if status == eslENOTFOUND:
        raise IOError("Not found: {0}".format(ssi_name))
    elif status == eslEOVERWRITE:
        raise IOError("Exists: {0}".format(ssi_name))
    elif status != eslOK:
        raise IOError("Failed to create: {0}".format(status))

    status = esl_sqfile_Open(file_path, 1, NULL, &sq_fp)
    if status != eslOK:
        raise IOError("Error opening {0}: {1}".format(file_path, status))

    if esl_newssi_AddFile(ssi, sq_fp.filename, sq_fp.format, &fh) != eslOK:
        raise IOError("Failed to add sequence file {0}".format(file_path))

    try:
        status = esl_sqio_ReadInfo(sq_fp, sq)
        while status == eslOK:
            count += 1
            if esl_newssi_AddKey(
                    ssi, sq.name, fh, sq.roff, sq.doff, sq.L) != eslOK:
                raise EaselError("unable to add {0} to index".format(sq.name))
            esl_sq_Reuse(sq)
            status = esl_sqio_ReadInfo(sq_fp, sq)
        if status == eslEFORMAT:
            raise IOError("Failed parsing.")
        elif status != eslEOF:
            raise IOError(("Unexpected error {0} reading sequence "
                "file").format(status))

        esl_newssi_Write(ssi)
    finally:
        esl_sq_Destroy(sq)
        esl_sqfile_Close(sq_fp)
        esl_newssi_Close(ssi)

    return count

def write_fasta(sequences not None, fp not None):
    """
    Writes `sequences` to the open file handle fp

    :param sequences: Iterable of :class:`EaselSequence` objects
    :param fp: Open file-like object
    """
    cdef int count = 0
    for sequence in sequences:
        count += 1
        sequence.write(fp)
    return count
