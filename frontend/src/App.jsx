import React, { useEffect, useState } from "react";

function App() {
  const [shelters, setShelters] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/shelters`)
      .then((res) => res.json())
      .then((data) => {
        setShelters(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch shelters:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-teal-700 mb-4">
        🏠 ChildResilience Agent
      </h1>

      {loading ? (
        <p>Loading shelters...</p>
      ) : (
        <ul className="space-y-3">
          {shelters.map((shelter) => (
            <li key={shelter.id} className="p-4 border rounded-lg shadow">
              <h2 className="font-semibold text-lg">{shelter.name}</h2>
              <p>📍 {shelter.lat}, {shelter.lng}</p>
              <p>Capacity: {shelter.capacity}</p>
              <p>Type: {shelter.type}</p>
              <p>☎️ {shelter.contact}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
