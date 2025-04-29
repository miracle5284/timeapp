
---

# Timer System

Timer System is a Django-based countdown timer web application that empowers you to manage your time effectively. With features such as setting, pausing, and resetting the timer, the app ensures that your countdown remains accurate—even after page refreshes—by persisting state in Django sessions. For best performance, Timer System works in tandem with the Timer Keeper Active extension, a lightweight Chrome extension that prevents background throttling, ensuring your timer continues running even when your browser is in battery saver mode.

---

## Summary

Timer System delivers a seamless and reliable countdown experience. Modern browsers often slow down or pause background tabs to conserve power, which can cause timers to reset or lose accuracy. Timer System overcomes this challenge by using Django sessions for persistent timer state, while the Timer Keeper Active extension injects performance-enhancing scripts into your timer page. Together, they guarantee that your countdown remains uninterrupted and accurate, whether you’re a professional, student, or someone who values precise time management.

---

## Key Features

### Timer System Web App

- **Persistent Countdown:**  
  Your timer state (duration, start, and pause times) is stored in Django sessions, so the countdown remains accurate even after a page refresh.

- **Interactive Timer Controls:**  
  - **Start, Pause, and Reset:** Manage your timer effortlessly.  
  - **Editable Input:** Modify hours, minutes, and seconds directly using on-screen controls and +/– buttons.
  
- **Responsive Single-Page Application (SPA):**  
  Enjoy a smooth user experience across devices with a modern, dynamic interface.
  
- **Robust API Endpoints:**  
  Control the timer via RESTful endpoints:
  - **Set Timer:** `POST /timer/set_timer`
  - **Pause Timer:** `PUT /timer/pause_timer`
  - **Reset Timer:** `PUT /timer/reset_timer`
  
- **Production-Ready Deployment:**  
  Designed with error handling and security enhancements, Timer System can be deployed locally, via Docker, or on cloud platforms like Heroku.

### Timer Keeper Active Extension

- **Background Throttling Prevention:**  
  Ensures that your timer remains active and precise by preventing Chrome’s background throttling.
  
- **High Performance Mode:**  
  Uses advanced techniques to request increased processing priority for your timer page.
  
- **Wake Lock Integration:**  
  Optionally keeps your screen active, ensuring uninterrupted timer performance.
  
- **Seamless Integration:**  
  Automatically injects scripts into your timer website so that your countdown never stops—even when the browser is refreshed or closed.
  
- **User-Friendly Configuration:**  
  An intuitive options page lets you toggle features like high performance mode, wake lock, and DoNot Disturb mode with ease.

**For optimal performance, we highly recommend installing Timer Keeper Active.**  
- **GitHub Repository:** [Timer Keeper Active on GitHub](https://github.com/miracle5284/timer-keeper-extension)  
- **Chrome Web Store:** [Timer Keeper Active – Chrome Web Store](https://chromewebstore.google.com/detail/jndhblddppbjacboankdagkmbnnmpbdf)

---

## Technologies Used

### Timer System Web App

- **Django:** Handles timer logic and session management.
- **JavaScript (ES6):** Drives dynamic UI interactions.
- **Axios:** Facilitates API calls for timer operations.
- **HTML/CSS & Bootstrap (Optional):** Provide a modern, responsive interface.
- **SQLite:** Serves as the development database.
- **Docker:** Enable containerized and cloud deployments.

### Timer Keeper Active Extension

- **Manifest v3:** Implements the latest security and performance standards.
- **Chrome Scripting API:** Dynamically injects performance-enhancing code.
- **Chrome Storage & Cookies:** Store user settings and integration signals.
- **Chrome Idle API:** Reapplies performance settings based on system state.

### The Active App is available at:
**Production Website**: https://timer.blueprime.app
**Beta Version**: https://staging-timer-app-slim.azurewebsites.net
---

## Getting Started

### Timer System Web App

1. **Clone the Repository:**
   ```bash
   git clone "https://github.com/miracle5284/timeapp.git">
   cd timer_system_app
   ```

2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run Migrations & Start the Server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Open your browser and visit `http://127.0.0.1:8000/timer/` to use the timer.

4. **Deployment Options:**
   Deploy using Docker or Heroku by following the instructions in the repository.

### Timer Keeper Active Extension

1. **Load the Extension Locally:**
   - Open Chrome and navigate to `chrome://extensions`.
   - Enable “Developer mode” and click “Load unpacked.”
   - Select the `timer-keeper` folder.

2. **Configure Settings:**
   Access the options page through the extension icon to customize features like high performance mode, wake lock, and Do Not Disturb.

3. **Automatic Integration:**
   The extension automatically injects its code into your timer website, ensuring that your countdown remains active even when the browser is in battery saver mode.

4. **Additional Resources:**
   - **GitHub Repository:** [Timer Keeper Active on GitHub](https://github.com/miracle5284/timer-keeper-extension)
   - **Chrome Web Store:** [Timer Keeper Active – Chrome Web Store](https://chromewebstore.google.com/detail/jndhblddppbjacboankdagkmbnnmpbdf)

---

## Conclusion

Timer System and Timer Keeper Active work together to deliver a robust and reliable countdown timer experience. Timer System ensures that your timer’s state is preserved and managed efficiently, while Timer Keeper Active guarantees that your timer remains active and immune to background throttling. This integrated solution is ideal for professionals, students, and everyday users who depend on accurate, uninterrupted timing.

**Download Timer Keeper Active today from the Chrome Web Store and experience uninterrupted, accurate timing—every minute counts!**

---