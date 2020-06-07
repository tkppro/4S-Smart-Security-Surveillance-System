import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native'
import {Container, Content, Header, Form, Input, Item, Button, Label} from 'native-base';

import firebase from '../src/firebase';

const logoURI = '../assets/images/logo_transparent.png';

export default function Login({ navigation }) {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const login = () => {
        try {
            firebase.auth().signInWithEmailAndPassword(email, password).then(function(user) {
                navigation.navigate('Home')
            })
        } catch (error) {
            console.log(error.toString())
        }
        
    };

    const register = () => {
        try {
            if(email < 6) {
                alert('Input again');
                return;
            }
            
            firebase.auth().createUserWithEmailAndPassword(email, password)
            .then((result) => {
                console.log(result)
                firebase.database().ref('/users/' + result.user.uid)
                .set({
                    email: result.user.email,
                    created_at: Date.now()
                })
            });
        } catch (error) {
            console.log(error.toString())
        }

        
    };

    return (
        <Container style={styles.container}>
            <View style={styles.viewImg}>
                <Image style={styles.logoStyle} source={require(logoURI)}/>
            </View>
            <Form>
                    <Item floatingLabel>
                        <Label>Email</Label>
                        <Input autoCorrect={false}
                            autoCapitalize="none"
                            onChangeText={(text) => setEmail(text)}
                        ></Input>
                    </Item>

                    <Item floatingLabel>
                        <Label>Password</Label>
                        <Input autoCorrect={false}
                            autoCapitalize="none"
                            secureTextEntry={true}
                            onChangeText={(text) => setPassword(text)}
                        ></Input>
                    </Item>
                    <Button full rounded success style={{marginTop: 10}} onPress={login}>
                        <Text style={{color: 'white'}}>Login</Text>
                    </Button>
                    <Button full rounded primary style={{marginTop: 10}} onPress={register}>
                        <Text style={{color: 'white'}}>Sign Up</Text>
                    </Button>
                </Form>
        </Container>
    )
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        margin: 10
    },
    logoStyle: {
        width: 150,
        height: 150
    },
    viewImg: {
        justifyContent: 'center',
        alignItems: 'center'
    }
    
});

