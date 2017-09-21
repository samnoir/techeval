import unittest
import flask_testing
from flask import Flask
import urllib
import json
import time


class MyTest(flask_testing.LiveServerTestCase):
    """
    Test cases for the evaluation of the simple financial transaction system
    """
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def get_history_url(self):
        return self.get_server_url() + '/history'
    
    def test_server_is_up(self):
        """
        Trivial case to check whether the server is up and running
        """
        resp = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(resp.code, 200)
        resp.close()
        
    def test_post_history(self):
        """
        Post one transaction into the database
        """
        txn = """
        {
            "sym":"USD",
            "action":"card_auth",
            "amt":49.21,
            "cuid0":"dWFH5qXl8vNw3vtt",
            "actor":"dWFH5qXl8vNw3vtt",
            "source":"dWFH5qXl8vNw3vtt",
            "note":"PARTY CITYe PlacOHUS",
            "tuid":"8BLZ-XY3E",
            "external_id":"V.27",
            "timestamp":1498867359524
        }
        """
        jdata = json.loads(txn)
        data = json.dumps(jdata).encode('utf8')
        print(data)
        print(self.get_history_url())
        req = urllib.request.Request(self.get_history_url(), data)
        req.add_header('Content-Type', 'application/json')
        t = time.time()
        f = urllib.request.urlopen(req)
        t = time.time() - t
        print("ELAPSED =", t)
        self.assertEqual(f.code, 200)
        print(f.read().decode('utf-8'))
        f.close()
        #self.fail('Not implemented')
    
    #def test_get_history_tuid(self):
        #"""
        #Get the transactions based on the tuid
        #"""
        #self.fail('Not implemented')
    
    #def test_get_history_wuid(self):
        #"""
        #Get the transactions based on the wuid
        #"""        
        #self.fail('Not implemented')
    
    #def test_err_get_history_tuid(self):
        #"""
        #ERROR: Test that the server returns error when given a wrong tuid
        #"""
        #self.fail('Not implemented')
    
    #def test_err_get_history_wuid(self):
        #"""
        #ERROR: Test that the server returns error when given a wrong wuid
        #"""
        #self.fail('Not implemented')
    
    #def test_err_get_history_tuid_wuid(self):
        #"""
        #ERROR: Test that the server returns error when given both wuid and tuid
        #"""
        #self.fail('Not implemented')
    
    #def test_error_post_history_with_duplicate_tuid(self):
        #"""
        #ERROR: Test that posting with a duplicate tuid returns error
        #"""
        #self.fail('Not implemented')
    
        
        
if __name__=='__main__':
    unittest.main()