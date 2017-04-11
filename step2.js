var key="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/="
function decode(input){
	var out="";
	var enc1;
	var enc2;
	var enc3;
	var char1;
	var char2;
	var char3;
	var char4;
	var index=0;
	input=input.replace(/[^A-Za-z0-9+/=]/g,"");
	while(index<input.length){
		char1=key.indexOf(input.charAt(index++));
		char2=key.indexOf(input.charAt(index++));
		char3=key.indexOf(input.charAt(index++));
		char4=key.indexOf(input.charAt(index++));
		enc1=char1<<2|char2>>4;
		enc2=(char2&15)<<4|char3>>2;
		enc3=(char3&3)<<6|char4;
		out=out+String.fromCharCode(enc1);
		if(enc2!=64){out=outt+String.fromCharCode(enc2)}
		if(enc3!=64){out=out+String.fromCharCode(enc3)}
	}
	return out
}
