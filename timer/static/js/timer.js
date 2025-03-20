let active = false;
let countdownWorker = null;
let hourEl = null;
let minuteEl = null;
let secondEl = null;

let valueChanged = false;
let controlBtn = null;
let resetBtn = null;
let initialDuration = null;
let duration = null;
let timerRunning = false;
let timeUpWrapper = null;
let csrfToken = null;
let notificationPermission = false;
const timeUpSound = new Audio(AUDIO_URL);

// Initialize variables and setup event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Request notification permission
  if ('Notification' in window) {
    Notification.requestPermission().then(function(permission) {
      notificationPermission = permission === 'granted';
    });
  }

  hourEl = document.getElementById('hours-display');
  minuteEl = document.getElementById('minutes-display');
  secondEl = document.getElementById('seconds-display');

  const dataContainer = document.getElementById('data-container');
  initialDuration = parseInt(dataContainer.getAttribute('data-initial'));
  timerRunning = dataContainer.getAttribute('data-active') === 'True';
  timeUpWrapper = document.getElementById('time-up-wrap');

  csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0]?.value;

  controlBtn = document.getElementById('control');
  resetBtn = document.getElementById('reset');

  duration = calculateDuration();
  addValidators();
  updateDisplay();

  // Set the active state and disable fields if the timer is running
  if (timerRunning) {
    active = true;
    toggleFieldStates(true); // Disable fields on reload if timer is running
    startTimer(duration);
  } else if (!duration && initialDuration) {
    timeUpWrapper.textContent = 'Time Up!!!';
  }
});


// Calculate the total duration in seconds
function calculateDuration() {
  const hour = parseInt(hourEl.textContent) || 0;
  const minute = parseInt(minuteEl.textContent) || 0;
  const second = parseInt(secondEl.textContent) || 0;
  duration = hour * 3600 + minute * 60 + second;
  return duration;
}

// Update the timer display based on duration
function updateDisplay(notifyChange = false) {
  timeUpWrapper.textContent = '';
  setTimeout(() => {
    duration = calculateDuration();
    renderTimer(duration);
    controlBtn.disabled = !duration;
    updateButtonStates();
    if (notifyChange) {
      valueChanged = true;
    }
  }, 0);
}

// Start or pause the timer
function toggleTimer() {
  if (active) {
    axios.put('/pause_timer', { duration }, getHeaders())
      .then(() => {
        if (countdownWorker) {
          countdownWorker.terminate();
          countdownWorker = null;
        }
        updateControlButtonText('Start');
        active = false; // Update the active state
        toggleFieldStates(false); // Re-enable editing and buttons
      });
    return;
  }

  calculateDuration();
  if (valueChanged) {
    initialDuration = duration;
    valueChanged = false;
  }
  axios.post('/set_timer', { duration, initialDuration }, getHeaders())
    .then(() => {
      startTimer(duration);
      active = true; // Update the active state
      toggleFieldStates(true); // Disable editing and buttons
    });
}

// Start countdown timer
function startTimer(duration) {
  renderTimer(duration);
  active = true;
  updateControlButtonText('Pause');
  timeUpWrapper.textContent = '';

  // Create a new worker from timerWorker.js
  countdownWorker = new Worker('/static/js/timerWorker.js');
  countdownWorker.postMessage({
    type: 'start',
    duration: duration,
  });
  resetBtn.disabled = false;

  countdownWorker.onmessage = function(event) {
    const remaining = event.data.remaining;
    if (remaining <= 0) {
      countdownWorker.terminate();
      countdownWorker = null;
      timeUpWrapper.textContent = 'Time Up!!!';
      calculateDuration();
      active = false;
      toggleFieldStates(false); // Re-enable editing and buttons
      updateControlButtonText('Start');
      updateButtonStates();
      playAlarm();
      sendNotification();
    }
    renderTimer(remaining);
  };
}

// Reset timer to the initial state
function resetTimer() {
  axios.put('/reset_timer', {}, getHeaders())
    .then(() => {
      if (countdownWorker) {
        countdownWorker.terminate();
        countdownWorker = null;
      }
      duration = initialDuration;
      renderTimer(duration);
      active = false;
      toggleFieldStates(false); // Re-enable editing and buttons
      updateButtonStates();
      updateControlButtonText('Start');
    });
}

// Render the timer display
function renderTimer(duration) {
  const hours = Math.floor(duration / 3600);
  const minutes = Math.floor((duration % 3600) / 60);
  const seconds = duration % 60;

  hourEl.textContent = String(hours).padStart(2, '0');
  minuteEl.textContent = String(minutes).padStart(2, '0');
  secondEl.textContent = String(seconds).padStart(2, '0');

    controlBtn.disabled = duration <= 0;
    resetBtn.disabled =  !(!!initialDuration);
}

