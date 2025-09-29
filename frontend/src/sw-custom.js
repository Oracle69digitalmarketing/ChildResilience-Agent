// src/sw-custom.js
/* global self, fetch */
const QUEUE_DB = 'cr-agent-queue-v1';
const QUEUE_STORE = 'reports';

// Simple IndexedDB helper (promise-based)
function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(QUEUE_DB, 1);
    req.onupgradeneeded = () => {
      req.result.createObjectStore(QUEUE_STORE, { keyPath: 'id', autoIncrement: true });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function addToQueue(item) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(QUEUE_STORE, 'readwrite');
    const store = tx.objectStore(QUEUE_STORE);
    const req = store.add({ ...item, createdAt: new Date().toISOString() });
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function getAllQueue() {
  const db = await openDB();
  return new Promise((resolve) => {
    const tx = db.transaction(QUEUE_STORE, 'readonly');
    const store = tx.objectStore(QUEUE_STORE);
    const req = store.getAll();
    req.onsuccess = () => resolve(req.result || []);
    req.onerror = () => resolve([]);
  });
}

async function removeFromQueue(key) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(QUEUE_STORE, 'readwrite');
    const store = tx.objectStore(QUEUE_STORE);
    const req = store.delete(key);
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

// Intercept POSTs to /api/report and queue when offline or on failure
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (event.request.method === 'POST' && url.pathname.endsWith('/api/report')) {
    event.respondWith((async () => {
      try {
        // Try network first
        const resp = await fetch(event.request.clone());
        // If response not ok, queue for later
        if (!resp.ok) {
          const body = await event.request.clone().json().catch(() => null);
          await addToQueue({ url: event.request.url, body, headers: {} });
          // register sync
          self.registration.sync.register('cr-agent-sync').catch(() => {});
        }
        return resp;
      } catch (err) {
        // Offline: queue request body
        try {
          const body = await event.request.clone().json().catch(() => null);
          await addToQueue({ url: event.request.url, body, headers: {} });
          self.registration.sync.register('cr-agent-sync').catch(() => {});
        } catch (e) {
          // ignore
        }
        return new Response(JSON.stringify({ status: 'queued' }), { status: 202, headers: { 'Content-Type': 'application/json' }});
      }
    })());
  }
});

// Background sync handler - attempts to flush queue
self.addEventListener('sync', (event) => {
  if (event.tag === 'cr-agent-sync') {
    event.waitUntil((async () => {
      const queue = await getAllQueue();
      for (const item of queue) {
        try {
          // send as JSON POST
          const r = await fetch(item.url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item.body)
          });
          if (r.ok) {
            await removeFromQueue(item.id);
            // notify clients about success
            self.clients.matchAll().then(clients => {
              clients.forEach(c => c.postMessage({ type: 'sync-success', id: item.id }));
            });
          }
        } catch (err) {
          // leave in queue for next sync
          console.warn('Background sync attempt failed', err);
          break;
        }
      }
    })());
  }
});

// On activation claim clients
self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});
