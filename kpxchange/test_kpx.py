
#Use green command to run a nicer test output from test directory
#from PIL import Image
import unittest
import run
import os
from tempfile import NamedTemporaryFile

class ServerTests(unittest.TestCase):

    def setUp(self):
        self.app = run.app.test_client()
        app_path = run.app.root_path
        print (app_path)

        if not os.path.exists(os.path.join(app_path,('vault/test'))): os.makedirs(os.path.join(app_path,('vault/test')))

    def tearDown(self):
        pass

    def testIsUp(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def testIsaFile(self):
        rv = self.app.post('/upload/test',data=dict(file=NamedTemporaryFile()))
        assert rv.status_code == 200

    def testUploadAllowedSize(self):
        zerobuff = b"0"*1024
        allowed_file = NamedTemporaryFile()
        allowed_file.write(zerobuff)
        allowed_file.seek(0)
        rv = self.app.post('/upload/test',data=dict(file=allowed_file))
        assert rv.status_code == 200

    def testUploadOversized(self):
        zerobuff = b"0"*1024*1500
        disallowed_file = NamedTemporaryFile()
        disallowed_file.write(zerobuff)
        disallowed_file.seek(0)
        rv = self.app.post('/upload/test', data=dict(file=disallowed_file))
        assert rv.status_code == 413

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ServerTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
