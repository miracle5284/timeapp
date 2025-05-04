let duration;
let intervalId;
let endTime;
let notification

// Handle messages from the main thread
self.onmessage = function(e) {
  if (e.data.type === 'start') {
    duration = e.data.duration;
    endTime = performance.now() + duration * 1000;
    tick();
  }
};

// Function to start the timer and send updates to the main thread
function tick() {
  intervalId = setInterval(() => {
    const now = performance.now();
    const remaining = Math.ceil((endTime - now) / 1000);
    duration = Math.max(0, remaining)
    self.postMessage({ remaining: duration });
    // Clear interval if time is up
    if (duration <= 0) {
      clearInterval(intervalId);
    }
  }, 1000);
}
