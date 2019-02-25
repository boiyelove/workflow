# from django.http import HttpResponse
# from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session

# def http_consumer(message):

# 	response = HttpResponse("Hello wordl! You asked for %s" % message.content['path'])
# 	for chunk in AsgiHandler.encode_response(response):
# 		message.reply_channel.send(chunk)

# def ws_message(message):
# 	message.reply_channel.send({
# 		"text": message.content['text'],
# 		})



#connected to werbsocket.connect
# def ws_add(message):
# 	message.reply_channel.send({"accept":True})
# 	Group("Chat").add(message.reply_channel)

#connected to websocket.disconnect
# def ws_connect(message):
# 	Group("chat").discard(message.reply_channel)


#connected to websocket.connect
# def ws_add(message):
# 	message.reply_channel.send({"accept": True})
# 	Group("chat").add(message.reply_channel)

#connected to websocket.receive
# def ws_message(message):
# 	Group("chat").send({
# 		"text": "[user] %s" % message.content["text"],
# 		})

#connected to websocket.disconnect
# def ws_disconnect(message):
# 	Group("Chat").discard(message.reply_channel)


@channel_session
def ws_connect(message):
	message.reply_channel.send({
		"accept": True
		})
	room = message.content['path'].strip("/")
	message.channel_session['room'] = room
	Group("chat-%s" % room).add(message.reply_channel)


@channel_session
def ws_message(message):
	Group('chat-%s' % message.channel_session['room']).send({
		'text': message['text'],
		})