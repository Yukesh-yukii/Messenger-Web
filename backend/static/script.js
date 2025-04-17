async function sendMessage() {
    const message = document.getElementById("message").value;

    if (!message) return alert("Please enter a message");

    const response = await fetch("http://127.0.0.1:5000/send-message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: message })
    });

    const data = await response.json();
    console.log(data);
    alert(data.message);
}
