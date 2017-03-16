import os;
import random;
import uuid; 
import string;
import sys;
import argparse;
from urllib2 import urlopen;
import imghdr;
import base64;

class genHTA(object):
	def __init__(self):
		self.args = None
		self.templates = {'TITLE': self.title, 'WINSTATE': self.winstate, 'SUBTITLE': self.subtitle,'BANNER': self.banner, 'ABOUT1': self.aboutone, 'ABOUT2': self.abouttwo,'QUESTION_BLOCK': self.qb,'SUBMIT_MESSAGE': self.sm}
		self.vtitle = ""
		self.vwinstate = ""
		self.vsubtitle = ""
		self.vbanner = ""
		self.vaboutone = ""
		self.vabouttwo = ""
		self.vqb = ""
		self.vsm = ""

	globalDim = []
	newlines = []
	
	def title( self ):
		return self.vtitle

	def winstate( self ):
		return self.vwinstate

	def subtitle( self ):
		return self.vsubtitle

	def banner( self ):
		return self.vbanner

	def aboutone( self ):
		return self.vaboutone

	def abouttwo( self ):
		return self.vabouttwo

	def qb( self ):
		return self.vqb

	def sm( self ):
		return self.vsm

	def randbool(self):
		return (random.random() >= 0.5)

	def populate( self ):
		print "[*] Begin populating with data, insert information now."
		print ""
		print "Title - This is the name of the campaign or could be the organisation you are posing to be."
		self.vtitle = raw_input("\033[1;30m[*] Title: \033[0;0m")
		print ""
		print "Do you want for the HTA to be maximised? (Y/N)"
		a = ""
		while (not (a.upper() == "Y" or a.upper() == "N")):
			a = raw_input("\033[1;30m[*] Maximised: \033[0;0m")
			if a.upper() == "Y":
				self.vwinstate = self.obfuscate("WINDOWSTATE=\"maxIMize\"")
			elif a.upper() == "N":
				self.vwinstate = ""
			else:
				print "\033[1;31m[!] You must specify either Y/N\033[0;0m"

		print ""
		print "Subtitle - Enter a subtitle that will appear as part of the campaign."
		self.vsubtitle = raw_input("\033[1;30m[*] Subtitle: \033[0;0m")

		print ""
		print "Banner - Enter a URL or local path for the image that you would like embedded."
		while (True):
			b = raw_input("\033[1;30m[*] Banner location: \033[0;0m")
			try:
				f = open('temptemptemptemptemptemp', 'wb')
				f.write(urlopen(b).read())
				f = open('temptemptemptemptemptemp')
			except ValueError:
				try:
					f = open(b)
				except:
					print "\033[1;31m[!] Invalid location\033[0;0m"
					continue
			imagetype = imghdr.what(f)
			if imagetype:
				encode = base64.b64encode(f.read())
				self.vbanner = "data:image/%s;base64,%s" % (imagetype, encode)
				break
			else:
				print "\033[1;31m[!] Invalid location\033[0;0m"
				continue

			f.close()

			#print f.read()

		print ""
		print "Describe the questionnaire, why are we conducting this?"
		print "Begin by writing a quick few sentences on who the organisation are."

		self.vaboutone = raw_input("\033[1;30m[*] About Organisation: \033[0;0m")

		print ""
		print "Now describe why you are conducting this question."

		self.vabouttwo = raw_input("\033[1;30m[*] About the questionnaire: \033[0;0m")

		print ""
		print "Now we will begin with inserting questions in the document."

		print "How many questions would you like in the form?"

		qnum = -1

		while qnum < 0:
			qnum = int(raw_input("\033[1;30m[*] Number of questions: \033[0;0m"))
			
		#print qnum
		print ""
		
		doneCount = 0
		print "There are currently three choices of questions you can have."
		print "(1) radio selector, (2) input box, (3) textarea"

		qlines = ""

		for i in range(0, qnum):
			while doneCount < qnum:
				select = 0
				while True:
					try:
						select = int(raw_input("\033[1;30m[*] ID of choice (1/2/3): \033[0;0m"))
						break
					except:
						print "\033[1;31m[!] Invalid choice\033[0;0m"
						continue
				if select >= 1 and select <= 3:
					doneCount += 1
				else:
					print "\033[1;31m[!] Invalid choice\033[0;0m"
					continue

				print ""
				qStr = raw_input("\033[1;30m[*] Enter a question: \033[0;0m")

				qlines += ("<h3>%s</h3>\r\n" % qStr)

				print ""

				if select == 1:
					#print "Radio Selected"
					rNum = 0
					while True:
						rNum = int(raw_input("\033[1;30m[*] How many radio buttons would you like? (1-10): \033[0;0m"))
						if rNum >= 1 and rNum <= 10:
							break
						else:
							print "\033[1;31m[!] Invalid choice\033[0;0m"
							continue
					lStr = raw_input("\033[1;30m[*] A word to describe the worst option (eg. No, terrible, worst, strongly disagree): \033[0;0m")
					rStr = raw_input("\033[1;30m[*] A word to describe the best option (eg. Yes, fantastic, best, strongly agree): \033[0;0m")
					print ""

					qlines += ("<label>%s</label> |" % lStr)
					for j in range(0,rNum):
						qlines += ("<input type=\"radio\" name=\"q%s\" />" % doneCount)

					qlines += (" | <label>%s</label><p>" % rStr)

				elif select ==2:
					#print "Input Box Selected"
					qlines += ("<input type=\"text\" name=\"q%s\" style=\"width:1000px\" /><br><p>" % doneCount)

				else:
					#print "Textarea Selected"
					qlines += ("<textarea style=\"width:1000px;height:200px\" name=\"q%s\"></textarea><p>" % doneCount)

		self.vqb = qlines

		print ""
		print "Submit Message - The message to display after submitting the form."

		self.vsm = raw_input("\033[1;30m[*] Submit Message: \033[0;0m")




	def obfuscate( self, line ):
		base = ""
		for i in line:
			value = ""
			if self.randbool():
				# uppercase it
				value = i.upper()
			else:
				# lower() it
				value = i.lower()
			base += value
		return base

	def printBanner(self):
		with open('banner.txt', 'r') as f:
			data = f.read()
			print "\033[1;31m%s\033[0;0m" % data
			print "Non-malicious anti-sandbox analysis HTA File Generator"
			print "Author: Vincent Yiu (@vysecurity)"

	def output(self):
		print "\033[1;33m[+] Writing payload to \033[1;31m%s\033[0;0m" % self.args.out
		f = open(self.args.out, "w+")
		#self.newlines
		f.write('\n'.join(self.newlines))
		f.close()
		print "\033[1;33m[+] Payload written\033[0;0m"

	def make_argparser(self):
		parser = argparse.ArgumentParser(description = "")
		#parser.add_argument("--image", metavar="<image_location_or_url>", dest = "img", default = "https://media.mnn.com/assets/images/2016/08/pinkblob.jpg.653x0_q80_crop-smart.jpg", help = "URL of image to use")
		parser.add_argument("--out", metavar="<output_file>", dest = "out", default = "output.hta", help = "File to output the generated HTA to")
		#parser.add_argument("--noMaximise", dest = "bMaximise", default = "True", action = "store_false")

		return parser

	def check_args(self, args):
		self.args = args

	def run(self, args):
		self.printBanner()

		print ""

		self.check_args(args)

		print ""
		print "[*] genHTA Started"
		self.populate()
		self.output()

	def generate_output(self):
		f = open("template.txt", "r")
		output = ""
		for line in f.readlines():
			for template in self.templates:
				template_text = "{{" + template + "}}"
				if template_text in line:
					line = line.replace(template_text, self.templates[template]())
					
			# Only output on non-blank lines
			if line and line != "\r\n":
				output += line
		#print output
		print "[+] Generated HTA"
		return output

	def output(self):
		# Open and write to text file

		print "[+] Open file: %s" % self.args.out

		f = open(self.args.out, 'w+')

		f.writelines(self.generate_output())

		f.close()

		print "[+] Payload written"

		print ""


if __name__ == '__main__':
	m = genHTA()
	parser = m.make_argparser()
	arguments = parser.parse_args()
	m.run(arguments)
