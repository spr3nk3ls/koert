import csv

class yaExcelDialect(csv.Dialect):
	delimiter = ";"
	quotechar = '"'
	doublequote = True
	skipinitialspace = False
	lineterminator = "\r\n"
	quoting = csv.QUOTE_MINIMAL

def read_rikf(f):
	return csv.reader(comment_stripper(f), 
			dialect = yaExcelDialect)

def open_rikf_ar(p):
	with open(p) as f:
		try:
			return list(read_rikf(f))
		except csv.Error as e:
			print "the path was: %s" % p
			raise e


def comment_stripper(f):
	for line in f:
		decom = line.split("#",1)[0].strip()
		if len(decom)==0:
			continue
		yield decom
		
