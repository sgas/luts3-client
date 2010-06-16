"""
Usage record related stuff.
"""

import urlparse

try:
    from xml.etree import cElementTree as ET
except ImportError:
    # Python 2.4 compatability
    from elementtree import ElementTree as ET

# ur namespaces and tag names, only needed ones
OGF_UR_NAMESPACE  = "http://schema.ogf.org/urf/2003/09/urf"
USAGE_RECORDS    = ET.QName("{%s}UsageRecords"   % OGF_UR_NAMESPACE)



def joinUsageRecordFiles(filenames):

    urs = ET.Element(USAGE_RECORDS)

    for fn in filenames:
        ur = ET.parse(fn)
        urs.append(ur.getroot())

    return ET.tostring(urs)

