import nose.tools
from nose import SkipTest

import pywps
from lxml import etree
from StringIO import StringIO

execute_request = "service=wps&request=execute&version=1.0.0&identifier=org.malleefowl.test.whoareyou&datainputs=[notes=Test;username=jule;password=test]"
wpsns = "http://www.opengis.net/wps/1.0.0"
ns = {'wps': wpsns}

def test_whoareyou():
    mypywps = pywps.Pywps(pywps.METHOD_GET)
    inputs = mypywps.parseRequest(execute_request)
    mypywps.performRequest(inputs)
    doc = etree.parse(StringIO(mypywps.response))
    r = doc.xpath("//*/wps:Output/wps:Data/wps:LiteralData", namespaces=ns)
    nose.tools.ok_(len(r) == 1, mypywps.response)
    nose.tools.ok_(r[0].text == 'Hello jule', r[0].text)

