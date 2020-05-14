import * as React from 'react';
import { Image, Platform, StyleSheet, Text, TouchableOpacity, 
    View, Dimensions } from 'react-native';
import { ScrollView } from 'react-native-gesture-handler';
import {Button} from 'native-base';

const bg = require('../assets/images/dashboard-2.png');

const w = Dimensions.get('window').width;
const h = Dimensions.get('window').height;

export default function Home({navigation}) {
    return (
        <View style={styles.container}>
            <Image 
                source={bg} style={styles.bg}
            ></Image>
            <Text style={styles.heading}>Reminders made simple</Text>
            <Text style={styles.smallHeading}>
                You won't be 
            never ever missed your notification everytime and everywhere</Text>
            <Button full success 
                style={styles.btn} onPress={() => {navigation.push('Notification')}}>
                <Text style={{color: 'white'}}>Get Started</Text>
            </Button>
        </View>
    );
}

Home.navigationOptions = {
    header: null,
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 40,
    },
    bg: {
        // flex: 1,
        width: 219,
        height: 282,
        resizeMode: "cover",
        // justifyContent: "center"
    },
    heading: {
        fontFamily: 'rubik-medium',
        color: '#554E8F',
        fontSize: 22
    },
    smallHeading: {
        fontFamily: 'sans',
        color: '#82A0B7',
        fontSize: 17,
        padding: 15,
        textAlign: "center"
    },
    btn: {
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 1,
        },
        shadowOpacity: 0.30,
        shadowRadius: 1.41,
        marginTop: 10, 
        borderRadius: 15,
    }
    
});
