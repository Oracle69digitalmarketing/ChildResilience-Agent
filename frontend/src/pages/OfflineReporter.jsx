import React, { useEffect, useState } from "react";

/**
 * OfflineReporter
 * - Posts JSON to /api/report
 * - If network fails, response will be queued by service worker (src/sw-custom.js)
 * - Listens to sync success events from SW and shows UI feedback
 *
 * NOTE: This component uses JSON POST (not multipart). For file uploads you need
 * a file-blob queue; this example demonstrates the JSON flow expected by SW.
 */

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const OfflineReporter = () => {
  const [form, setForm] = useState({
    reporter_name: "",
    location: "",
    description: "",
    language: "en",
    childimpacttags: [],
    equity_flag: false,
    priority_score: 0,
    child_age_group: ""
  });

  const [status, setStatus] = useState("idle"); // idle | sending | queued | success | error
  const [queueCount, setQueueCount] = useState(0);

  // Update queue count from IndexedDB (same DB name as SW)
  const refreshQueueCount = async () => {
    if (!('indexedDB' in window)) return;
    try {
      const dbReq = indexedDB.open('cr-agent-queue-v1');
      dbReq.onsuccess = () => {
        const db = dbReq.result;
        const tx = db.transaction('reports', 'readonly');
        const store = tx.objectStore('reports');
        const countReq = store.count();
        countReq.onsuccess = () => setQueueCount(countReq.result || 0);
      };
    } catch (e) {
      // ignore
    }
  };

  useEffect(() => {
    refreshQueueCount();

    const onSyncSuccess = (e) => {
      setStatus("success");
      refreshQueueCount();
    };
    const onSyncFailed = (e) => {
      setStatus("error");
    };

    window.addEventListener("cr-sync-success", onSyncSuccess);
    window.addEventListener("cr-sync-failed", onSyncFailed);
    window.addEventListener("online", refreshQueueCount);
    window.addEventListener("offline", refreshQueueCount);

    return () => {
      window.removeEventListener("cr-sync-success", onSyncSuccess);
      window.removeEventListener("cr-sync-failed", onSyncFailed);
      window.removeEventListener("online", refreshQueueCount);
      window.removeEventListener("offline", refreshQueueCount);
    };
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const toggleTag = (tag) => {
    setForm(prev => {
      const tags = prev.childimpacttags.includes(tag) ? prev.childimpacttags.filter(t => t !== tag) : [...prev.childimpacttags, tag];
      return { ...prev, childimpacttags: tags };
    });
  };

  const postReport = async (payload) => {
    setStatus("sending");
    try {
      const resp = await fetch(`${API_URL}/api/report`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (resp.status === 202) {
        // queued by SW
        setStatus("queued");
      } else if (!resp.ok) {
        // server error
        const err = await resp.json().catch(() => ({ error: resp.statusText }));
        console.warn("Server response not ok:", err);
        setStatus("error");
      } else {
        setStatus("success");
      }
    } catch (err) {
      // network error => likely queued by SW or response from SW simulated 202
      console.warn("Network/Fetch error:", err);
      setStatus("queued");
    } finally {
      refreshQueueCount();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      reporter_name: form.reporter_name,
      location: form.location,
      description: form.description,
      language: form.language,
      childimpacttags: form.childimpacttags,
      equity_flag: form.equity_flag,
      priority_score: form.priority_score,
      child_age_group: form.child_age_group
    };

    await postReport(payload);
  };

  return (
    <div style={{ maxWidth: 640, margin: "0 auto", padding: 16 }}>
      <h3>Report Incident</h3>
      <form onSubmit={handleSubmit}>
        <label>
          Name
          <input name="reporter_name" onChange={handleChange} value={form.reporter_name} required />
        </label>

        <label>
          Location
          <input name="location" onChange={handleChange} value={form.location} required />
        </label>

        <label>
          Description
          <textarea name="description" onChange={handleChange} value={form.description} required />
        </label>

        <label>
          Language
          <select name="language" onChange={handleChange} value={form.language}>
            <option value="en">English</option>
            <option value="yo">Yoruba</option>
            <option value="ha">Hausa</option>
            <option value="ig">Igbo</option>
            <option value="sw">Swahili</option>
            <option value="hi">Hindi</option>
          </select>
        </label>

        <fieldset>
          <legend>Child Impact Tags</legend>
          {["schooldisruption", "healthrisk", "nutrition", "shelter"].map(tag => (
            <label key={tag} style={{ display: "block", margin: "6px 0" }}>
              <input type="checkbox" checked={form.childimpacttags.includes(tag)} onChange={() => toggleTag(tag)} />
              {tag}
            </label>
          ))}
        </fieldset>

        <label>
          Equity Flag
          <input type="checkbox" name="equity_flag" checked={form.equity_flag} onChange={handleChange} />
        </label>

        <label>
          Priority
          <input type="range" name="priority_score" min="0" max="5" value={form.priority_score} onChange={handleChange} />
        </label>

        <label>
          Child Age Group
          <select name="child_age_group" onChange={handleChange} value={form.child_age_group}>
            <option value="">Select</option>
            <option value="0-5">0–5</option>
            <option value="6-12">6–12</option>
            <option value="13-17">13–17</option>
          </select>
        </label>

        <div style={{ marginTop: 12 }}>
          <button type="submit" disabled={status === "sending"}>{status === "sending" ? "Sending..." : "Submit"}</button>
        </div>
      </form>

      <div style={{ marginTop: 16 }}>
        <strong>Network:</strong> {navigator.onLine ? "online" : "offline"} <br />
        <strong>Queue:</strong> {queueCount} pending report(s) <br />
        <strong>Status:</strong> {status}
      </div>
    </div>
  );
};

export default OfflineReporter;
