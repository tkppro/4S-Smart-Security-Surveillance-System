import React, { useState } from 'react';
import { StyleSheet, Text, View, Button, Dimensions, FlatList, CheckBox, Image } from 'react-native';
import { RectButton, ScrollView, TouchableOpacity } from 'react-native-gesture-handler';
import Mock from '../components/Mock';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import firebase from '../src/firebase';

const width = Dimensions.get('window').width;
const height = Dimensions.get('window').height;

export default function NotificationScreen({ navigation }) {
    const isToday = (someDate) => {
        const today = new Date()
        return someDate.getDate() == today.getDate() &&
            someDate.getMonth() == today.getMonth() &&
            someDate.getFullYear() == today.getFullYear()
    };

    const [mockData, setMockData] = useState(Mock);
    
    const [resNotifications, setResNotifications] = useState();
    

    React.useEffect(() => {
        
        firebase.database().ref('/actions').on('value', data => {
            var newData = data.val()
            var arr = Object.entries(newData)
            setResNotifications(arr);
        })
        
        // const retrieveData = async () => {
        //     let ary = {};
        //     const eventref = firebase.database().ref("/actions").orderByKey();
        //     const snapshot = await eventref.on('value');
        //     const value = snapshot.val();
        //     ary = Object.entries(value);
        //     return ary;
        // }

    }, []);

    const filterToday = () => {
        // mockData.forEach((item) => moment(item.detectedAt).format('MMMM Do YYYY  h:mm:ss'));
        // var array = mockData.filter(item => isToday(new Date(item.detectedAt)));
        return resNotifications.filter(item => isToday(new Date(item.detectedAt))).length()
    };

    const sortNotifications = () => {
        
    };

    const generateRandomColor = () => {
        var arr = ['#FFD506', '#1ED102', '#D10263']
        var num = Math.round(Math.random() *3);
        // converting number to hex string to be read as RGB
        var hexString = arr[num];
        return hexString;
    };

    const NotificationTemplate = ({ item, style }) => {
        return (
            <View style={{ ...styles.singleNotification, borderLeftColor: style }}>
                <TouchableOpacity style={styles.touchableStyle} onPress={() => navigation.push('Notification',
                        {
                            screen: 'DetailNotification',
                            params: { item }
                        })}>
                    <Text style={styles.notiTime}>{item.detectedAt} {item.name} - standing</Text>
                    <Text></Text>
                </TouchableOpacity>
            </View>
        )
    };
    
    return (
        <ScrollView
            style={styles.container}
            contentContainerStyle={styles.contentContainer}>
            <LinearGradient
                colors={['#3867D5', '#81C7F5']}
                style={styles.headerBackground}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
            >
                <View style={styles.welcomeView}>
                    <Text style={{ ...styles.textWhite, ...styles.textRubikRegular, fontSize: 34 }}>Hello User!</Text>
                    <Text style={{ ...styles.textWhite, ...styles.textRubikRegular, fontSize: 15 }}>Today you have {filterToday} notifications</Text>
                </View>

                <View style={styles.remindBox}>
                    <View>
                        <Text style={styles.textWhite}>Today Reminder</Text>
                        <Text style={styles.textWhite}>Newest notification at 13:00 PM</Text>
                    </View>
                    <Image style={{ width: 50, height: 50 }} source={require('../assets/images/bell.png')}></Image>
                </View>

            </LinearGradient>
            <View style={styles.notifications}>
                <Text style={styles.smallTitle}>Today</Text>
                <View>
                    <FlatList
                        inverted
                        data={resNotifications}
                        renderItem={({ item }) => <NotificationTemplate style={generateRandomColor()} item={item[1]} />}
                        keyExtractor={item => item[0]}
                    >

                    </FlatList>
                </View>
            </View>
            {/* <View style={styles.notifications}>
                <Text style={styles.smallTitle}>Yesterday</Text>
                <View>
                    <FlatList
                        data={mockData}
                        renderItem={({ item }) => <NotificationTemplate style={generateRandomColor()} item={item} />}
                        keyExtractor={item => item.id.toString()}
                    >

                    </FlatList>
                </View>
            </View> */}
        </ScrollView>
    );
}

NotificationScreen.navigationOptions = {
    header: null,
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fafafa',
    },
    contentContainer: {
        // alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#F9FCFF'
    },

    headerBackground: {
        backgroundColor: '#81C7F5',
        height: 180,
        width: width,
        flex: 1,
        justifyContent: 'space-between',
        padding: 20,
        
    },
    remindBox: {
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
        // opacity: 0.5,
        padding: 15,
        borderRadius: 5,
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    welcomeView: {
        marginBottom: 20
    },
    textWhite: {
        color: 'white',
    },
    textRubikRegular: {
        fontFamily: 'rubik-regular',
    },
    singleNotification: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
        marginBottom: 10,
        marginTop: 10,
        height: 50,
        backgroundColor: '#fff',
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 1,
        },
        shadowOpacity: 0.20,
        shadowRadius: 1.41,
        paddingRight: 10,
        elevation: 2,
        borderRadius: 5,
        borderLeftWidth: 5,
        alignItems: 'center'
    },
    notifications: {
        padding: 18
    },
    notiTime: {
        fontFamily: 'rubik-medium',
        color: '#554E8F'
    },
    smallTitle: {
        fontFamily:'rubik-medium', 
        fontSize: 13, 
        color: '#8B87B3'
    },
    touchableStyle: {
        marginTop: 20,
    }
});
