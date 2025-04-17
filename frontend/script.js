// frontend/script.js
const auth = firebase.auth();
const db = firebase.firestore();
const messagesRef = db.collection("messages");

// Monitor auth state
auth.onAuthStateChanged(user => {
  if (user) {
    document.getElementById('chat').style.display = 'block';
    loadMessages();
  } else {
    document.getElementById('chat').style.display = 'none';
  }
});

// Sign Up
function signUp() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  auth.createUserWithEmailAndPassword(email, password)
    .then(() => alert("Signed up!"))
    .catch(err => alert(err.message));
}

// Sign In
function signIn() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  auth.signInWithEmailAndPassword(email, password)
    .then(() => alert("Signed in!"))
    .catch(err => alert(err.message));
}

// Sign Out
function signOut() {
  auth.signOut();
}

// Send Message
function sendMessage() {
  const message = document.getElementById("messageInput").value;
  if (message.trim() !== "") {
    messagesRef.add({
      text: message,
      uid: auth.currentUser.uid,
      email: auth.currentUser.email,
      createdAt: firebase.firestore.FieldValue.serverTimestamp()
    });
    document.getElementById("messageInput").value = "";
  }
}

// Load messages in real-time
function loadMessages() {
  messagesRef.orderBy("createdAt")
    .onSnapshot(snapshot => {
      const messages = document.getElementById("messages");
      messages.innerHTML = "";
      snapshot.forEach(doc => {
        const data = doc.data();
        const msg = document.createElement("div");
        msg.textContent = `${data.email}: ${data.text}`;
        messages.appendChild(msg);
      });
    });
}
