import unittest
from clickatell import Transport
from clickatell.exception import ClickatellError
import json

class TransportTest(unittest.TestCase):

    def test_parseLegacyFailure(self):
        response = {'body': 'ERR: Some exception'}
        transport = Transport()
        self.assertRaises(ClickatellError, lambda: transport.parseLegacy(response))

    def test_parseLegacyMultiFailure(self):
        response = {'body': 'ERR: 301, Some Failure\nOK:12345'}
        transport = Transport()
        result = transport.parseLegacy(response)
        self.assertTrue(len(result) == 2)
        self.assertTrue(result[0]['code'] == '301')
        self.assertTrue(result[1]['OK'] == '12345')

    def test_parseLegacy(self):
        response = {'body': 'OK: 1234 Test: 12345'}
        transport = Transport()
        result = transport.parseLegacy(response)
        self.assertTrue(result['OK'] == '1234')
        self.assertTrue(result['Test'] == '12345')

    def test_parseRestFailure(self):
        response = {'body': json.dumps({'error':{'description':'Error','code':'301'}})}
        transport = Transport()
        self.assertRaises(ClickatellError, lambda: transport.parseRest(response))

    def test_parseRest(self):
        response = {'body': json.dumps({'data':True})}
        transport = Transport()
        self.assertTrue(transport.parseRest(response))

    def test_merge(self):
        transport = Transport()
        dict1 = {'test': 1}
        dict2 = {'test': 2, 'test2': 3}
        dict3 = {'test1': 1, 'test2': 2}
        merge = transport.merge(dict1, dict2, dict3)
        self.assertTrue(merge['test'] == 2)
        self.assertTrue(merge['test2'] == 2)
        self.assertTrue(merge['test1'] == 1)