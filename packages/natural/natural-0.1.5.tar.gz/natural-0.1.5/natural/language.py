# -*- coding: utf-8 -*-
import gettext
import locale
import os


'''
.. py:attribute:: LOCALE_PATH

   Path on the file system to the locale/ directory, used to find translations
   for the current locale.


.. py:attribute:: CONVENTION

   Container for all the locale conventions, see
   http://docs.python.org/library/locale.html#locale.localeconv
'''


locale.setlocale(locale.LC_ALL, '')

LOCALE_PATH = os.path.join(os.path.dirname(__file__), 'locale')
gettext.bindtextdomain('natural', LOCALE_PATH)
gettext.textdomain('natural')
try:
    TRANSLATION = gettext.translation('natural', LOCALE_PATH)
    _ = TRANSLATION.ugettext
except IOError:
    _ = gettext.NullTranslations().ugettext

# generic
CONVENTION = locale.localeconv()


def _multi(singular, plural, count):
    '''
    Provides translations for plural and singular forms of a term.
    '''
    if count == 1:
        return singular
    else:
        return plural
