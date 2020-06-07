import React from 'react';
import { View, Text, ImageBackground, StyleSheet } from 'react-native';

export default function DetailNotification({ route, navigation }) {
    const { item } = route.params;
    
    return (
        <View style={styles.container}>
            <ImageBackground style={styles.imageStyle}
                source={{uri: item.image}}>

            </ImageBackground>
            <View style={styles.textContainer}>
                <Text style={styles.namePerson}>Person: {item.name}</Text>
                <Text>Time detected: {item.detectedAt}</Text>
                <Text>Visible time: {item.visibleTime}s</Text>
                {/* <Text>Stand with: {item.note} </Text> */}
            </View>
            
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center'
    },
    imageStyle: {
        width: 350,
        height: 350,
        // resizeMode: 'stretch',
    },
    textContainer: {

    },
    namePerson: {
        fontSize: 30,
        fontWeight: 'bold',
        fontFamily: 'rubik-regular',
    }
});