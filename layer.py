from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity

from chatterbotapi import ChatterBotFactory, ChatterBotType
from HTMLParser import HTMLParser

factory = ChatterBotFactory()

bot = factory.create(ChatterBotType.CLEVERBOT)
bot_sessions = dict()

class EchoLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

            message_txt = messageProtocolEntity.getBody()
            to = messageProtocolEntity.getFrom()
            
            if to not in bot_sessions.keys():
                print "adding {} to participants".format(to)
                bot_sessions[to] = bot.create_session()
            bot_answer = bot_sessions[to].think(message_txt)
            text = "Bot answers: {}".format(HTMLParser().unescape(bot_answer).encode("utf-8"))
            print "Got <{}> from {}".format(message_txt, to)
            print "Answering with <{}>".format(text)
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(text, to = to)
            
            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery", entity.getFrom())
        self.toLower(ack)
