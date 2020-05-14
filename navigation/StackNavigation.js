import React from 'react'
import { createStackNavigator} from '@react-navigation/stack';
import Login from '../screens/Login';
import Register from '../screens/Register';
import NotificationScreen from '../screens/NotificationScreen';
import DetailNotification from '../screens/DetailNotification';

const Stack = createStackNavigator();
const INITIAL_ROUTE_NAME = 'Home';

export default function Navigator({ navigation, route }) {
    navigation.setOptions({ headerTitle: getHeaderTitle(route) });
    return (
        <Stack.Navigator initialRouteName={INITIAL_ROUTE_NAME} screenOptions={{
            headerShown: false
          }}>
            <Stack.Screen name="Login" component={Login}
                options={{ title: 'Sign in' }}
            />
            <Stack.Screen name="Register" component={Register}
                options={{ title: 'Sign up' }}
            />
            {/* <Stack.Screen name="NotificationScreen" component={NotificationScreen}
                options={{ title: 'Notifications' }}
            /> */}
            <Stack.Screen name="DetailNotification" component={DetailNotification}
                options={{ title: 'Detail Notification' }}
            />
        </Stack.Navigator>
    );
}

function getHeaderTitle(route) {
    const routeName = route.state?.routes[route.state.index]?.name ?? INITIAL_ROUTE_NAME;
  
    switch (routeName) {
        case 'Login':
            return 'Log in an account';
        case 'Register':
            return 'Create new account';
        // case 'NotificationScreen': 
        //     return 'Your notifications';
        case 'DetailNotification':
            return 'Detail';
    }
  }
  