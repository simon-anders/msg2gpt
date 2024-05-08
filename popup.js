document.addEventListener('DOMContentLoaded', () => {
    const menuOptions = document.querySelectorAll('.menu-option');

    menuOptions.forEach(option => {
        option.addEventListener('click', handleTaskClick);
    });
});

async function handleTaskClick(event) {
    const tabs = await messenger.tabs.query({ active: true, currentWindow: true });
    const message = await messenger.messageDisplay.getDisplayedMessage(tabs[0].id);
    const full_msg = await messenger.messages.getRaw(message.id);
    console.log("Requesting task '" + event.target.id + "' for message " + message.headerMessageId + ".");
    await browser.runtime.sendMessage({
        "task": event.target.id,
        "message": full_msg
    });
    window.close();
}
