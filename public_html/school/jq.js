document.addEventListener('DOMContentLoaded', ()=>
{
	function rate(argument) {
		// body...

		alert('ok')
	}
	{
		const request = new XMLHttpRequest();
		const rating = document.getElementsByName('stars')
		for (i=0; i< rating.length;i++){
				if (o[i].checked)
				{ 
					o[i].value
				}
		}


		request.open('POST', '/rate');

		request.onload =() =>{

			const data = request.responseText;
			document.querySelector('#rate') = data;
		}
	}
})