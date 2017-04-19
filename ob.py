#!/usr/bin/python
import random
import string
import base64
import re

# custom Base64 encoder
def encode(s):
	return base64.b64encode(s).translate(
		string.maketrans(
			string.uppercase+string.lowercase+string.digits+"+/",
			string.digits+string.uppercase+string.lowercase+"+/"
		)
	)

# chunk base64 data into random sizes
def chunk(s):
	c=[]
	i=0
	while(i<len(s)):
		j=random.choice(range(5,20))
		c.append(s[i:i+j])
		i+=j
	return c

# 1. load Javascript file
with open('step1.js') as f:
	s = f.read()
# 2. save required spaces, remove unnecessary formatting
s = s.replace('function ','function_').replace('var ','var_')
s = re.sub(r' ?([=+]) ?',r'\1',re.sub("[\t\n]","",s))
# 3. randomize function and variable names
fs=[]
vs=[]
p = re.compile(r'function_([0-9a-zA-Z]+)\(([^)]+)\)')
for m in re.finditer(p,s):
	fs.append(m.group(1))
	vs.append(m.group(2))
p = re.compile(r'var_([0-9a-zA-Z]+)[;=]')
for m in re.finditer(p,s):
	vs.append(m.group(1))
for f in fs:
	s = s.replace(f,''.join(random.choice(string.ascii_uppercase) for _ in range(6)))
for v in vs:
	s = s.replace(v,''.join(random.choice(string.ascii_uppercase) for _ in range(6)))
# 4. replace special characters with Javascript equivalents
s = re.sub(r'(function_[^{]+){',r'\1{dq=String.fromCharCode;',s);
s = s.replace('="',"'+dq(0x3d)+'\"").replace('"',"'+dq(0x22)+'").replace('<',"'+dq(60)+'")
s = s.replace('>',"'+dq(62)+'").replace('/',"'+dq(parseInt(57,8))+'").replace(' ',"'+dq(parseInt(40,8))+'")
s = s.replace(':',"'+dq(58)+'").replace('%',"'+dq(0x25)+'")
# 4b. and deal with hanging concatenations
s = s.replace("+''+","+").replace("=''+","=").replace("+'';",";").replace('_',' ')
# 5. obfuscate remaining strings with BreakingPoint (Ixia) technique
p = re.compile(r"'([^']+)'")
for m in re.finditer(p,s):
	s = s.replace(m.group(0),str(int(m.group(1),36))+'..toString(36)')
# 6. custom Base64 encoder and random sized chunks
b=encode(s[:-1])
c=chunk(b)
m=range(0,len(c))
r=list(zip(m,c))
random.shuffle(r)
# 7. build obfuscated array
j1='x=['
for i in r:
	j1+='"'+i[1]+'",'
j1=j1[:-1]+'];'
j2='z='
for i in sorted(r):
	j2+='x['+str(r.index(i))+']+'
j2=j2[:-1]+';'
# 8. build obfuscated javascript page
print '''<html><head>
<meta http-equiv="X-UA-Compatible" content="IE=10">
<meta charset="UTF-8">
</head>
<body><hl>boom boom</hl><script>'''
print j1
print j2
# 9. load Javascript decoder file
with open('step2.js') as f:
	s = f.read()
# 10. save required spaces, remove unnecessary formatting
s = s.replace('function ','function_').replace('var ','var_')
s = re.sub(r' ?([=+]) ?',r'\1',re.sub("[\t\n]","",s))
# 11. randomize function and variable names
fs=[]
vs=[]
p = re.compile(r'function_([0-9a-zA-Z]+)\(([^)]+)\)')
for m in re.finditer(p,s):
	fs.append(m.group(1))
	vs.append(m.group(2))
p = re.compile(r'var_([0-9a-zA-Z]+)[;=]')
for m in re.finditer(p,s):
	vs.append(m.group(1))
for f in fs:
	s = s.replace(f,''.join(random.choice(string.ascii_uppercase) for _ in range(6)))
for v in vs:
	s = s.replace(v,''.join(random.choice(string.ascii_uppercase) for _ in range(6)))
print s.replace('_',' ')
"""
print '''k="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/=";
function g(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9+/=]/g,"");while(f<e.length){s=k.indexOf(e.charAt(f++));o=k.indexOf(e.charAt(f++));u=k.indexOf(e.charAt(f++));a=k.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}return t;}
eval(g(z));
</script>
"""
print '''<h5>pop pop</h5></body></html>'''
