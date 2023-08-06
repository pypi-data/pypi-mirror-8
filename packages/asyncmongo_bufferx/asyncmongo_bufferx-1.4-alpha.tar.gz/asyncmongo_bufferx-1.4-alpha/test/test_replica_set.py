import tornado.ioloop
import time
import logging
import subprocess
import socket

import test_shunt
import asyncmongo
import asyncmongo.connection
import asyncmongo.errors

TEST_TIMESTAMP = int(time.time())

class ReplicaSetTest(test_shunt.MongoTest):
    mongod_options = [
        ('--port', '27018', '--replSet', 'rs0'),
        ('--port', '27019', '--replSet', 'rs0'),
        ('--port', '27020', '--replSet', 'rs0'),
    ]

    def mongo_cmd(self, cmd, port=27018, res='"ok" : 1'):
        pipe = subprocess.Popen("mongo --port %d" % port, shell=True,
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        reply = pipe.communicate(cmd)[0]
        assert reply.find(res) > 0
        return reply

    def wait_master(self, port):
        while True:
            if self.mongo_cmd("db.isMaster();", port).find('"ismaster" : true') > 0:
                logging.info("%d is a master", port)
                break
            else:
                logging.info("Waiting for %d to become master", port)
                time.sleep(5)

    def setUp(self):
        super(ReplicaSetTest, self).setUp()
        hostname = socket.gethostname()
        logging.info("configuring a replica set at %s" % hostname)
        cfg = """
        {
            "_id" : "rs0",
            "members" : [
                {
                    "_id" : 0,
                    "host" : "%(hostname)s:27018"
                },
                {
                    "_id" : 1,
                    "host" : "%(hostname)s:27019",
                    "priority" : 2
                },
                {
                    "_id" : 2,
                    "host" : "%(hostname)s:27020",
                    "priority" : 0
                }
            ]
        }
        """ % dict(hostname=hostname)
        self.mongo_cmd("rs.initiate(%s);" % cfg)
        logging.info("waiting for replica set to finish configuring")
        self.wait_master(27019)

    def test_connection(self):
        class Pool(object):
            def __init__(self):
                super(Pool, self).__init__()
                self._cache = []

            def cache(self, c):
                self._cache.append(c)

        class AsyncClose(object):
            def process(self, *args, **kwargs):
                tornado.ioloop.IOLoop.instance().stop()

        hostname = socket.gethostname()
        try:
            conn = asyncmongo.connection.Connection(pool=Pool(),
                                                    seed=[(hostname, 27018), (hostname, 27020)],
                                                    rs="rs0")

            conn._put_job(AsyncClose(), 0)
            conn._next_job()
            tornado.ioloop.IOLoop.instance().start()

            assert conn._host == hostname
            assert conn._port == 27019

        except:
            tornado.ioloop.IOLoop.instance().stop()
            raise

    def test_update(self):
        try:
            test_shunt.setup()
            db = asyncmongo.Client(pool_id='testrs', rs="rs0", seed=[("127.0.0.1", 27020)], dbname='test', maxconnections=2)

            # Update
            def update_callback(response, error):
                logging.info("UPDATE:")
                tornado.ioloop.IOLoop.instance().stop()
                logging.info(response)
                assert len(response) == 1
                test_shunt.register_called('update')

            db.test_stats.update({"_id" : TEST_TIMESTAMP}, {'$inc' : {'test_count' : 1}}, upsert=True, callback=update_callback)

            tornado.ioloop.IOLoop.instance().start()
            test_shunt.assert_called('update')

            # Retrieve the updated value
            def query_callback(response, error):
                tornado.ioloop.IOLoop.instance().stop()
                logging.info(response)
                logging.info(error)
                assert error is None
                assert isinstance(response, dict)
                assert response['_id'] == TEST_TIMESTAMP
                assert response['test_count'] == 1
                test_shunt.register_called('retrieved')

            db.test_stats.find_one({"_id" : TEST_TIMESTAMP}, callback=query_callback)
            tornado.ioloop.IOLoop.instance().start()
            test_shunt.assert_called('retrieved')

            # Switch the master
            self.mongo_cmd(
                "cfg = rs.conf(); cfg.members[1].priority = 1; cfg.members[0].priority = 2; rs.reconfig(cfg);",
                27019, "reconnected to server")
            self.wait_master(27018)

            # Expect the connection to be closed
            def query_err_callback(response, error):
                tornado.ioloop.IOLoop.instance().stop()
                logging.info(response)
                logging.info(error)
                assert isinstance(error, Exception)

            db.test_stats.find_one({"_id" : TEST_TIMESTAMP}, callback=query_err_callback)
            tornado.ioloop.IOLoop.instance().start()

            # Retrieve the updated value again, from the new master
            def query_again_callback(response, error):
                tornado.ioloop.IOLoop.instance().stop()
                logging.info(response)
                logging.info(error)
                assert error is None
                assert isinstance(response, dict)
                assert response['_id'] == TEST_TIMESTAMP
                assert response['test_count'] == 1
                test_shunt.register_called('retrieved_again')

            db.test_stats.find_one({"_id" : TEST_TIMESTAMP}, callback=query_again_callback)
            tornado.ioloop.IOLoop.instance().start()
            test_shunt.assert_called('retrieved_again')
        except:
            tornado.ioloop.IOLoop.instance().stop()
            raise
