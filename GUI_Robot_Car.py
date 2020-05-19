from tkinter import *
#import paho.mqtt.subscribe as subscribe
#import paho.mqtt.publish as publish
import time
import serial
root=Tk()
miFrame=Frame(root)
miFrame.pack()
Servo_cont=20
Fwd_cont=False
Rev_cont=False

Led_cont=0
arg=0
arduino = serial.Serial('COM4', 9600)


#................................Labels..........................................

Distance_measured_label=Label(miFrame,text="Distancia Medida: ")
Distance_measured_label.grid(row=0,column=0,padx=10,pady=10)

Distance_ran_label=Label(miFrame,text="Distancia Recorrida: ")
Distance_ran_label.grid(row=1,column=0,padx=10,pady=10)

Aprox_speed_label=Label(miFrame,text="Velocidad Aprox: ")
Aprox_speed_label.grid(row=2,column=0,padx=10,pady=10)

Temperature_label=Label(miFrame,text="Temperatura:")
Temperature_label.grid(row=3,column=0,padx=10,pady=10)

Servo_pos_label=Label(miFrame,text="Posicion del servo:")
Servo_pos_label.grid(row=4,column=0,padx=10,pady=10)


#..............................Entries........................................

Distance_measured=StringVar()
Distance_measured_Entry=Entry(miFrame,textvariable=Distance_measured)
Distance_measured_Entry.grid(row=0,column=1,padx=10,pady=10)

Distance_ran=StringVar()
Distance_ran_Entry=Entry(miFrame,textvariable=Distance_ran)
Distance_ran_Entry.grid(row=1,column=1,padx=10,pady=10)

Aprox_speed=StringVar()
Aprox_speedEntry=Entry(miFrame,textvariable=Aprox_speed)
Aprox_speedEntry.grid(row=2,column=1,padx=10,pady=10)

Temperature=StringVar()
TemperatureEntry=Entry(miFrame,textvariable=Temperature)
TemperatureEntry.grid(row=3,column=1,padx=10,pady=10)

Servo_pos=StringVar()
Servo_pos_Entry=Entry(miFrame,textvariable=Servo_pos)
Servo_pos_Entry.grid(row=4,column=1,padx=10,pady=10)





#......................Functions Part.................................................


def ServoUp():
	global Servo_cont
	Servo_cont=int(Servo_cont)+1
	if(Servo_cont>99):
		Servo_cont=99
	Servo_pos.set(str(Servo_cont))
	Servo_cont= str(Servo_cont).encode('utf-8')
	arduino.write(Servo_cont)
	arduino.write(b'\n')
	

def ServoDown():
	global Servo_cont
	Servo_cont=int(Servo_cont)-1
	if(Servo_cont<20):
		Servo_cont=20
	Servo_pos.set(str(Servo_cont))
	Servo_cont= str(Servo_cont).encode('utf-8')
	arduino.write(Servo_cont)
	arduino.write(b'\n')
	

def getData(string_received):
	x = string_received.find(":")
	Data=string_received[x+1:]
	return Data


def StartFunction(button):
	global Fwd_cont
	global Rev_cont

	if button==0:
		Fwd_cont= not Fwd_cont
		

	if button==1:
		Rev_cont=not Rev_cont
		

	if Fwd_cont == False and Rev_cont == False:
		Fwd_text.set("Avanzar")
		Rev_text.set("Retroceder")
		arduino.write(b'1')
		arduino.write(b'\n')

	if Fwd_cont == True and Rev_cont == False:
		Fwd_text.set("Stop")
		arduino.write(b'3')
		arduino.write(b'\n')

	if Rev_cont == True and Fwd_cont == False:
		Rev_text.set("Stop")
		arduino.write(b'2')
		arduino.write(b'\n')
	
	

def LedTurn():
	global Led_cont
	Led_cont+=1
	if Led_cont%2==0:
		Led_text.set("Encender")
		arduino.write(b"9")
		arduino.write(b'\n')
	else:
		Led_text.set("Apagar")
		arduino.write(b"8")
		arduino.write(b'\n')
		
	
def SerialEvent():
	#global arg

	rawString = arduino.readline()
	rawString = rawString.decode('utf-8')
	#print(rawString)
	

		
	if "Distance:" in rawString:
		Distance_measured.set(getData(rawString))
		#print("Distance "+Distance)
			
	if "Distancia Recorrida:" in rawString:
		Distance_ran.set(getData(rawString))
		#print("Distancia Recorrida "+Distance_ran)
		
	if "Velocidad:" in rawString:
		Aprox_speed.set(getData(rawString))

	if "Temperatura:" in rawString:
		Temperature.set(getData(rawString))
		#print("Temperature "+Temperature)

	root.after(100,SerialEvent)
	
Fwd_text=StringVar()
Rev_text=StringVar()
Led_text=StringVar()
Fwd_text.set("Avanzar")
Rev_text.set("Retroceder")
Led_text.set("Encender")

#..................................Botones......................................

ServoUp_button=Button(miFrame,text="+ Posicion Servo",width=15,command=lambda:ServoUp(),fg="White",bg="Green")
ServoUp_button.grid(row=0,column=3,padx=10,pady=10)

ServoDown_button=Button(miFrame,text="- Posicion Servo",width=15,command=lambda:ServoDown(),fg="White",bg="Red")
ServoDown_button.grid(row=1,column=3,padx=10,pady=10)

Led_button=Button(miFrame,textvariable=Led_text,width=15,command=lambda:LedTurn(),fg="White",bg="Gray")
Led_button.grid(row=2,column=3,padx=10,pady=10)

Direction_button=Button(miFrame,textvariable=Fwd_text,width=15,command=lambda:StartFunction(0),fg="White",bg="Gray")
Direction_button.grid(row=3,column=3,padx=10,pady=10)

Start_button=Button(miFrame,textvariable=Rev_text,width=15,command=lambda:StartFunction(1),fg="White",bg="Gray")
Start_button.grid(row=4,column=3,padx=10,pady=10)


#...........................Variables de Inicio/Referencia.........................
Distance_ran_ref=0
Aprox_speed_ref=0
Temperature_ref=26
Servo_pos_ref=20



#.............................Loop Start....................................
"""
Distance_ran.set(Distance_ran_ref)
Aprox_speed.set(Aprox_speed_ref)
Temperature.set(Temperature_ref)
"""
Servo_pos.set(Servo_pos_ref)






#.............................INICIO DE PARAMETROS BASICOS..................


root.after(100,SerialEvent)


root.mainloop()    #INICIO DE BUCLE