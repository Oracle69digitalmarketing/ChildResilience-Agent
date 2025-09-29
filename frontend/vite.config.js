import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
import path from "path";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      injectRegister: "auto",
      registerType: "prompt",
      strategies: "injectManifest",
      srcDir: "src",
      filename: "sw-custom.js", // this will be injected
      manifest: {
        name: "ChildResilience Agent",
        short_name: "ChildResilience",
        start_url: "/",
        display: "standalone",
        background_color: "#ffffff",
        theme_color: "#2b7a78",
        icons: [
          { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png" }
        ]
      },
      workbox: {
        // precache config & runtime caching rules
        globPatterns: ["**/*.{js,css,html,ico,png,svg}"],
        runtimeCaching: [
          {
            // API requests (NetworkFirst so newest data preferred)
            urlPattern: new RegExp(`${process.env.REACT_APP_API_URL || "http://localhost:8000"}`),
            handler: "NetworkFirst",
            options: {
              cacheName: "api-cache",
              expiration: { maxEntries: 200, maxAgeSeconds: 60 * 60 * 24 } // 1 day
            }
          },
          {
            // Map tiles (cache first)
            urlPattern: /^https:\/\/(tile|a|b|c)\.tile\.openstreetmap\.org\//,
            handler: "CacheFirst",
            options: {
              cacheName: "osm-tiles",
              expiration: { maxEntries: 500, maxAgeSeconds: 60 * 60 * 24 * 7 } // 7 days
            }
          },
          {
            // icons
            urlPattern: /\/icons\//,
            handler: "CacheFirst",
            options: {
              cacheName: "icons-cache",
              expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 24 * 30 } // 30 days
            }
          }
        ]
      },
      // Ensure injectManifest reads our custom service worker
      injectManifest: {
        swSrc: path.resolve(__dirname, "src/sw-custom.js"),
      },
    })
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src")
    }
  }
});
