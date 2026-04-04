import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyC4vM-gZORxtdOJ5oNgzfw-UGv-mfGgBLQ",
  authDomain: "anthropos-ai-c7d76.firebaseapp.com",
  projectId: "anthropos-ai-c7d76",
  storageBucket: "anthropos-ai-c7d76.firebasestorage.app",
  messagingSenderId: "9407132672",
  appId: "1:9407132672:web:c872d3b5f91208faf294e5"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

window.signInWithGoogle = async function () {
  try {
    const result = await signInWithPopup(auth, provider);
    window.location.href = "/checkout.html";
  } catch (error) {
    console.error("Google sign-in error:", error);
    alert(error.message);
  }
};
