import time

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import  PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block

pn_config = PNConfiguration()
pn_config.subscribe_key = 'sub-c-9638809a-cecc-11ec-a368-1a35c262c233'
pn_config.publish_key = 'pub-c-39e8bfae-0f60-4003-899f-ebc776b77ed2'
pubnub = PubNub(pn_config)

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}

#pubnub.subscribe().channels([TEST_CHANNEL]).execute()

class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print('\n -- Successfully replaced the local chain')
            except Exception as e:
                print(f'\n -- The chain is not replaced: {e}')
#pubnub.add_listener(Listener())

class PubSub():
    def __init__(self, blockchain):
        self.pubnub = PubNub(pn_config)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))
    def publish(self, channel, message):
        self.pubnub.publish().channel(channel).message(message).sync()
    def broadcast_block(self, block):
        self.publish(CHANNELS['TEST'], block.to_json())

def main():
    pubsub =PubSub()

    time.sleep(1)

    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar' })

if __name__ == '__main__':
    main()