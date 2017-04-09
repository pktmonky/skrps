k="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/="
decode(e){
	var t="";
	var n,r,i;
	var s,o,u,a;
	var f=0;
	e=e.replace(/[^A-Za-z0-9+/=]/g,"");
	while(f<e.length){
		s=k.indexOf(e.charAt(f++));
		o=k.indexOf(e.charAt(f++));
		u=k.indexOf(e.charAt(f++));
		a=k.indexOf(e.charAt(f++));
		n=s<<2|o>>4;
		r=(o&15)<<4|u>>2;
		i=(u&3)<<6|a;
		t=t+String.fromCharCode(n);
		if(u!=64){t=t+String.fromCharCode(r)}
		if(a!=64){t=t+String.fromCharCode(i)}
	}
	return t
}
