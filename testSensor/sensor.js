function getRand(min, max, dp) {
  const factor = Math.pow(10, dp);
  const random = Math.random() * (max - min) + min;
  return Math.round(random * factor) / factor;
}

function sendUpdate() {
  const data = {
    name: "sensor1",
    value: `${getRand(22.01, 23.01, 2)}`,
    time: new Date().toLocaleTimeString("en-GB", { hour12: false }),
  };

  console.log(`sending: ${JSON.stringify(data)} `);

  fetch("http://localhost:8000/update", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Send update every 5 seconds
setInterval(sendUpdate, 5000);

// Send first update immediately
sendUpdate();