// Adjust time by incrementing or decrementing
function adjustTime(elId, increment) {
  const el = document.getElementById(elId);
  let value = parseInt(el.textContent) || 0;

  value = Math.max(0, value + increment);
  el.textContent = String(value).padStart(2, '0');

  validateRange(el);
  updateDisplay(true);
}

// Validate user input range and reset invalid values
function validateRange(el) {
  const value = parseInt(el.textContent, 10);

  if (el.id !== 'hours-display' && (isNaN(value) || value < 0 || value > 59)) {
    showPopover(el, `${el.id.includes('minutes') ? 'Minutes' : 'Seconds'} must be between 0 and 59`);
    el.textContent = '00';
  }
}

// Add validation to editable fields
function addValidators() {
  const editableSpans = document.querySelectorAll('.display');

  editableSpans.forEach((el) => {

    el.addEventListener('keypress', (event) => {

      if (isNaN(event.key)) {
        event.preventDefault();
        showPopover(el, 'Only numbers are allowed!');
      } else if (el.textContent === '00') {
        event.preventDefault();
        let position = getCursorPosition();
        el.textContent = event.key.padEnd(3 - position, '0')
        setCursorPosition(el,1)
      }
    });

    el.addEventListener('blur', () => {
      validateRange(el);
      updateDisplay(true);
    });
  });
}

// Enable or disable editing and buttons based on the active state
function toggleFieldStates(disable) {
  // Disable or enable the time displays
  document.querySelectorAll('.display').forEach((el) => {
    el.contentEditable = !disable;
  });

  // Disable or enable the plus and minus buttons
  document.querySelectorAll('.btn-icon').forEach((btn) => {
    btn.disabled = disable;
  });

  // Ensure the control button remains clickable
  controlBtn.disabled = false;
}

// Update button states based on the display value
function updateButtonStates() {
  const els = [hourEl, minuteEl, secondEl];

  els.forEach((el, idx) => {
    const value = parseInt(el.textContent);
    const previousSiblings = el.previousElementSibling;
    const minusBtn = previousSiblings.querySelector('button:last-of-type');
    const plusBtn = previousSiblings.querySelector('button:first-of-type');

    if (value >= 59 && idx !== 0) {
      plusBtn.disabled = true;
      minusBtn.disabled = false;
    } else if (value <= 0) {
      minusBtn.disabled = true;
      plusBtn.disabled = false;
    } else {
      minusBtn.disabled = false;
      plusBtn.disabled = false;
    }
  });
}

// Show popover for validation messages
function showPopover(el, message) {
  const popover = document.createElement('div');
  popover.className = 'custom-popover';
  popover.textContent = message;

  el.parentElement.appendChild(popover);
  setTimeout(() => popover.remove(), 3000);
}

// Get API headers
function getHeaders() {
  return {
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
  };
}

// Manipulating windows cursor position
function getCursorPosition() {
  const selection = window.getSelection();
  return selection.anchorOffset;
}

function setCursorPosition(el, index) {
  const selection = window.getSelection();
  const range = document.createRange();

  let node = el.firstChild; // Get the text node
  if (!node) return; // Prevent errors if the element is empty

  let length = node.length;
  if (index > length) index = length; // Avoid out-of-bounds errors

  range.setStart(node, index);
  range.collapse(true); // Collapse to ensure a single caret position

  selection.removeAllRanges();
  selection.addRange(range);
}


// Helper function to fade out/in the control button text
function updateControlButtonText(newText) {
  const controlText = document.getElementById("control-text");
  if (!controlText) {
    // Fallback if span is missing
    controlBtn.textContent = newText;
    return;
  }
  controlText.classList.remove("fade-in");
  controlText.classList.add("fade-out");
  setTimeout(() => {
    controlText.textContent = newText;
    controlText.classList.remove("fade-out");
    controlText.classList.add("fade-in");
  }, 500); // Match the CSS transition duration
}

function playAlarm() {
  timeUpSound.play().catch(error => {
    console.error('Error playing audio:', error);
  });
}

function sendNotification () {
  if (notificationPermission) {
    try {
      new Notification('Timer Complete!', {
        body: `Your timer of ${initialDuration} seconds has finished!`,
        icon: '/static/imgs/clock-circle-svgrepo-com.svg',
        requireInteraction: true  // Make notification persist until user interaction
      });
    } catch (e) {
      console.warn('Notification failed:', e);
    }
  }

  // Vibrate if supported
  if ('vibrate' in navigator) {
    navigator.vibrate([200, 100, 200]);
  }
}