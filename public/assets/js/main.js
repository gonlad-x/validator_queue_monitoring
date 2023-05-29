checkDarkMode();
lastUpdateTime();

// Check if dark mode is set
function checkDarkMode() {
	// Use past setting if available
	let darkModeEnabled = localStorage.getItem("darkModeEnabled");
	if (darkModeEnabled === null) {
		// Default to user browser theme preference
		let matched = window.matchMedia("(prefers-color-scheme: dark)").matches;
		if (matched) {
			setDarkMode("true");
		} else {
			setDarkMode("false");
		}
	} else {
		setDarkMode(darkModeEnabled);
	}
}

// Toggle dark mode theme
function setDarkMode(enable) {
	document.getElementById("enableDarkMode").classList.add("d-none");
	document.getElementById("disableDarkMode").classList.add("d-none");
	var root = document.getElementsByTagName("html")[0];
	if (enable == "true") {
		// Enable dark mode
		root.setAttribute("data-bs-theme", "dark"); 
		root.classList.add("dark-mode");
		document.getElementById("disableDarkMode").classList.remove("d-none");
		localStorage.setItem("darkModeEnabled", "true");
	} else if (enable == "false") {
		// Disable dark mode
		root.setAttribute("data-bs-theme", "light"); 
		root.classList.remove("dark-mode");
		document.getElementById("enableDarkMode").classList.remove("d-none");
		localStorage.setItem("darkModeEnabled", "false");
	}
}

// Populate the last updated time
function lastUpdateTime() {
	let lastUpdated = document.getElementById("lastUpdated");
	let currentEpoch = Math.floor( Date.now() / 1000);
	let updateEpoch = lastUpdated.getAttribute('data-last-updated');
	let timeSinceUpdate = Math.floor( (currentEpoch - updateEpoch)/60 );
	let lastUpdatedText = "Last updated: ";
	if (timeSinceUpdate > 0) {
		if (timeSinceUpdate > 1) {
			lastUpdatedText += `${timeSinceUpdate} minutes ago`;
		} else {
			lastUpdatedText += `${timeSinceUpdate} minute ago`;
		}
	} else {
		let timeSinceUpdate = Math.floor(currentEpoch - updateEpoch);
		if (timeSinceUpdate > 1) {
			lastUpdatedText += `${timeSinceUpdate} seconds ago`;
		} else {
			lastUpdatedText += `${timeSinceUpdate} second ago`;
		}
	}
	lastUpdated.innerHTML = lastUpdatedText;
}
