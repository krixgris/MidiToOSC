#	Algorithms from https://easings.net
#
#	Excluded algos that go above 1 or below 0 
import math

#region easeIn
def easeInSine(x):
	return 1 - math.cos((x * math.pi) / 2)

def easeInCubic(x):
	return x * x * x

def easeInQuint(x):
	return x * x * x * x * x

def easeInCirc(x):
	return 1 - math.sqrt(1 - pow(x, 2))

def easeInQuad(x):
	return x*x

def easeInQuart(x):
	return x * x * x * x

def easeInExpo(x):
	if x == 0:
		val = 0
	else:
		val = pow(2, 10 * x - 10)
	return val
#endregion

#region easeOut
def easeOutSine(x):
	return math.sin((x * math.pi) / 2)

def easeOutCubic(x):
	return 1 - pow(1 - x, 3)

def easeOutQuint(x):
	return 1 - pow(1 - x, 5)
	
def easeOutCirc(x):
	return math.sqrt(1 - pow(x - 1, 2))

def easeOutQuad(x):
	return 1 - (1 - x) * (1 - x)

def easeOutQuart(x):
	return 1 - pow(1 - x, 4)

def easeOutExpo(x):
	if x == 1:
		return 1
	else:
		return 1 - pow(2, -10 * x)
#endregion

#region easeInOut
def easeInOutSine(x):
	return -(math.cos(math.pi * x) - 1) / 2
	
def easeInOutCubic(x):
	if(x < 0.5):
		val = 4 * x * x * x
	else:
		val = 1 - pow(-2 * x + 2, 3) / 2
	return val

def easeInOutQuint(x):
	if(x < 0.5):
		val = 16 * x * x * x * x * x
	else:
		val = 1 - pow(-2 * x + 2, 5) / 2
	return val

def easeInOutCirc(x):
	if(x < 0.5):
		val = (1 - math.sqrt(1 - pow(2 * x, 2))) / 2
	else:
		val = (math.sqrt(1 - pow(-2 * x + 2, 2)) + 1) / 2
	return val

def easeInOutQuad(x):
	if x < 0.5:
		return 2 * x * x
	else:
		return 1 - pow(-2 * x + 2, 2) / 2
	
def easeInOutQuart(x):
	if x < 0.5:
		return 8 * x * x * x * x
	else:
		return 1 - pow(-2 * x + 2, 4) / 2

def easeInOutExpo(x):
	if x == 0:
		return 0
	elif x == 1:
		return 1
	elif x < 0.5:
		return pow(2, 20 * x - 10) / 2
	else:
		return (2 - pow(2, -20 * x + 10)) / 2
#endregion

#region weirdOnes
def easeInElastic(x):
	c4 = (2 * math.pi) / 3

	if x == 0:
		return 0
	elif x == 1:
		return 1
	else:
		return -pow(2, 10 * x - 10) * math.sin((x * 10 - 10.75) * c4)

def easeOutElastic(x):
	c4 = (2 * math.pi) / 3

	if x == 0:
		return 0
	elif x == 1:
		return 1
	else:
		return pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1

def easeInOutElastic(x):
	c5 = (2 * math.pi) / 4.5
	if x == 0:
		return 0
	elif x == 1:
		return 1
	elif x < 0.5:
		return -(pow(2, 20 * x - 10) * math.sin((20 * x - 11.125) * c5)) / 2
	else:
		return (pow(2, -20 * x + 10) * math.sin((20 * x - 11.125) * c5)) / 2 + 1

def easeInBack(x):
	c1 = 1.70158
	c3 = c1 + 1
	if x == 0:
		return c3 * x * x * x - c1 * x * x

def easeOutBack(x):
	c1 = 1.70158
	c3 = c1 + 1
	return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2)

def easeInOutBack(x):
	c1 = 1.70158
	c2 = c1 * 1.525

	if x < 0.5:
		return (pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
	else:
		return (pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2

def easeInBounce(x):
	return 1 - easeOutBounce(1 - x)
	
def easeOutBounce(x):
	n1 = 7.5625
	d1 = 2.75

	if (x < 1 / d1):
		return n1 * x * x
	elif (x < 2 / d1):
		x1 = x-1.5 / d1
		return n1 * x1 * x1 + 0.75
	elif (x < 2.5 / d1):
		x1 = x-2.25 / d1
		return n1 * x1 * x1 + 0.9375
		# return n1 * x1 * x1 + 0.9375
		#return n1 * (x -= 2.25 / d1) * x + 0.9375
	else:
		x1 = x-2.625 / d1
		return n1 * x1 * x1 + 0.984375

def easeInOutBounce(x):
	if x < 0.5:
		return (1 - easeOutBounce(1 - 2 * x)) / 2
	else:
		return (1 + easeOutBounce(2 * x - 1)) / 2
#endregion