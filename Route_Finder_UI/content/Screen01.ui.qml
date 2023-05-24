/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick 6.5
import QtQuick.Controls 6.5
import Route_Finder_UI

Rectangle {
    width: 1280
    height: 720

    color: Constants.backgroundColor

    Button {
        id: button
        x: 594
        y: 557
        text: qsTr("Button")
        icon.color: "#3870a5"
        highlighted: false
        flat: false
    }

    TextInput {
        id: textInput
        x: 489
        y: 211
        width: 130
        height: 28
        text: qsTr("Text Input")
        font.pixelSize: 12
    }

    TextField {
        id: textField
        x: 594
        y: 209
        width: 107
        height: 33
        placeholderText: qsTr("Text Field")
    }

    RoundButton {
        id: roundButton
        x: 309
        y: 360
        text: "A"
        rotation: 13.182
    }

    RoundButton {
        id: roundButton1
        x: 813
        y: 334
        text: "B"
    }
}
