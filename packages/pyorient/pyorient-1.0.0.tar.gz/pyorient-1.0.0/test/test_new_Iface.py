__author__ = 'Ostico <ostico@gmail.com>'
import unittest
import os
import sys

os.environ['DEBUG'] = "1"
os.environ['DEBUG_VERBOSE'] = "0"
# if os.path.realpath('../') not in sys.path:
#     sys.path.insert(0, os.path.realpath('../'))
#
# if os.path.realpath('.') not in sys.path:
#     sys.path.insert(0, os.path.realpath('.'))

import pyorient

class CommandTestCase(unittest.TestCase):
    """ Command Test Case """

    def test_new_client_interface(self):

            client = pyorient.OrientDB("localhost", 2424)
            session_id = client.connect( "admin", "admin" )

            db_name = "GratefulDeadConcerts"

            cluster_info = client.db_open( db_name, "admin", "admin" )
            assert cluster_info != []

            result = client.query("select from followed_by", 10, '*:0')
            assert True
            assert result != []
            from pyorient.Commons.OrientTypes import OrientRecord
            assert isinstance( result[0], OrientRecord )
            assert len(result) == 10
            assert result[0].__getattribute__('in') != 0
            assert result[0].out != 0

            def _callback(item):
                assert True
                assert item != []
                from pyorient.Commons.OrientTypes import OrientRecord
                assert isinstance( item, OrientRecord )

            result = client.query_async("select from followed_by",
                                        10, '*:0', _callback )
            assert True
            assert result is None

            res = client.record_load( "#11:0", "*:-1", _callback )
            assert res.rid == "#11:0"
            assert res.o_class == 'followed_by'
            assert res.__getattribute__('in') != 0
            assert res.out != 0

            # TEST COMMANDS
            db_name = 'test_commands'

            exists = client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY )

            print "Before %r" % exists
            try:
                client.db_drop(db_name)
                assert True
            except pyorient.PyOrientCommandException, e:
                print e.message
            finally:
                client.db_create( db_name, pyorient.DB_TYPE_GRAPH,
                                  pyorient.STORAGE_TYPE_MEMORY )

            cluster_info = client.db_open(
                db_name, "admin", "admin", pyorient.DB_TYPE_GRAPH, ""
            )

            cluster_id = client.command( "create class my_class extends V" )[0]
            assert cluster_id != 0

            rec = { '@my_class': { 'alloggio': 'casa', 'lavoro': 'ufficio', 'vacanza': 'mare' } }
            rec_position = client.record_create( cluster_id, rec )

            print "New Rec Position: %s" % rec_position.rid
            assert rec_position.rid is not None
            assert rec_position.rid != 0
            assert rec_position.rid != -1

            res = client.record_load( rec_position.rid, "*:0" )
            assert res.rid == rec_position.rid
            assert res.o_class == 'my_class'
            assert res.alloggio == 'casa'
            assert res.lavoro == 'ufficio'
            assert res.vacanza == 'mare'

            deletion = client.record_delete( cluster_id, rec_position.rid )
            assert deletion is True

            result = client.query("select from my_class", 10, '*:0')
            assert True
            assert result == []

            # CLUSTERS
            new_cluster_id = client.data_cluster_add(
                'my_cluster_1234567', pyorient.CLUSTER_TYPE_PHYSICAL
            )
            assert new_cluster_id > 0

            new_cluster_list = client.db_reload()
            new_cluster_list.sort(key=lambda cluster: cluster['id'])

            _list = []
            for cluster in new_cluster_list:
                print "Cluster Name: %s, ID: %u " \
                      % ( cluster['name'], cluster['id'] )
                value = client.data_cluster_data_range(cluster['id'])
                print "Value: %s " % value
                _list.append( cluster['id'] )
                assert value is not []
                assert value is not None

            # check for new cluster in database
            try:
                _list.index( new_cluster_id )
                print "New cluster %r found in reload." % new_cluster_id
                assert True
            except ValueError:
                assert False

            # delete the new cluster
            print "Drop Cluster ID: %r" % new_cluster_id
            drop_cluster = client.data_cluster_drop( new_cluster_id )
            assert drop_cluster is True

            result = client.query("select from my_class", 10, '*:0')
            assert True
            assert result == []

    def test_transaction_new_iface(self):

        client = pyorient.OrientDB('localhost', 2424)

        client.connect( "admin", "admin" )

        db_name = 'test_transactions'

        exists = client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY )

        print "Before %r" % exists
        try:
            client.db_drop(db_name)
            assert True
        except pyorient.PyOrientCommandException, e:
            print e.message
        finally:
            client.db_create( db_name, pyorient.DB_TYPE_GRAPH,
                              pyorient.STORAGE_TYPE_MEMORY )

        cluster_info = client.db_open(
            db_name, "admin", "admin", pyorient.DB_TYPE_GRAPH, ""
        )

            #######################################

        # execute real create
        rec = { 'alloggio': 'baita', 'lavoro': 'no', 'vacanza': 'lago' }
        rec_position = client.record_create( 3, rec )

        #  START TRANSACTION
        print "debug breakpoint line"
        tx = client.tx_commit()
        tx.begin()

        # prepare for an update
        rec3 = { 'alloggio': 'albergo', 'lavoro': 'ufficio', 'vacanza': 'montagna' }
        update_success = client.record_update( 3, rec_position.rid, rec3,
                                  rec_position.version )

        # prepare transaction
        rec1 = { 'alloggio': 'casa', 'lavoro': 'ufficio', 'vacanza': 'mare' }
        rec_position1 = client.record_create( -1, rec1 )

        rec2 = { 'alloggio': 'baita', 'lavoro': 'no', 'vacanza': 'lago' }
        rec_position2 = client.record_create( -1, rec2 )

        delete_msg = client.record_delete( 3, rec_position.rid )


        tx.attach( rec_position1 )
        tx.attach( rec_position1 )
        tx.attach( rec_position2 )
        tx.attach( update_success )
        tx.attach( delete_msg )
        res = tx.commit()

        for k, v in res.iteritems():
            print k + " -> " + v.vacanza

        assert len(res) == 3
        assert res["#3:1"].vacanza == 'mare'
        assert res["#3:2"].vacanza == 'mare'
        assert res["#3:3"].vacanza == 'lago'

        client.db_drop( db_name, pyorient.STORAGE_TYPE_MEMORY )

# x = CommandTestCase('test_command').run()

# x = CommandTestCase('test_new_client_interface').run()