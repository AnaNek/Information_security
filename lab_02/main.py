import random

'''
ALPHABET = [chr(i) for i in range(256)]
'''
''' ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", " "]
'''

class Rotor():
    def __init__(self, seed):
        self.alphabet = [chr(i) for i in range(256)]
		self.routes = range(len(alphabet))
		random.seed(seed)
		random.shuffle(self.routes)
     
    def __str__(self):
		s = ''
		for i in range(len(self.alphabet)):
			s += '%s %i => %i\n' % (self.alphabet[i], i, self.routes[i])
		return s
		   
    def forward(self, index):
		return self.routes[index]
	
	def backwards(self, index):
		return self.routes.index(index)
		
	def rotate(self):
	    self.routes = shift(self.routes, 1)
	   
class Reflector():
    def __init__(self):
		pass
     
    def __str__(self):
		s = ''
		for i in range(len(self.alphabet)):
			s += '%s %i => %i\n' % (self.alphabet[i], i, self.routes[i])
		return s
		   
    def encrypt(self, index):
		return self.routes[index]
