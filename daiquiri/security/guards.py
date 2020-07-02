# =============================================================================
# IMPORTS
# =============================================================================
import abc
import os
import daiquiri as dq

# =============================================================================
# CONSTANTS
# =============================================================================
PROHIBITED_KEYWORDS_PATH = os.path.dirname(
    dq.__file__) + '/security/prohibited_keywords.txt'
PROHIBITED_IMPORTS_PATH = os.path.dirname(
    dq.__file__) + '/security/prohibited_imports.txt'

# =============================================================================
# BASE CLASSES
# =============================================================================
class BaseGuard(abc.ABC):
    """ Base class for `Guard` objects that scan input files for job
    description.

    Methods
    -------
    scan : Scans the input file and returns a `boolean` variable
        indicating whether the submitted job is suitable for running.

    """
    def __init__(self):
        super(BaseGuard, self).__init__()

    @abc.abstractmethod
    def scan(self, *args, **kwargs):
        raise NotImplementedError


# =============================================================================
# MODULE CLASSES
# =============================================================================
class KeywordsGuard(BaseGuard):
    """ Search for prohibited keywords in job description file.

    Parameters
    ----------
    keywords : `List` of `str` or `None`
        List of keywords to be excludeded in the submitted job.
        If not specified, use the default list of prohibited keywords from
        `prohibited_keywords.txt`.




    """
    def __init__(self, keywords=None):
        super(KeywordsGuard, self).__init__()

        # if no keywords are specified, use the default keywords
        # from `keywords.txt`
        if keywords is None:
            with open(PROHIBITED_KEYWORDS_PATH, 'r') as f_handle: # file handle
                keywords = f_handle.readlines()

                # just in case
                keywords = [keyword.lower().strip() for keyword in keywords]

        self.keywords = keywords

    def scan(self, input):
        """ Scans the input file for keywords and returns a `boolean` variable
        indicating whether the submitted job is suitable for running.

        Parameters
        ----------
        input : `str`
            Job submission file as string.

        Returns
        -------
        ok : `bool`
            Whether a job description is approved to be submitted.

        """

        return all(
            keyword not in input for keyword in self.keywords
        )

class ImportGuard(BaseGuard):
    """ Search for imports in job submission file.

    Parameters
    ----------
    keywords : `List` of `str` or `None`
        List of keywords to be excludeded in the submitted job.
        If not specified, use the default list of prohibited keywords from
        `prohibited_imports.txt`.



    """
    def __init__(self, keywords=None):
        super(ImportGuard, self).__init__()

        # if no keywords are specified, use the default keywords
        # from `keywords.txt`
        if keywords is None:
            with open(PROHIBITED_IMPORTS_PATH, 'r') as f_handle: # file handle
                keywords = f_handle.readlines()

                # just in case
                keywords = [keyword.lower().strip() for keyword in keywords]

        self.keywords = keywords

    def scan(self, input):
        """ Scans the input file for imports and returns a `boolean` variable
        indicating whether the submitted job is suitable for running.

        Parameters
        ----------
        input : `str`
            Job submission file as string.

        Returns
        -------
        ok : `bool`
            Whether a job description is approved to be submitted.

        """
        # get all lines
        lines = input.split('\n')

        # strip
        lines = [line.strip() for line in lines]

        # get all import lines
        # NOTE:
        # I think `import` has to be at the beginning?
        import_lines = [line for line in lines if line.startswith('import')]

        # get all imported stuff
        imports = ' '.join(import_lines).split(' ')

        # scan
        return all(
            keyword not in imports for keyword in self.keywords
        )
