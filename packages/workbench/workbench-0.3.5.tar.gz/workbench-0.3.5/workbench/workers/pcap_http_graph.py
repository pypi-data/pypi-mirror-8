''' pcap_http_graph worker '''
import os
import zerorpc
import pprint
import gevent

def gsleep():
    ''' Convenience method for gevent.sleep '''
    print '*** Gevent Sleep ***'
    gevent.sleep(0)

class PcapHTTPGraph(object):
    ''' This worker generates a graph from a PCAP (depends on Bro) '''
    dependencies = ['pcap_bro']

    def __init__(self):
        ''' Initialization '''
        self.workbench = zerorpc.Client(timeout=300, heartbeat=60)
        self.workbench.connect('tcp://127.0.0.1:4242')
        self.mime_types = ['application/x-dosexec', 'application/pdf', 'application/zip',
                           'application/jar', 'application/vnd.ms-cab-compressed',
                           'application/x-shockwave-flash']
        self.exclude_mime_types = ['text/plain','text/html','image/jpeg','image/png']

        # Caches for nodes and relationships to avoid adding things over and over
        self.node_cache = set()
        self.rel_cache = set()

        # In general this is heavy handed but seems better to do than not do
        self.workbench.clear_graph_db()

    # Graph methods
    def add_node(self, node_id, name, labels):
        ''' Cache aware add_node '''
        if node_id not in self.node_cache:
            self.workbench.add_node(node_id, name, labels)
            self.node_cache.add(node_id)

    def add_rel(self, source_id, target_id, rel):
        ''' Cache aware add_rel '''
        if (source_id, target_id) not in self.rel_cache:
            self.workbench.add_rel(source_id, target_id, rel)
            self.rel_cache.add((source_id, target_id))

    def execute(self, input_data):
        ''' Okay this worker is going build graphs from PCAP Bro output logs '''

        # Grab the Bro log handles from the input
        bro_logs = input_data['pcap_bro']

        # Weird log
        if 'weird_log' in bro_logs:
            stream = self.workbench.stream_sample(bro_logs['weird_log'])
            self.weird_log_graph(stream)

        # HTTP log
        gsleep()
        stream = self.workbench.stream_sample(bro_logs['http_log'])
        self.http_log_graph(stream)

        # Files log
        gsleep()
        stream = self.workbench.stream_sample(bro_logs['files_log'])
        self.files_log_graph(stream)

        return {'output':'go to http://localhost:7474/browser and execute this query "match (s:origin), (t:file), p=allShortestPaths((s)--(t)) return p"'}

    def http_log_graph(self, stream):
        ''' Build up a graph (nodes and edges from a Bro http.log) '''
        print 'Entering http_log_graph...'
        for row in list(stream):

            # Skip '-' hosts
            if (row['id.orig_h'] == '-'):
                continue

            # Add the originating host
            self.add_node(row['id.orig_h'], row['id.orig_h'], ['host', 'origin'])

            # Add the response host and reponse ip
            self.add_node(row['host'], row['host'], ['host'])
            self.add_node(row['id.resp_h'], row['id.resp_h'], ['host'])

            # Add the http request relationships
            self.add_rel(row['id.orig_h'], row['host'], 'http_request')
            self.add_rel(row['host'], row['id.resp_h'], 'A')

    def weird_log_graph(self, stream):
        ''' Build up a graph (nodes and edges from a Bro weird.log) '''

        # Here we're just going to capture that something weird
        # happened between two hosts
        weird_pairs = set()
        for row in list(stream):
            weird_pairs.add((row['id.orig_h'], row['id.resp_h']))

        # Okay now make the weird node for each pair
        for pair in weird_pairs:

            # Skip '-' hosts
            if (pair[0] == '-'):
                continue

            # Add the originating host
            self.add_node(pair[0], pair[0], ['host', 'origin'])

            # Add the response host
            self.add_node(pair[1], pair[1], ['host'])

            # Add a weird node
            weird_name = 'weird'+pair[0]+'_'+pair[1]
            self.add_node(weird_name, 'weird', ['weird'])

            # The relationships between the nodes
            self.add_rel(pair[0], weird_name, 'weird')
            self.add_rel(weird_name, pair[1], 'weird')

    def files_log_graph(self, stream):
        ''' Build up a graph (nodes and edges from a Bro dns.log) '''
        for row in list(stream):

            # dataframes['files_log'][['md5','mime_type','missing_bytes','rx_hosts','source','tx_hosts']]
            
            # If the mime-type is interesting add the uri and the host->uri->host relationships
            if row['mime_type'] not in self.exclude_mime_types:

                # Check for weird conditions
                if (row['total_bytes'] == '-'):
                    continue
                if ('-' in row['md5']):
                    continue

                # Check for missing bytes and small file
                if row['missing_bytes']:
                    labels = ['missing', 'file']
                elif row['total_bytes'] < 50*1024:
                    labels = ['small','file']
                else:
                    labels = ['file']

                # Make the file node name kewl
                name = '%6s  %s  %.0f-KB' % (row['md5'][:6], row['mime_type'], row['total_bytes']/1024.0)
                if row['missing_bytes']:
                    name += '*'
                name = name.replace('application/','')
                
                # Add the file node
                self.add_node(row['md5'], name, labels)

                # Add the tx_host
                self.add_node(row['tx_hosts'], row['tx_hosts'], ['host'])

                # Add the file->tx_host relationship
                self.add_rel(row['tx_hosts'], row['md5'], 'file')

    def __del__(self):
        ''' Class Cleanup '''
        # Close zeroRPC client
        self.workbench.close()

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' pcap_http_graph.py: Unit test '''
    # This worker test requires a local server as it relies on the recursive dependencies
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect("tcp://127.0.0.1:4242")

    # Generate the input data for this worker
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../data/pcap/kitchen_boss.pcap')
    md5 = workbench.store_sample(open(data_path, 'rb').read(), 'kitchen_boss.pcap', 'pcap')
    input_data = workbench.work_request('pcap_bro', md5)

    # Execute the worker (unit test)
    worker = PcapHTTPGraph()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    pprint.pprint(output)

    # Execute the worker (server test)
    output = workbench.work_request('pcap_http_graph', md5)
    print '\n<<< Server Test >>>'
    pprint.pprint(output)

if __name__ == "__main__":
    test()
