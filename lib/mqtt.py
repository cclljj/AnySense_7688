import paho.mqtt.publish as publish

class mqtt:
	def __init__(self, MQTT_broker, MQTT_port, MQTT_topic):
		self.host = MQTT_broker
		self.port = MQTT_port
		self.topic = MQTT_topic

	def pub(self, data):
		try:
			publish.single(self.topic, data, hostname=self.host, port = self.port)
		except:
			print('Send Error !')

		


