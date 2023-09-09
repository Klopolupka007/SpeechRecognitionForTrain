RECORD_BUTTON_BASE = """
QPushButton {
    background-color: rgb(50,50,50);
    border-style: solid;
    border-width:1px;
    border-color: black;
    border-radius:50px;
    max-width:100px;
    max-height:100px;
    min-width:100px;
    min-height:100px;
    image: url(:/images/micro_light.png);
}
QPushButton:hover {
    background-color: rgb(30,30,30);
    border-width:2px;
}
QPushButton:pressed {
    background-color: rgb(10,10,10);
    border-width:3px;
}
"""


RECORD_BUTTON_RECORDING = """
QPushButton {
    background-color: rgb(50,50,50);
    border-style: solid;
    border-width:1px;
    border-color: red;
    border-radius:50px;
    max-width:100px;
    max-height:100px;
    min-width:100px;
    min-height:100px;
    image: url(:/images/stop_recording.png);
}
QPushButton:hover {
    background-color: rgb(30,30,30);
    border-width:2px;
}
QPushButton:pressed {
    background-color: rgb(10,10,10);
    border-width:3px;
}
"""