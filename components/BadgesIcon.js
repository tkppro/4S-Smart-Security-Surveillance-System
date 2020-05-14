import { Ionicons } from '@expo/vector-icons';
import * as React from 'react';
import {View, Text} from 'react-native'
import Colors from '../constants/Colors';

export default function BadgesIcon(props) {
    return (
      <View style={{ width: 24, height: 24, margin: 5 }}>
        <Ionicons name={props.name} size={30} color={props.focused ? Colors.tabIconSelected : Colors.tabIconDefault} />
        {props.badgeCount > 0 && (
          <View
            style={{
              // On React Native < 0.57 overflow outside of parent will not work on Android, see https://git.io/fhLJ8
              position: 'absolute',
              right: -6,
              top: -3,
              backgroundColor: 'red',
              borderRadius: 6,
              width: 13,
              height: 13,
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <Text style={{ color: 'white', fontSize: 10, fontWeight: 'bold' }}>
              {props.badgeCount}
            </Text>
          </View>
        )}
      </View>
    );
  }