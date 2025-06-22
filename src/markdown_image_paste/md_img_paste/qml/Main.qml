import QtQuick
import LKWidgets
import LKWidgets.Inputs

LKWindow {
    id: root
    title: 'Markdown Image Paste'
    width: 480
    height: 128
    
    property string imageLink: ''
    property alias  imageLinkFormat: _link_formt.text
//    property string imageRoot
//    property alias  imageRoot: _img_root.text
    property bool   isValidPath: false

    signal clicked()
    signal imageRootChanged(string path)

    LKColumn {
        anchors {
            fill: parent
            margins: 12
        }
        spacing: 8
        alignment: 'hfill'

        LKInput {
            id: _img_root
            // text: root.imageRoot
            textColor: root.isValidPath ? 'black' : 'red'
            textHint: 'Input a dirpath to save images'
            Component.onCompleted: {
                this.textEdited.connect(root.imageRootChanged)
            }
        }

        LKField2 {
            id: _link_formt
            title: 'Link format'
            text: `![](./<img_root_name>/<img_file_name>.<img_file_ext>)`
        }

        LKText {
            text: root.imageLink ? root.imageLink : (
                '<font color="grey">Click below button to dump image from ' +
                'clipboard to local.</font>'
            )
        }

        LKButton {
            width: parent.width
            text: 'Dump image'
            onClicked: root.clicked()
        }
    }

//    Item {
//        anchors.fill: parent
//
//        LKRectangle {
//    //        x: target.x
//    //        y: target.y
//            x: target.mapToItem(this, target.x, target.y).x
//            y: target.mapToItem(this, target.x, target.y).y
////            x: mapFromItem(target, target.x, target.y).x
////            y: mapFromItem(target, target.x, target.y).y
//    //        x: mapFromGlobal(
//    //            mapToGlobal(target.x, target.y).x,
//    //            mapToGlobal(target.x, target.y).y,
//    //        ).x
//    //        y: mapFromGlobal(
//    //            mapToGlobal(target.x, target.y).x,
//    //            mapToGlobal(target.x, target.y).y,
//    //        ).y
//    //        x: target.mapToGlobal(target.x, target.y).x
//    //        y: target.mapToGlobal(target.x, target.y).y
//            width: target.width
//            height: target.height
//            border.width: 1
//            border.color: pycolor.red
//            color: 'transparent'
//
//            property var target: _link_formt
//        }
//    }

    Component.onCompleted: {
        py.backend.init_ui(this)
    }
}
