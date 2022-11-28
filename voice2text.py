import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
import cv2
import time
import speech_recognition as sr
import sys

# Mientras run=True, corre el programa
run = True
active = False

class Template(object):
	def __init__(self, args):
		super(Template, self).__init__()
		self.args = args

		# Publisher de voz
		self.pub_voz = rospy.Publisher("/duckiebot/voz/v2t", String, queue_size=10)
		self.pub_tiempo = rospy.Publisher("/duckiebot/voz/tiempo", String, queue_size=1)

		# Subscribers
		rospy.Subscriber("/duckiebot/joy", Joy, self.callback_control)
		rospy.Subscriber("/duckiebot/voz/publicar_msg", String, self.callback_req)

		# Programa de voz
		self.r = sr.Recognizer()

		self.A = 0
		self.X = 0

	def callback(self, auto=False):
		# Modifico los valores globales
		global run, active

		if self.X == 1:
		    run = False
		    return

		# Ejecutar el microfono solo si no esta activo (evita lag)
		if (self.A == 1 and not active) or auto:
			active = True
			with sr.Microphone() as source:
				print("Quack quack...")  # que lo diga
				audio = self.r.listen(source, None, 1.5)

				try:
					text = self.r.recognize_google(audio, language='es-ES')
					print("Lo quack dijiste fue:", str(text))
					msg = String()
					msg.data = str(text)
					
					# Si se llama desde el programa, es tiempo (en segundos)
					if auto:
						self.pub_tiempo.publish(msg)
					# Sino, es probablemente una instruccion
					else:
						self.pub_voz.publish(msg)
				except Exception as e:
					print("No quackche", str(e))

				active = False

	def callback_control(self, msg):
		buttons = list(msg.buttons)

		self.A = buttons[0]
		self.X = buttons[2]
		
	def callback_req(self, msg):
		self.callback(True)
		

def main():
	# Nodo local del PC
	rospy.init_node("pc")

	print("Funcionando!")

	obj = Template('args')

	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		if run == False:
			sys.exit()
	    
		obj.callback()
		rate.sleep()

if __name__ == '__main__':
	main()
