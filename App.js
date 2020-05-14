import * as React from 'react';
import { Platform, StatusBar, StyleSheet, View, Vibration } from 'react-native';
import { SplashScreen } from 'expo';
import * as Font from 'expo-font';
import { Ionicons } from '@expo/vector-icons';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Navigator from './navigation/StackNavigation';
import BottomTabNavigator from './navigation/BottomTabNavigator';
import useLinking from './navigation/useLinking';

import firebase from './src/firebase';
import * as Permissions from 'expo-permissions';
import { Notifications } from 'expo';
import Constants from 'expo-constants';

import {Container, Content, Header, Form, Input, Item, Button, Label} from 'native-base';

const Stack = createStackNavigator();

export default function App(props) {
    const [isLoadingComplete, setLoadingComplete] = React.useState(false);
    const [initialNavigationState, setInitialNavigationState] = React.useState();
    const containerRef = React.useRef();
    const { getInitialState } = useLinking(containerRef);
    const [isLoggedIn, setLoggedIn] = React.useState(false);

    const [data, setData] = React.useState({
        expoPushToken: '',
        notification: {},
    });

    _handleNotification = notification => {
        Vibration.vibrate();
        console.log(notification);
        setData({
            ...data,
            expoPushToken: '',
            notification: notification
        });
    };

    registerForPushNotificationsAsync = async (user) => {
        if (Constants.isDevice) {
            const { status: existingStatus } = await Permissions.getAsync(Permissions.NOTIFICATIONS);
            let finalStatus = existingStatus;
            if (existingStatus !== 'granted') {
                const { status } = await Permissions.askAsync(Permissions.NOTIFICATIONS);
                finalStatus = status;
            }
            if (finalStatus !== 'granted') {
                alert('Failed to get push token for push notification!');
                return;
            }
            token = await Notifications.getExpoPushTokenAsync();
            console.log(token);
            // this.setState({ expoPushToken: token });
            setData({
                ...data,
                expoPushToken: token,
                notification: ''
            });

            let updates = {expoToken: ''};
            updates.expoToken = token;
            firebase.database().ref('users').child(user.user.uid).update(updates);

        } else {
            alert('Must use physical device for Push Notifications');
        }

        if (Platform.OS === 'android') {
            Notifications.createChannelAndroidAsync('default', {
                name: 'default',
                sound: true,
                priority: 'max',
                vibrate: [0, 250, 250, 250],
            });
        }
    };
    // Load any resources or data that we need prior to rendering the app
    React.useEffect(() => {
        async function loadResourcesAndDataAsync() {
            try {
                SplashScreen.preventAutoHide();

                // Load our initial navigation state
                setInitialNavigationState(await getInitialState());

                // Load fonts
                await Font.loadAsync({
                    ...Ionicons.font,
                    'space-mono': require('./assets/fonts/SpaceMono-Regular.ttf'),
                    'rubik-regular': require('./assets/fonts/rubik/Rubik-Regular.ttf'),
                    'rubik-medium': require('./assets/fonts/rubik/Rubik-Medium.ttf'),
                    'sans': require('./assets/fonts/sans/OpenSans-Regular.ttf')
                });
            } catch (e) {
                // We might want to provide this error information to an error reporting service
                console.warn(e);
            } finally {
                setLoadingComplete(true);
                SplashScreen.hide();
            }
        }

        loadResourcesAndDataAsync();

        firebase.auth().signInWithEmailAndPassword('tkpproo@gmail.com', 'thang12345')
        .then((user) => {
            // console.log(user.user.uid)
            registerForPushNotificationsAsync(user);
        })
        // var that = this;
        // registerForPushNotificationsAsync();
        // this._notificationSubscription = Notifications.addListener(_handleNotification);

    }, []);

    if (!isLoadingComplete && !props.skipLoadingScreen) {
        return null;
    } else {
        if (isLoggedIn) {
            return (
                <View style={styles.container}>
                    <NavigationContainer>
                        <Stack.Navigator>
                            <Stack.Screen name="Root" component={Navigator} options={{ headerShown: false }} />
                        </Stack.Navigator>
                    </NavigationContainer>
                </View>
            );
        }
        else {
            return (
                <View style={styles.container}>
                    {Platform.OS === 'ios' && <StatusBar barStyle="default" />}
                    <NavigationContainer ref={containerRef} initialState={initialNavigationState}>
                        <Stack.Navigator>
                            <Stack.Screen name="Home" component={BottomTabNavigator} options={{ headerShown: false }} />
                            {/* </Stack.Navigator>
                        <Stack.Navigator> */}
                            <Stack.Screen name="Notification" component={Navigator} />
                        </Stack.Navigator>
                    </NavigationContainer>
                </View>
            );
        }
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
});
