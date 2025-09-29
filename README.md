# ChildResilience-Agent Frontend

ChildResilience-Agent is a Progressive Web App (PWA) designed to empower children, caregivers, and community responders in crisis situations. It provides real-time incident reporting, shelter discovery, and offline-ready dashboards that integrate directly with the backend resilience engine.

This frontend is built with React + Vite + TailwindCSS, and enhanced with PWA support for field deployment in low-connectivity regions.


---

## 🚀 Features

📱 Installable PWA — Works as a mobile app with offline support.

🏠 Shelter Map & Directory — Locate nearby shelters with capacity, type, and contact info.

🚨 Incident Reporting — Submit child protection, safety, or climate-related incidents.

🔔 Multi-channel Alerts — Integrates with backend for SMS, WhatsApp, and email notifications.

🌍 Multilingual Ready — Supports English by default with future i18n support.

🔒 JWT Auth Integration — Secure login and role-based access.

📊 Resilience Dashboard — Visualize incidents and response activity in real-time.



---

## 🏗️ Tech Stack

Framework: React (Vite)

Styling: TailwindCSS + shadcn/ui components

State Management: React Query

PWA Support: vite-plugin-pwa

Maps: Leaflet + OpenStreetMap

Notifications: Integrated with backend (SNS, Twilio, Email)

Auth: JWT from FastAPI backend



---

## 📂 Project Structure

frontend/
 ├── public/                # Static assets (PWA icons, manifest)
 ├── src/
 │   ├── api/               # Axios clients for backend APIs
 │   ├── components/        # Reusable UI components
 │   ├── features/
 │   │   ├── shelters/      # Shelter listing & map
 │   │   ├── incidents/     # Incident reporting UI
 │   │   └── auth/          # Login / Register flows
 │   ├── hooks/             # Custom React hooks
 │   ├── pages/             # App pages
 │   ├── App.jsx            # Main app entry
 │   └── main.jsx           # PWA registration + React root
 ├── vite.config.js         # Vite + PWA setup
 ├── tailwind.config.js     # Tailwind setup
 └── package.json           # Dependencies & scripts


---

## ⚡ Quick Start

1. Clone the repo

git clone https://github.com/your-org/childresilience-agent.git
cd childresilience-agent/frontend

2. Install dependencies

npm install

3. Run in development

npm run dev

App runs at: http://localhost:5173

4. Build for production

npm run build

5. Preview production build

npm run preview


---

## 📱 PWA Setup

Icons: Provided in public/icons (192x192, 512x512).

Manifest: Configured in vite.config.js.

Service Worker: Auto-registered with virtual:pwa-register.

Offline Support: Critical routes cached for low-connectivity use.



---

## 🔗 Backend Integration

The frontend connects to the FastAPI backend at:

http://localhost:8000/api

Available endpoints include:

/shelters — Fetch shelter directory

/incidents — Report or list incidents

/auth/login — User authentication



---

## 🚀 Deployment

AWS Amplify — Best for full-stack CI/CD with backend.

S3 + CloudFront — Global CDN with HTTPS.

Firebase Hosting — Optional alternative with analytics.



---

### 👥 Contributors

Built by the ChildResilience-Agent Team — advancing resilience, safety, and child protection through tech innovation.

