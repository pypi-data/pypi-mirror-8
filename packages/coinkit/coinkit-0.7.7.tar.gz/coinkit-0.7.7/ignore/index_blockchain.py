import traceback, json
from coinkit import *
from collections import defaultdict
from pprint import pprint
from decimal import *

class ExtendedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(ExtendedJSONEncoder, self).default(o)

class Blockchain(object):
    def __init__(self, bitcoind_client):
        self.txs = {}
        self.address_txs = defaultdict(dict)
        self.bitcoind = bitcoind_client.bitcoind
        self.block_count = self.bitcoind.getblockcount()
        self.nulldata_txs = defaultdict(list)

    def spend_input(self, tx_hash, input):
        if 'txid' in input and 'vout' in input and 'scriptSig' in input:
            input_tx_hash = str(input['txid'])
            input_index = str(input['vout'])
            
            script_sig_asm = str(input['scriptSig'].get('asm'))
            script_sig_hex = str(input['scriptSig'].get('hex'))
            script_sig_parts = script_sig_asm.split(' ')
            if len(script_sig_parts) > 1 and (len(script_sig_parts[-1]) == 130 
                or len(script_sig_parts[-1]) == 66):
                public_key_string = script_sig_parts[-1]
                try:
                    recipient_address = BitcoinPublicKey(public_key_string, verify=False).address()
                except:
                    print "Error with transaction..."
                    print "Input tx hash: %s" % input_tx_hash
                    print "Current tx hash: %s" % tx_hash
                    print input['scriptSig']
                    traceback.print_exc()
                    return
            elif len(script_sig_parts) == 1:
                print "coinbase transaction input"
                return
            else:
                print "input with unknown transaction type"
                print "Input tx hash: %s" % input_tx_hash
                print "Current tx hash: %s" % tx_hash
                print input['scriptSig']
                return

            #print recipient_address
            input_id = '%s-%s' % (input_tx_hash, input_index)

            if input_id in self.address_txs[recipient_address]:
                self.address_txs[recipient_address][input_id] = False

    def log_output(self, tx_hash, output):
        if 'scriptPubKey' in output and 'n' in output:
            output_index = output['n']
            output_script = output['scriptPubKey']
            if 'addresses' in output_script:
                output_addresses = output_script['addresses']
                for address in output_addresses:
                    self.address_txs[address]['%s-%s' % (tx_hash, output_index)] = True

    def check_for_nulldata(self, tx, block_number):
        if 'vin' in tx and 'vout' in tx:
            inputs = tx['vin']
            outputs = tx['vout']
            for output in outputs:
                if 'scriptPubKey' in output:
                    script_asm = str(output['scriptPubKey'].get('asm'))
                    script_parts = script_asm.split(' ')
                    script_type = str(output['scriptPubKey'].get('type'))
                    if script_type == 'nulldata' and len(script_parts) == 2:
                        script_data = script_parts[1]
                        nulldata_tx = {'data': script_data, 'outputs': outputs }
                        self.nulldata_txs[block_number].append(nulldata_tx)
                        print "nulldata tx"

    def process_tx(self, tx_hash, block_number):
        print tx_hash
        # lookup the raw tx using the tx hash
        try:
            raw_tx = self.bitcoind.getrawtransaction(tx_hash)
        except:
            traceback.print_exc()
            return
        
        # extract the tx data from the raw tx
        tx = self.bitcoind.decoderawtransaction(raw_tx)
        # update tx index
        self.txs[tx_hash] = tx
        # log all the outputs in the transaction
        if 'vout' in tx:
            outputs = tx['vout']
            for output in outputs:
                self.log_output(tx_hash, output)
        # all the inputs were once unspent outputs, but now they are spent...
        # make sure they are marked as such
        if 'vin' in tx:
            inputs = tx['vin']
            for input in inputs:
                self.spend_input(tx_hash, input)

        self.check_for_nulldata(tx, block_number)

    def index(self, first_block=None, last_block=None):
        if not first_block and last_block:
            block_count = self.bitcoind.getblockcount()
            first_block, last_block = 0, block_count

        for block_number in range(first_block, last_block+1):
            print "\n%s%s%s" % ("="*10, str(block_number), "="*10)
            block_hash = self.bitcoind.getblockhash(block_number)
            block_data = self.bitcoind.getblock(block_hash)
            if 'tx' in block_data:
                tx_hashes = block_data['tx']
                for tx_hash in tx_hashes:
                    self.process_tx(tx_hash, block_number)

    def save_address_txs(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.address_txs, cls=ExtendedJSONEncoder))

    def save_nulldata_txs(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(self.nulldata_txs, cls=ExtendedJSONEncoder))

def get_bitcoind_client():
    try:
        with open('tests/secrets.json', 'r') as f:
            SECRETS = json.loads(f.read())
    except Exception as e:
        traceback.print_exc()
        return None

    bitcoind_client = BitcoindClient(SECRETS['rpc_username'], SECRETS['rpc_password'])
    return bitcoind_client

from datetime import datetime

def main():
    start = datetime.now()
    first_block, num_blocks = 331757, 2
    bitcoind_client = get_bitcoind_client()
    if bitcoind_client:
        block_count = bitcoind_client.bitcoind.getblockcount()
        blockchain = Blockchain(bitcoind_client)
        blockchain.index(first_block, first_block+num_blocks-1)
        blockchain.save_address_txs('ignore/address_txs.txt')
        blockchain.save_nulldata_txs('ignore/nulldata_txs.txt')
    end = datetime.now()
    delta = end - start
    print "%s seconds" % delta.seconds

if __name__ == '__main__':
    main()
