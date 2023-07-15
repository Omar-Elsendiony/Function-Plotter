import sys
import matplotlib
import utility
# matplotlib.use('Qt5Agg')
import numpy as np
from PySide2.QtWidgets import QFormLayout, QVBoxLayout, QWidget, QApplication,QHBoxLayout,QPushButton,QMessageBox,QDesktopWidget,QLineEdit,QGridLayout,QFrame,QColormap,QSizePolicy,QLabel

from PySide2.QtGui import QIcon,QPixmap,QPageSize,QScreen,QPalette,QColor,QPainter,QFont,QMouseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class GreenFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        r, g, b, a = self.palette().color(QPalette.Window).toTuple()
        self._bgcolor = QColor(157, 217, 243)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), self._bgcolor)
        super().paintEvent(event)



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QWidget):
    xData = []
    yData = []
    iterator = 0
    listEquations = []
    maxEquations = 4
    reachedMaxEquations = False
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Window minimum dimensions
        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        # canvas with toolbar
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)        
        toolbar = NavigationToolbar(self.canvas, self)


        self.layout3 = QGridLayout()  # the grid layout that holds everything

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = GreenFrame()
        widget.setLayout(layout)
        

        # layout 2 also the side bar
        self.layout2 = QVBoxLayout()
        # toplayout holds xmin and xmax
        self.topLayout = QFormLayout()
        self.addIcon()
        self.addBoundaries()
        self.setEquation()
        self.setButton()

        widget2 = GreenFrame()
        widget2.setLayout(self.layout2)
        # self.setCentralWidget(widget)
        
        # Add a label and a line edit to the form layout
        
        # self.topLayout.setFont
        
        self.layout3.addWidget(widget2,0,0,1,1)
        self.layout3.addWidget(widget,0,1,1,4)

        # self.setStyleSheet("background-color:yellow")
        self.setLayout(self.layout3)
        self.show()

    def setButton(self):
        self.btn1 = QPushButton("Plot",self)
        # btn1.move(0,50)
        self.btn1.clicked.connect(self.update_plot)

        self.btn1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn1.setMaximumWidth(100)
        # btn2.setMaximumWidth(100)
        # btn3.setMaximumWidth(100)
        # btn1.setLayoutDirection()
        self.layout2.addWidget(self.btn1)
        self.btn1.setStyleSheet("background-color:#F21231")
        # btn1.setLayoutDirection(Qt)

    def update_plot(self):
        # make a label and add it
        # QMessageBox.about(self,"info","Error F*")
        xMinVal = self.textXmin.text()
        xMaxVal = self.textXmax.text()
        validity = self.checkValidityBoundaries(xMinVal,xMaxVal)
        if (validity == False): return QMessageBox.about(self,"update error","can not update plot")

        myEquation = self.inputText.text()
        self.xData = np.linspace(int(xMinVal),int(xMaxVal),100)
        res1,res2,type = utility.computeY(myEquation,self.xData)
        # print(type)
        if (type[0] == 'pa'): self.yData=res2[-1]    #pa equivalent to processed array
        elif (type[0] == 'n'):  myOnes = np.ones(len(self.xData)); self.yData=res1[-1]*myOnes #n is a constant number
        elif (type[0] =="error"): QMessageBox.about(self,"update error","error in the equation"); return
        elif (type[0] == 'i'): self.yData = self.xData  # output is the input 'i'
        # print(self.yData)

        ########## now there is no error ##################################
        equationText = self.inputText.text()
        if (self.reachedMaxEquations== False and self.maxEquations > self.iterator):
            self.iterator += 1
            label = QLabelClickable(equationText)
            font = QFont()
            font.setBold(True)
            font.setPointSize(15)
            font.setFamily("sanserif")
            label.setFont(font)
            label.setAutoFillBackground(True)
            label.setStyleSheet("color:blue")
            self.topLayout.addWidget(label)
            self.listEquations.append(label)
            # print(self.iterator)
            
        else:
            self.reachedMaxEquations = True
            self.iterator %= self.maxEquations
            self.listEquations[self.iterator].setText(equationText)
            self.iterator += 1
        ###############################################################


        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xData, self.yData, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def addIcon(self):
        icon1 = QIcon("bar-graph")
        appIcon = QIcon("lap")
        self.setWindowIcon(appIcon)
        # icon1.set
        
        label = QLabel("l",self)
        pixmap = icon1.pixmap(300,300)
        # label.setMinimumHeight(100)
        # label.setMinimumWidth(100)
        # pixmap.scaledToHeight(100)
        label.setPixmap(pixmap)
        
        # label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # label.setStyleSheet("transform: scale(3);")
        # label.setFixedSize(10,10)
        
        label.setStyleSheet("width:1900px; height:1900px; margin:80 150 80 150;padding:0px")
        self.layout2.addWidget(label)

    def addBoundaries(self):
        
        labelXmin = QLabel("Xmin:")
        labelXmax = QLabel("Xmax:")
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        font.setFamily("sanserif")
        labelXmin.setFont(font)
        labelXmax.setFont(font)
        self.textXmin = QLineEdit()
        self.textXmax = QLineEdit()
        self.textXmin.setMaximumWidth(100)
        self.textXmax.setMaximumWidth(100)
        self.textXmax.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.textXmin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        labelXmax.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        labelXmin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.topLayout.addRow(labelXmin, self.textXmin)
        self.topLayout.addRow(labelXmax, self.textXmax)
        self.topLayout.setSizeConstraint(QFormLayout.SetFixedSize)
        self.layout2.addLayout(self.topLayout,stretch=3)
    def setEquation(self):
        self.inputText = QLineEdit()
        self.inputText.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.inputText.setMaxLength(20)  # set the maximum length of the input text to 20

        self.inputText.setMaximumWidth(500)
        self.layout2.addWidget(self.inputText)

    # def showMessage(self):
    #     # QMessageBox.about(self,"info","Error F*")
    #     print("e")

    def checkIntegerOrFloat(self,myInput):
        try:
        # Convert it into integer
            val = int(myInput)
            # print("Input is an integer number. Number = ", val)
        except ValueError:
            try:
                # Convert it into float
                val = float(myInput)
                # print("Input is a float  number. Number = ", val)
            except ValueError:
                # print("No.. input is not a number. It's a string")
                return False
        return True
    def checkValidityBoundaries(self,min,max):
        if (self.checkIntegerOrFloat(min) and self.checkIntegerOrFloat(max)):
            if (int(min) >= int(max)):
                QMessageBox.about(self,"error","minimum x-value cannot be greater than maximum x-value")
                return False
            return True
        else: 
            QMessageBox.about(self,"error","Both xMin and xMax should be either integers or floats only")
            return False
    def update_plot_2(self,myEquation):
        # return QMessageBox.about(self,"info","Error F*")
        xMinVal = self.textXmin.text()
        xMaxVal = self.textXmax.text()
        validity = self.checkValidityBoundaries(xMinVal,xMaxVal)
        if (validity == False): return QMessageBox.about(self,"update error","can not update plot")

        
        self.xData = np.linspace(int(xMinVal),int(xMaxVal),100)
        res1,res2,type = utility.computeY(myEquation,self.xData)
        # print(type)
        if (type[0] == 'pa'): self.yData=res2[-1]    #pa equivalent to processed array
        elif (type[0] == 'n'):  myOnes = np.ones(len(self.xData)); self.yData=res1[-1]*myOnes #n is a constant number
        elif (type[0] =="error"): QMessageBox.about(self,"update error","error in the equation"); return
        elif (type[0] == 'i'): self.yData = self.xData  # output is the input 'i'
        # print(self.yData)
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xData, self.yData, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()


class QLabelClickable(QLabel):
    def __init__(self,parent=None):
        super(QLabelClickable,self).__init__(parent)

    def mousePressEvent(self, ev: QMouseEvent) -> None:    
        w.update_plot_2(self.text()) 
        # return QMessageBox.about(self,"info","Error F*")


if __name__ == '__main__':  
    app = QApplication(sys.argv)
    # app.setActiveWindow(QM)
    w = MainWindow()
    
    app.exec_()