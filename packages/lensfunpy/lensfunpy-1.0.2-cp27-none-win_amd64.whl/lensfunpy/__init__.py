from __future__ import absolute_import

import os

import lensfunpy._lensfun
globals().update(lensfunpy._lensfun.__dict__)

# for Windows we wrap the Database constructor to load the bundled database files
# as lensfun wouldn't find any in the standard search locations like on Linux
if os.name == 'nt':
    _Database = Database
    del Database
    
    from functools import wraps
    import glob
    
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    _xml_glob = os.path.join(_ROOT, 'db_files', '*.xml')
    
    @wraps(_Database)
    def Database(filenames=None, xml=None, loadAll=True):
        if loadAll:
            if not filenames:
                filenames = []
            filenames.extend(glob.glob(_xml_glob))
        return _Database(filenames, xml, loadAll)
    