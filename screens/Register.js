import React from 'react';
import { View, Text, StyleSheet, TextInput, Button, Image } from 'react-native'

const logoURI = '../assets/images/logo_transparent.png';

export default function Register({ navigation }) {
    return (
        <View style={styles.container}>
            <Image style={styles.logoStyle} source={require(logoURI)}/>
            <View>
                <TextInput 
                    style={styles.inputStyle} 
                    placeholder='username'></TextInput>
                <Button 
                    title="Sign up"
                ></Button>
            </View>
            <Button 
                title="Already have account? Sign in"
                onPress={() => navigation.navigate('Login')}
                ></Button>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'space-around',
        alignItems: 'center',
        margin: 10
    },
    inputStyle: {
        borderWidth: 1,
        borderColor: 'gray',
        width: 200,
        marginBottom: 30,
        height: 40
    },
    logoStyle: {
        width: 150,
        height: 150
    },
    signUpButton: {
        color: 'white'
    }
});

