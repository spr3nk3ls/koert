from common import MildErr, ManyMildErrs, ObjDirErr

# raised when the string representation of a countlet
# has a white object name.
class NoObjStrErr(MildErr):
	pass

class Count:
	def __init__(self, countlets, constr):
		self.countlets = countlets
		self.constr = constr

	def map(self, f, comb=lambda x,y: sum((x,y))):
		res = dict()
		for item in self.countlets.iteritems():
			for k,v in f(*item):
				if k in res:
					res[k] = comb(res[k],v)
				else:
					res[k] = v
		return Count(res, self.constr)

	def total(self, f=lambda x:x, zero=0):
		return sum([f(obj) * self.countlets[obj] 
			for obj in self.countlets], zero)
	
	@classmethod
	def zero(cls, constr):
		return Count({}, constr)
	
	def __getitem__(self, item):
		return self.countlets[item]

	def __contains__(self, item):
		return item in self.countlets

	def __iter__(self):
		return iter(self.countlets)

	def __repr__(self):
		return "\n".join(["%s: %s" % (obj, amount) for 
			obj, amount in self.countlets.iteritems()])

	@classmethod
	def from_array(cls, ar, objdir, constr):
		countlets = {}
		errors = []
		for line in ar:
			if len(line)==0:
				continue
			try:
				obj, amount = cls.countlet_from_line(line, 
						objdir, constr)
			except NoObjStrErr as e:
				errors.append(e)
				continue
			## to get errors on all missing products
			except ObjDirErr as e:
				errors.append(e)
				continue
			if obj in countlets:
				raise MildErr("obj appears twice: '%s'"
						"(amount: %s)"
						% (obj, amount))
			countlets[obj] = amount
		if len(errors)>0:
			raise ManyMildErrs(errors)
		return cls(countlets=countlets, constr=constr)
	
	@classmethod
	def countlet_from_line(cls, line, objdir, constr):
		if len(line)==0:
			raise ValueError("no object given")
		obj_str = line[0]
		if(obj_str==""):
			raise NoObjStrErr()
		obj = objdir[obj_str]
		amount = None
		if len(line)==1:
			amount = 0
		else:
			amount_str = line[1]
			try:
				amount = 0 if amount_str=="" \
						else constr(amount_str)
			except ValueError:
				raise MildErr("could not parse amount: '%s'" \
						% amount_str)
		return obj, amount

	def __add__(self, other):
		countlets = {}
		for a in (self, other):
			for obj in a.countlets.iterkeys():
				if obj not in countlets:
					countlets[obj] = self.constr(0)
				countlets[obj] += a[obj]
		return Count(countlets=countlets, constr=self.constr)
	
	def __neg__(self):
		countlets = {}
		for obj in self.countlets.iterkeys():
			countlets[obj] = -self.countlets[obj]
		return Count(countlets, self.constr)
	
