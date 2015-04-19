#imports
import subprocess
import os
import filecmp
import md5
import hashlib
import time
#shutil.move
#end imports
#
#DEBUG mode
debug = True
#File Paths
myPFS_path = "MyPFS"
cache_path = "cache"
NUM_NODES = 4
#DIR_MyPFS = none
##########
#Functions
##########
#
#
def listDirectories():
        subprocess.call(['ls', '-lR'])
        
#LAUNCH RPFS    
def launch():
        print "Welcome to RPFS!"
        os.mkdir(myPFS_path)
        os.mkdir(cache_path)
        if debug:
                print "[MyPFS and cache created successfully]"
        for i in range(0, NUM_NODES):
                node_name = 'node' + str(i+1)
                os.mkdir(myPFS_path +'/' +  node_name)
                os.mkdir(cache_path + '/' + node_name)
        if debug:
                print '[Nodes creates successfully]'
                print '[Now mounting the cache nodes]'
        for i in range(0, NUM_NODES):
                node_name = 'node' + str(i+1)
                #path to mount to
                original_path = myPFS_path + '/' + node_name
                #path to be mounted
                mount_path = cache_path + '/' + node_name
                #mount mount_path to original_path
                subprocess.Popen(["rpfs", original_path, mount_path])
        DIR_MyPFS = myPFS_path
 

                
############################### 
#CONSISTENT HASHING STARTS HERE 
#A single node for the circular linked list    
class Node:
	def __init__(self, i):
		self.name = 'node'+str(i)
		self.next_node = None
		self.idx = i
		self.flag = True
	#sets the next__node field for self	
	def setNext(self, next):
		self.next_node = next
	#gets the next node field of a node	
	def getNext(self):
		return self.next_node
	#gets the current status of the flag	
	def getFlag(self):
		return self.flag
	#ensures the flag is turned OFF	
	def turnOff(self):
		self.flag = False
	#ensures that the flag is turned ON
	def turnOn(self):
		self.flag = True
	#returns the name of the node	
	def getName(self):
		return str(self.name)
		
#Circular Linked List 	
class HashLinkedList:
	def __init__(self):
		self.size = 0
		self.dummy = Node(0)
		head = self.dummy
		#print 'Name = ' + (head).getName()
		self.dummy.setNext( head )
	#returns the current size, ie how many nodes (excluding the dummy	
	def getSize(self):
		return self.size
	#adds a node to the CLL
	def add_node(self):
		if self.size == 0:
			nn = Node(1)
			self.dummy.setNext(nn)
			nn.setNext(self.dummy)
			self.size = 1
		else:
			curr = self.dummy
			i = 0
			while i < self.size:
				i = i +1
				curr = curr.getNext() #end while
			nn = Node(self.size+1)
			curr.setNext(nn)
			nn.setNext(self.dummy)
			self.size = self.size+1
	#print the list [used for debugging]	
	def printList(self):
		i = 0
		curr = self.dummy
		while i < 11:
			print curr.getName()
			curr=  curr.getNext()
			i = i +1
			
class HashRing():
	def __init__(self, n):
		self.hashLinkedList = HashLinkedList()
		i = 1
		self.MAX_NODES = n
		self.num_nodes = n
		while i <= n:
			self.hashLinkedList.add_node()
			i = i + 1
	
	def killNode():
		self.num_nodes = self.num_nodes - 1
	
	def calculateNode(self, filename):
		#hash the filename
		m = hashlib.md5()
		print '[DEBUG calculate hashed node..'
		m.update(str(filename))
		generatedHash = m.hexdigest()
		hash100 = (int(str(generatedHash), 16)%100 + 1)		
		if debug:
			print '\tmd5 = ' + str(generatedHash)
			print '\thash100 = ' + str(hash100) + ']'
		folder = 0
		if hash100 > 80:
			folder = 5
		elif hash100 > 60:
			folder = 4
		elif hash100 > 40:
			folder = 3
		elif hash100 > 20:
			folder = 2
		else:
			folder = 1
		return folder
		
	def printRing(self):
		self.hashLinkedList.printList()

def ringTest():
	hr = HashRing(5)
	print 'Filename1 node: ' + str(hr.calculateNode("file1"))
	print 'Filename2 node: ' + str(hr.calculateNode("file2"))
	print 'Filename3 node: ' + str(hr.calculateNode("file3"))
	print 'Filename4 node: ' + str(hr.calculateNode("file4"))
	print 'Filename5 node: ' + str(hr.calculateNode("file5"))
	#hr.printRing()
#CONSISTENT HASHING ENDS HERE 
#############################
                
#SHUTDOWN RPFS 
def shutDown():
        #TODO: unmount
        subprocess.Popen(["fusermount", "-u", "cache/node1"])
        subprocess.Popen(["fusermount", "-u", "cache/node2"])
        subprocess.Popen(["fusermount", "-u", "cache/node3"])
        subprocess.Popen(["fusermount", "-u", "cache/node4"])
        subprocess.call(['rm', '-rf', myPFS_path])
        subprocess.call(['rm', '-rf', cache_path])
        if debug:
                print "[Deleted directories]"
        print "RPFS has shut down"

# listens for added files to directories
def dirListen():
	if debug:
		print 'Listening...\n'
	A = set(os.listdir(myPFS_path))
	r = HashRing(5)
	while( True ):
		B = set(os.listdir(myPFS_path))
		C = B-A
		if C:
			if debug:
				print 'Changes in MyPFS = ' + str(C)
			nf = C.pop()
			filename = nf.split('.')[0]
			print str(filename)
			folder_no = r.calculateNode(nf)
			fromPath = myPFS_path+'/'+str(nf)
			moveTo = myPFS_path+'/'+'node'+str(folder_no)
			print ('Moveto: ' + str(moveTo))
			subprocess.call(['cp', '-a', fromPath, moveTo ])
		A = B
        	
            

#main function
def _main():
        #launch()
        dirListen()
        #ringTest()
        


#start with  main
_main()

