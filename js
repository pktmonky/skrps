function inject(name)
{
	object = '<table style="width:100%" id="' + name + '">';
	object = object + '<tr><th>When</th><th>What</th><th>Where</th></tr>';
	object = object + '<tr><th>Yesterday</th><th>Baseball</th><th>Downtown</th></tr>';
	object = object + '<tr><th>Tomorrow</th><th>Dodgeball</th><th>Uptown</th></tr>';
	object = object + '</table>';

	var div = document.createElement('div');
	div.innerHTML = object;
	document.body.appendChild(div);
}

inject('myTable');
