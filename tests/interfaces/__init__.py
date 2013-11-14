
import sip
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)

import sys

if sys.version_info[1] >= 3:
    from unittest.mock import patch, MagicMock
else:
    from mock import patch, MagicMock
