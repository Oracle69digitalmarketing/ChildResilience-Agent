import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

// Vite PWA registers SW automatically when using VitePWA.
// But we also add a message listener so the app can react to SW messages (sync success, failure).
if ("serviceWorker" in navigator) {
  // Wait for service worker to be ready and listen for messages from it
  navigator.serviceWorker.ready
    .then((registration) => {
      console.log("Service Worker ready:", registration);

      // Message handler from SW
      navigator.serviceWorker.addEventListener("message", (event) => {
        const payload = event.data;
        if (!payload) return;
        // Broadcast custom events to the app
        if (payload.type === "sync-success") {
          window.dispatchEvent(new CustomEvent("cr-sync-success", { detail: payload }));
        } else if (payload.type === "sync-failed") {
          window.dispatchEvent(new CustomEvent("cr-sync-failed", { detail: payload }));
        }
      });
    })
    .catch((err) => console.warn("SW ready error:", err));
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
