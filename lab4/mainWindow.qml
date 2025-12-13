import QtQuick 2.0
import QtQuick.Window 2.3

import "."

Window {
    id: root
    visible: true
    width: 1000
    height: 1000
    title: "Paint!"

    Rectangle {
        id: tools
        width: parent.width
        height: 180
        color: "#545454"

        property color paintColor: "#33B5E5"
        property int thickness: 1
        property int spacing: 4

        Column {
            spacing: tools.spacing
            anchors.centerIn: parent
            width: parent.width * 0.8

            // Первая строка - цвета
            Row {
                spacing: tools.spacing
                anchors.horizontalCenter: parent.horizontalCenter

                Repeater {
                    model: ["#33B5E5", "#99CC00", "#FFBB33", "#FF4444"]
                    Square {
                        active: tools.paintColor === color
                        color: modelData
                        onClicked: tools.paintColor = color
                    }
                }
            }

            // Вторая строка - толщина
            Row {
                spacing: tools.spacing
                anchors.horizontalCenter: parent.horizontalCenter

                Repeater {
                    model: [1,2,3,4,5]

                    Circle {
                        id: circle
                        active: tools.thickness === thickness
                        thickness: modelData
                        text: thickness
                        onClicked: tools.thickness = thickness
                    }
                }
            }
            
            // Третья строка - кнопки управления (3 кнопки)
            Row {
                spacing: 40
                anchors.horizontalCenter: parent.horizontalCenter
                
                // Кнопка очистки
                Rectangle {
                    id: clearButton
                    width: 120
                    height: 40
                    color: clearMouseArea.pressed ? Qt.darker("#E0E0E0", 1.2) : 
                           clearMouseArea.containsMouse ? Qt.darker("#E0E0E0", 1.1) : "#E0E0E0"
                    radius: 20
                    
                    Text {
                        text: "🗑 Очистить"
                        color: "#333333"
                        anchors.centerIn: parent
                        font.pixelSize: 14
                        font.bold: true
                    }
                    
                    MouseArea {
                        id: clearMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        
                        onClicked: {
                            canvas.clearCanvas()
                            console.log("Canvas очищен")
                        }
                    }
                }
                
                // Кнопка сохранения
                Rectangle {
                    id: saveButton
                    width: 120
                    height: 40
                    color: saveMouseArea.pressed ? Qt.darker("#E0E0E0", 1.2) : 
                           saveMouseArea.containsMouse ? Qt.darker("#E0E0E0", 1.1) : "#E0E0E0"
                    radius: 20
                    
                    Text {
                        text: "💾 Сохранить"
                        color: "#333333"
                        anchors.centerIn: parent
                        font.pixelSize: 14
                        font.bold: true
                    }
                    
                    MouseArea {
                        id: saveMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        
                        onClicked: {
                            canvas.saveCanvas()
                            console.log("Изображение сохранено вручную")
                        }
                    }
                }
                
                // Кнопка автосохранения
                Rectangle {
                    id: autoSaveButton
                    width: 140
                    height: 40
                    color: autoSaveTimer.running ? 
                           (autoMouseArea.pressed ? Qt.darker("#4CAF50", 1.2) : 
                            autoMouseArea.containsMouse ? Qt.darker("#4CAF50", 1.1) : "#4CAF50") :
                           (autoMouseArea.pressed ? Qt.darker("#FF9800", 1.2) : 
                            autoMouseArea.containsMouse ? Qt.darker("#FF9800", 1.1) : "#FF9800")
                    radius: 20
                    
                    Text {
                        text: autoSaveTimer.running ? "⏸ Автосохр." : "▶ Автосохр."
                        color: "white"
                        anchors.centerIn: parent
                        font.pixelSize: 14
                        font.bold: true
                    }
                    
                    MouseArea {
                        id: autoMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        
                        onClicked: {
                            autoSaveTimer.running = !autoSaveTimer.running
                            console.log("Автосохранение: " + (autoSaveTimer.running ? "ВКЛ" : "ВЫКЛ"))
                        }
                    }
                }
            }
        }
    }

    Canvas {
        id: canvas
        anchors {
            left: parent.left
            right: parent.right
            top: tools.bottom
            bottom: parent.bottom
            margins: 8
        }

        property real lastX
        property real lastY
        property color color: tools.paintColor

        onPaint: {
            var ctx = getContext("2d")
            ctx.lineWidth = tools.thickness
            ctx.strokeStyle = canvas.color
            ctx.beginPath()
            ctx.moveTo(lastX, lastY)

            lastX = paint_area.mouseX
            lastY = paint_area.mouseY

            ctx.lineTo(lastX, lastY)
            ctx.stroke()
        }

        // Функция для сохранения изображения
        function saveCanvas() {
            // Получаем данные canvas в формате base64
            var imageData = canvas.toDataURL("image/png")
            // Убираем префикс "data:image/png;base64,"
            var base64Data = imageData.replace("data:image/png;base64,", "")
            // Отправляем в бэкенд
            _backend.saveCanvas(base64Data, "manual")
        }
        
        // Функция для очистки canvas
        function clearCanvas() {
            var ctx = getContext("2d")
            ctx.reset()
            canvas.requestPaint()
        }

        MouseArea {
            id: paint_area
            anchors.fill: parent

            onPressed: {
                canvas.lastX = mouseX
                canvas.lastY = mouseY
            }

            onPositionChanged: {
                canvas.requestPaint()
            }
        }
    }

    // Таймер для автоматического сохранения каждые 10 секунд
    Timer {
        id: autoSaveTimer
        interval: 10000
        running: true
        repeat: true
        onTriggered: {
            console.log("Автосохранение...")
            canvas.saveCanvas()
        }
    }
    
    // Статусная строка внизу
    Rectangle {
        id: statusBar
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        height: 30
        color: "#333333"
        
        Text {
            anchors {
                left: parent.left
                leftMargin: 10
                verticalCenter: parent.verticalCenter
            }
            color: "white"
            text: autoSaveTimer.running ? 
                  "Автосохранение включено (каждые 10 сек)" : 
                  "Автосохранение выключено"
        }
    }
}