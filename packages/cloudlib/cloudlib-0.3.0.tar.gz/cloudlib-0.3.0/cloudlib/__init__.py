# =============================================================================
# Copyright [2014] [Kevin Carter]
# License Information :
# This software has no warranty, it is provided 'as is'. It is your
# responsibility to validate the behavior of the routines and its accuracy
# using the code provided. Consult the GNU General Public license for further
# details (see GNU General Public License).
# http://www.gnu.org/licenses/gpl.html
# =============================================================================
__author__ = 'Kevin Carter'
__contact__ = 'Kevin Carter'
__email__ = 'kevin@cloudnull.com'
__copyright__ = '2014 All Rights Reserved'
__license__ = 'GPLv3+'
__date__ = '2014-04-20'
__version__ = '0.3.0'
__status__ = 'Production'
__appname__ = 'cloudlib'
__description__ = 'general purpose library for in application use'
__url__ = 'https://github.com/cloudnull/cloudlib'


class MissingConfig(Exception):
    """Raise this exception when the config variable is required."""
    pass


class MissingConfigValue(Exception):
    """Raise this exception when the config a value is required."""
    pass


class MessageFailure(Exception):
    """Raise this exception when an application fails processing a message."""
    pass


class MD5CheckMismatch(Exception):
    """Exception class when the md5 sum of a file is not what is expected."""
    pass
