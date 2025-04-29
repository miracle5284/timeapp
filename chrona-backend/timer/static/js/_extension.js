let timeout, interval, observer;
let notificationFired = false;
let extensionPromptDiv, dataContainerDiv;
let extensionId, markedDataContainerInactive = false;
let extensionInitialized = false;

// Constants for DOM elements and extension settings
const extensionTrackerAttr = "data-timer-extension";
const extensionHandshakeInterval = 10000;
const extensionName = "Timer Keeper Active";
const extensionInstallBtnId = "installLink";
const extensionEnableBtnId = "enableLink";
const extensionPromptId = "extensionPrompt";
const dataContainerId = "data-container";
const CHROME_EXTENSION_PREFIX_URL = "https://chromewebstore.google.com/detail"


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
/**
 * Checks if the Timer Keeper extension is installed by inspecting cookies.
 * Updates UI elements accordingly.
 */
function checkForExtension() {
  try {
    const extensionEnableBtn = document.getElementById(extensionEnableBtnId);
    const extensionInstallBtn = document.getElementById(extensionInstallBtnId);
    const extensionPrompt = document.getElementById(extensionPromptId);
    const extensionData = document.cookie
      .split(";")
      .map(row => row.trim())
      .find(row => row.startsWith("timer-keeper="));

    if (extensionData) {
      const extensionDetails = JSON.parse(extensionData.split("=")[1]);

      if (extensionDetails.installed) {
        extensionInitialized = true;
        extensionId = extensionDetails.extensionId;
        extensionInstallBtn.style.display = "none";
        extensionEnableBtn.style.display = "inline";
        extensionEnableBtn.addEventListener("click", showExtensionWarning);
      }
    } else {
      extensionPrompt.style.display = "block";
      extensionInstallBtn.style.display = "inline";
      extensionEnableBtn.style.display = "none";
      extensionInstallBtn.addEventListener("click", () => {
        window.location.href = `${CHROME_EXTENSION_PREFIX_URL}/${dataContainerDiv.getAttribute("data-extension-id")}`;
      });
    }
  } catch (error) {
    console.error("Error checking for extension:", error);
  }
}

// Initialize extension detection when the page loads
window.addEventListener("load", () => {
  extensionPromptDiv = document.getElementById(extensionPromptId);
  dataContainerDiv = document.getElementById(dataContainerId);
  extensionPromptDiv.style.display = "none";
  observer = getExtensionObserver();
  startExtensionHandshake();
});

/**
 * Handles the Timer Keeper extension status change event.
 * Updates UI and notifies the user if the extension is inactive.
 */
document.addEventListener("onTimerKeeperExtensionEvent", (event) => {
  if (event.detail.active) {
    extensionPromptDiv.style.display = "none";
    stopExtensionObserve();
    notificationFired = false;
    markedDataContainerInactive = false;
  } else {
    extensionPromptDiv.style.display = "block";
    if (!notificationFired && Notification.permission === "granted" && document.visibilityState !== "visible") {
      new Notification("Timer Keeper is inactive", {
        body: "Please enable the Timer Keeper extension for optimum results.",
        icon: "/static/imgs/clock-circle-svgrepo-com.svg",
        requireInteraction: true,
      });
      notificationFired = true;
    }
    if (dataContainerDiv && !markedDataContainerInactive) {
      dataContainerDiv.setAttribute(extensionTrackerAttr, "inactive");
      markedDataContainerInactive = true;
    }
    clearInterval(interval);
    interval = null;
    resumeExtensionObserve();
  }
});

/**
 * Sends a handshake message to the extension to confirm its active status.
 */
function checkExtensionHandshake() {

  if (chrome.runtime) {
    chrome.runtime.sendMessage(extensionId, { type: "PING_FROM_PAGE" }, (response) => {
      if (!chrome.runtime.lastError && response?.type === "PONG_FROM_EXTENSION") {
        document.dispatchEvent(new CustomEvent("onTimerKeeperExtensionEvent", { detail: { active: true } }));
      } else {
        document.dispatchEvent(new CustomEvent("onTimerKeeperExtensionEvent", { detail: { active: false } }));
      }
    });
  } else {
    document.dispatchEvent(new CustomEvent("onTimerKeeperExtensionEvent", { detail: { active: false } }));
  }
}

/**
 * Starts the handshake process with the extension, ensuring it remains active.
 */
function startExtensionHandshake() {
  if (!extensionInitialized)
    setTimeout(() => {
        checkForExtension();
        checkExtensionHandshake();
    }, 300);
  else checkExtensionHandshake();
  interval = setInterval(checkExtensionHandshake, extensionHandshakeInterval);
}

/**
 * Observes changes in the extension tracker attribute and triggers a handshake.
 */
function getExtensionObserver() {
  return new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.type === "attributes" && mutation.attributeName === extensionTrackerAttr) {
        if (mutation.target.getAttribute(extensionTrackerAttr) === "active") {
          startExtensionHandshake();
        }
      }
    }
  });
}

/**
 * Resumes observing the extension activity by monitoring attribute changes.
 */
function resumeExtensionObserve() {
  if (observer && dataContainerDiv) {
    observer.observe(dataContainerDiv, { attributes: true, attributeFilter: [extensionTrackerAttr] });
  }
}

/**
 * Stops observing the extension activity to prevent redundant monitoring.
 */
function stopExtensionObserve() {
  if (observer) observer.disconnect();
}

/**
 * Displays a modal warning when the extension is not detected.
 */
function showExtensionWarning() {
  let instructionModal = document.getElementById("instruction-modal");
  if (!instructionModal) {
    instructionModal = document.createElement("div");
    instructionModal.id = "instruction-modal";
    instructionModal.style.display = "flex";
    instructionModal.innerHTML = `
      <div class="modal-content">
        <h2>Extension Not Detected ⚠️</h2>
        <p>Enable the Timer Keeper Active extension for the best performance.</p>
        <p><strong>Without the extension:</strong> Background timers may be throttled, affecting accuracy.</p>
        <ol>
          <li>Open <code>chrome://extensions</code> in Chrome.</li>
          <li>Find <strong>Timer Keeper Active</strong>.</li>
          <li>Enable the extension.</li>
        </ol>
        <p><a href="https://github.com/miracle5284/timer-keeper-extension" target="_blank">Need Help?</a></p>
        <button onclick="document.getElementById('instruction-modal').style.display='none'">Close</button>
      </div>
    `;
    document.body.appendChild(instructionModal);
  }
  instructionModal.style.display = "block";
}
