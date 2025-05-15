const videoFrame = document.getElementById("video-frame");
const statusDiv = document.getElementById("status");
const startButton = document.getElementById("start-button");
const stopButton = document.getElementById("stop-button");
const detectedClassesDiv = document.getElementById("detected-classes");
const classIdSelect = document.getElementById("class-id-select");
const setClassButton = document.getElementById("set-class-button");
const confidenceSlider = document.getElementById("confidence-slider");
const confidenceValue = document.getElementById("confidence-value");
const alertBox = document.getElementById("alert-box");

const websocketUrl = "ws://localhost:8000/ws/video_stream/";
let socket = null;
let currentClassIds = [];
let confidenceThreshold = 0.1; // Default confidence threshold
let isManualDisconnect = false; // Flag to prevent auto-reconnect when manually stopping

// Update confidence value display and send update to WebSocket
confidenceSlider.addEventListener("input", () => {
    confidenceValue.textContent = confidenceSlider.value;
    confidenceThreshold = parseFloat(confidenceSlider.value);
    sendWebSocketMessage({
        action: "set_confidence_threshold",
        confidence_threshold: confidenceThreshold,
    });
    console.log(`Confidence threshold set to ${confidenceThreshold}`);
});

// Update UI status
function updateStatus(connected) {
    if (connected) {
        statusDiv.innerHTML = '<i class="fas fa-check"></i>';
        statusDiv.className = "status-connected";
        startButton.disabled = true;
        stopButton.disabled = false;
    } else {
        statusDiv.innerHTML = '<i class="fas fa-times"></i>';
        statusDiv.className = "status-disconnected";
        startButton.disabled = false;
        stopButton.disabled = true;
    }
}

// Send messages through WebSocket if connected
function sendWebSocketMessage(message) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
    }
}

// Establish WebSocket connection
function connectWebSocket() {
    if (socket && socket.readyState === WebSocket.OPEN) {
        console.warn("WebSocket is already connected.");
        return;
    }

    isManualDisconnect = false; // Reset flag since the user is starting the stream
    socket = new WebSocket(websocketUrl);

    socket.onopen = () => {
        console.log("WebSocket connected");
        updateStatus(true);
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Update video frame
        if (data.frame) {
            requestAnimationFrame(() => {
                videoFrame.src = "data:image/jpeg;base64," + data.frame;
            });
        }

        // Update detected classes
        if (data.detected_classes) {
            detectedClassesDiv.textContent =
                "Detected Classes: " + data.detected_classes.join(", ");
        }

        // Show alert if received
    if (data.alert) {
        let alertMessage = data.alert;

        // Replace "Class ID 1" with "No Safety Vest"
        alertMessage = alertMessage.replace(/Class ID 1/g, "No Safety Vest");
        alertMessage = alertMessage.replace(/Class ID 3/g, "Safety Vest");
        alertMessage = alertMessage.replace(/Class ID 2/g, "No Helmet");
        alertMessage = alertMessage.replace(/Class ID 4/g, "Helmet");

        alertBox.innerHTML = `<p style="color: red; font-weight: bold;">${alertMessage}</p>`;
    }
};

    socket.onclose = () => {
        console.warn("WebSocket closed");

        updateStatus(false);

        // If the disconnection was NOT manual, attempt reconnection after 3 seconds
        if (!isManualDisconnect) {
            console.log("Attempting to reconnect...");
            setTimeout(connectWebSocket, 3000);
        }
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        socket.close();
    };
}

// Disconnect WebSocket
function disconnectWebSocket() {
    if (socket) {
        isManualDisconnect = true; // Set flag to prevent auto-reconnection
        socket.close();
        socket = null;
        updateStatus(false);
        videoFrame.src = "";
        detectedClassesDiv.textContent = "";
        alertBox.innerHTML = "";
        console.log("Streaming stopped manually.");
    }
}

// Set object classes to detect
function setClassesToDetect() {
    const selectedClassIds = Array.from(classIdSelect.selectedOptions).map((option) =>
        parseInt(option.value)
    );

    if (selectedClassIds.length > 0) {
        currentClassIds = selectedClassIds;
        sendWebSocketMessage({
            action: "set_class_ids",
            class_ids: currentClassIds,
        });
        console.log(`Class IDs ${selectedClassIds.join(", ")} set for detection.`);
    } else {
        alert("Please select at least one class.");
    }
}

// Attach event listeners
startButton.addEventListener("click", connectWebSocket);
stopButton.addEventListener("click", disconnectWebSocket);
setClassButton.addEventListener("click", setClassesToDetect);
