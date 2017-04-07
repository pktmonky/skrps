import re
import random
import string
with open('js') as f:
	s = f.read()
s = s.replace('function ','function_').replace('var ','var_')
s = re.sub("[\t\n]","",s)
s = re.sub(r' ?([=+]) ?',r'\1',s)
fs=[]
p = re.compile(r'function_([0-9a-zA-Z]+)\(')
for m in re.finditer(p,s):
	fs.append(m.group(1))
vs=[]
p = re.compile(r'var_([0-9a-zA-Z]+)\=')
for m in re.finditer(p,s):
	vs.append(m.group(1))
for f in fs:
	s = s.replace(f,''.join(random.choice(string.ascii_uppercase) for _ in range(6)))
for v in vs:
	s = s.replace(v,''.join(random.choice(string.ascii_uppercase) for _ in range(6)))
s = re.sub(r'(function_[^{]+){',r'\1{dq=String.fromCharCode;',s);
s = s.replace('="',"'+dq(0x3d)+'\"").replace('"',"'+dq(0x22)+'").replace('<',"'+dq(60)+'")
s = s.replace('>',"'+dq(62)+'").replace('/',"'+dq(parseInt(57,8))+'").replace(' ',"'+dq(parseInt(40,8))+'")
s = s.replace(':',"'+dq(58)+'").replace('%',"'+dq(0x25)+'")
s = s.replace("+''+","+").replace("=''+","=").replace("+'';",";").replace('_',' ')
p = re.compile(r"'([^']+)'")
for m in re.finditer(p,s):
	s = s.replace(m.group(0),str(int(m.group(1),36))+'..toString(36)')
print s


