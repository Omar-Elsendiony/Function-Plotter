import pytest
from typing import List
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QMessageBox
import main,time
from PySide2.QtTest import QTest
from concurrent.futures import ThreadPoolExecutor

@pytest.fixture
def app(qtbot):
    test_app = main.MainWindow()
    qtbot.addWidget(test_app)
    return test_app

@pytest.mark.parametrize("xMin,xMax,equation,output", [(-100,100,'x^2',0), (-1231,142,'5*x^3+2*x',0), (3,1,'x^3*',1),(-10,10,'2*3/x',0)])
def test_equation_input_correctness_with_many_cases(app,qtbot,xMin,xMax,equation,output):
    def close_window():
        time.sleep(1)
        active_window = QApplication.activeWindow()
        # print(type(active_window))
        global error
        if  isinstance(active_window,QMessageBox):
            active_window.close()
            time.sleep(2)
            active_window = QApplication.activeWindow()
            active_window.close()
            
            error = 1
            return 1 # 1 signifies that there was an error in the execution
        else: error = 0; return 0 # 0 signifies that that there was no error (linux convention)

    app.textXmin.setText(str(xMin))
    app.textXmax.setText(str(xMax))
    app.inputText.setText(str(equation))
    ThreadPoolExecutor().submit(close_window)
    # close_window()
    qtbot.mouseClick(app.btn1, QtCore.Qt.LeftButton)
    time.sleep(2)
    # print(error)
    assert error == output
    time.sleep(1)
    
    pass


@pytest.mark.parametrize("xMin,xMax,equation,output", [('','','x^2',1), ('yr',0,'x^2',1), (3,1,'x^2',1),(-10,10,'x^2',0)])
def test_boundaries_take_correct_values(app, qtbot,xMin,xMax,equation,output):
    def close_window():
        time.sleep(1)
        active_window = QApplication.activeWindow()
        # print(type(active_window))
        global error
        if  isinstance(active_window,QMessageBox):
            active_window.close()
            time.sleep(2)
            active_window = QApplication.activeWindow()
            active_window.close()
            
            error = 1
            return 1 # 1 signifies that there was an error in the execution
        else: error = 0; return 0 # 0 signifies that that there was no error (linux convention)

    # error = 0
    app.textXmin.setText(str(xMin))
    app.textXmax.setText(str(xMax))
    app.inputText.setText(str(equation))
    ThreadPoolExecutor().submit(close_window)
    # close_window()
    qtbot.mouseClick(app.btn1, QtCore.Qt.LeftButton)
    time.sleep(2)
    # print(error)
    assert error == output
    time.sleep(1)


@pytest.mark.parametrize("xMin,xMax,equations,output", [(-100,100,['x^2','5*x^3+2*x','2*3/x','x',''],0)])
def test_alternating_between_previous_equations(app, qtbot,xMin,xMax,equations,output):
    def close_window():
        time.sleep(1)
        active_window = QApplication.activeWindow()
        # print(type(active_window))
        global error
        if  isinstance(active_window,QMessageBox):
            active_window.close()
            time.sleep(2)
            active_window = QApplication.activeWindow()
            active_window.close()
            
            error = 1
            return 1 # 1 signifies that there was an error in the execution
        else: error = 0; return 0 # 0 signifies that that there was no error (linux convention)

    # error = 0
    app.textXmin.setText(str(xMin))
    app.textXmax.setText(str(xMax))
    
    for equation in equations:
        app.inputText.setText(str(equation))
        ThreadPoolExecutor().submit(close_window)
        # close_window()
        qtbot.mouseClick(app.btn1, QtCore.Qt.LeftButton)
        time.sleep(2)
        # print(error)
        assert error == output
        time.sleep(2)
    time.sleep(10)


