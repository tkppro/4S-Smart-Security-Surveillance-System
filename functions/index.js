const functions = require('firebase-functions');
var fetch = require('node-fetch')

const admin = require('firebase-admin');
admin.initializeApp();

//send the push notification 
exports.sendPushNotification = functions.database.ref('actions/{id}').onCreate((snap, context) => {
    const root = snap.val().name + " person detected at your house"
    var messages = []

    //return the main promise 
    return admin.database().ref('/users').once('value').then(function (snapshot) {
        snapshot.forEach(function (childSnapshot) {
            var expoToken = childSnapshot.val().expoToken;

            if(expoToken)
                messages.push({
                    "to": expoToken,
                    "sound": "default",
                    "title": "New detection!",
                    "badge": 1,
                    "body": root || "New Action Added"
                });
        });
        //firebase.database then() respved a single promise that resolves
        //once all the messages have been resolved 
        return Promise.all(messages)

    })
    .then(messages => {
        fetch('https://exp.host/--/api/v2/push/send', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(messages)

        });
    })
    .catch(reason => {
        console.log(reason)
    })


});