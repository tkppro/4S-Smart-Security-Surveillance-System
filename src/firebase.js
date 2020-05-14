import * as firebase from "firebase";

var firebaseConfig = {
    apiKey: "AIzaSyCSNfd7IOyqlDhnww_bNC9tIhDz7hODvW4",
    authDomain: "sproject-3697d.firebaseapp.com",
    databaseURL: "https://sproject-3697d.firebaseio.com",
    projectId: "sproject-3697d",
    storageBucket: "sproject-3697d.appspot.com",
    messagingSenderId: "864689882485",
    appId: "1:864689882485:web:7936b36e4b537d18a4bf3c"
};
// Initialize Firebase
export default !firebase.apps.length ? firebase.initializeApp(firebaseConfig) : firebase.app();