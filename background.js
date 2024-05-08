browser.runtime.onMessage.addListener((message) => {
	let port = browser.runtime.connectNative( "process_message.pipe_message" );

    port.onDisconnect.addListener(() => {
        if (port.error) {
            console.error("pipe_message: Failed to connect to Python script:", port.error.message);
        }
    });

	port.postMessage( message );
});
