browser.runtime.onMessage.addListener((message) => {
	console.log( "9" );
	console.log( message );
	
	let port = browser.runtime.connectNative( "process_message.simon_anders" );
	port.postMessage( message );
});
