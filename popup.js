document.addEventListener('DOMContentLoaded', () => {
    // Add a single event listener to the parent <ul> element
    document.querySelector('ul').addEventListener('click', handleTaskClick);
    console.log("added")
});

async function handleTaskClick(event) {

	console.log("in handler");
	console.log(event);

	const tabs = await messenger.tabs.query({ active: true, currentWindow: true });
	const message = await messenger.messageDisplay.getDisplayedMessage(tabs[0].id);
	const full_msg = await messenger.messages.getRaw(message.id);

	await browser.runtime.sendMessage( {
 		"task": event.target.id,
 		"message": full_msg } )
}

