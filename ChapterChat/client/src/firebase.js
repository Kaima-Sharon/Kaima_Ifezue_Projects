import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAUmPh7f-KEdbvIMdT4ego_yt5MOUUmqP4",
  authDomain: "chapterchat-498eb.firebaseapp.com",
  projectId: "chapterchat-498eb",
  storageBucket: "chapterchat-498eb.firebasestorage.app",
  messagingSenderId: "1005713428425",
  appId: "1:1005713428425:web:afdb5588523349de582218",
  measurementId: "G-SERH3M1Y8Z"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { auth };
export { db };
export default app;