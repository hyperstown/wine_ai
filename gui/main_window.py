import sys

from PyQt5.QtCore import pyqtSlot, QRect, Qt, QCoreApplication
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, 
    QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout, QMainWindow,
    QStackedWidget, QCheckBox, QRadioButton, QLineEdit
)
from PyQt5.QtGui import QIntValidator


class Property:

    def __init__(self, width, height, screen, left=0, top=0, title=""):
        self.width = width
        self.height = height
        self.screen = screen
        self.left = left
        self.top = top
        self.title = title

    def center_horizontally(self):
        self.left = self.screen.size().width() // 2 - self.width // 2

    def center_vertically(self):
        self.top = self.screen.size().height() // 2 - self.height // 2

    def center_window(self):
        self.center_horizontally()
        self.center_vertically()

class WidgetFormMixin:

    def __init__(self, props):
        super().__init__()  # inherit init of QWidget
        self.props = props
        self.set_middle_layout()
        self.view()

    def view(self):

        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        
        # Page description 
        # margin: left, top; width, height
        if hasattr(self, 'label1'):
            self.label1.setGeometry(QRect(0, 0, self.props.width, self.props.height // 3))
            self.label1.setWordWrap(True) # allow word-wrap
            self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # next button
        self.next_button = QPushButton(text="Next")
        self.next_button.setToolTip("Next")
        # prev button
        self.pervious_button = QPushButton(text="Previous")
        self.pervious_button.setToolTip("Previous")

        # exit button
        exit_button = QPushButton(text="Close")
        exit_button.setToolTip("Exit window")
        exit_button.clicked.connect(self.exit_window)


        # add elements to the layout
        if hasattr(self, 'label1'):
            v_layout.addWidget(self.label1)
        
        v_layout.addLayout(self.middle_layout)

        h_layout.addWidget(self.pervious_button)
        h_layout.addWidget(self.next_button)
        v_layout.addLayout(h_layout)

        v_layout.addWidget(exit_button)
        self.setLayout(v_layout)

    @pyqtSlot()
    def exit_window(self):
        QCoreApplication.instance().quit()



class Widget1(WidgetFormMixin, QWidget):

    def set_middle_layout(self):

        # Page description
        self.label1 = QLabel(text="Welcome to Wine adviser!\nPlease answer questions below.")

        # age
        input_label = QLabel("Enter your age")
        input_layout = QVBoxLayout()
        input_filed = QLineEdit()
        input_filed.setValidator(QIntValidator())
        input_filed.setMaxLength(3)
        input_filed.setFixedSize(100, 20)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(input_filed)
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # checkboxes
        self.check1 = QCheckBox("Intrested in non alcoholic wines")
        self.check2 = QCheckBox("Intrested in alcoholic wines")
        self.check3 = QCheckBox("Are you drunk?")
        self.check4 = QCheckBox("Are you a vegan?")

        checkboxes_layout = QVBoxLayout()
        #checkboxes_layout.addLayout(input_layout)
        checkboxes_layout.addWidget(self.check1)
        checkboxes_layout.addWidget(self.check2)
        checkboxes_layout.addWidget(self.check3)
        checkboxes_layout.addWidget(self.check4)
        checkboxes_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.middle_layout = QVBoxLayout()
        self.middle_layout.addLayout(input_layout)
        self.middle_layout.addLayout(checkboxes_layout)
        self.middle_layout.addSpacing(100)



class Widget2(WidgetFormMixin, QWidget):

    def set_middle_layout(self):
        
        label = QLabel(text="Select time of the day:")

        select_box_layout = QVBoxLayout()
        select_box_layout.addWidget(label)
        select_box_layout.addSpacing(10)

        options_list = ['Morning', 'Noon', 'Afternoon', 'Evening']
        
        for option in options_list:
            select_box_layout.addWidget(QRadioButton(option))

        select_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.middle_layout = select_box_layout


class Widget3(WidgetFormMixin, QWidget):

    def set_middle_layout(self):
        
        label = QLabel(text="Select type of meeting:")

        select_box_layout = QVBoxLayout()
        select_box_layout.addWidget(label)
        select_box_layout.addSpacing(10)

        options_list = ['Business', 'Relatives', 'Friends', 'Picnic', 'Drinks']

        for option in options_list:
            select_box_layout.addWidget(QRadioButton(option))

        select_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.middle_layout = select_box_layout


class Widget4(WidgetFormMixin, QWidget):

    def set_middle_layout(self):
        
        label = QLabel(text="Select type of dish:")

        select_box_layout = QVBoxLayout()
        select_box_layout.addWidget(label)
        select_box_layout.addSpacing(10)

        options_list = [
            'Red meat', 'Poultry', 'Pasta', 'Fish', 'Pork',
            'Barbecue', 'Seafood', 'Salad', 'Dessert', 'Appetizer and snacks'
        ]

        for option in options_list:
            select_box_layout.addWidget(QRadioButton(option))

        select_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.middle_layout = select_box_layout


class Widget5(WidgetFormMixin, QWidget):

    def set_middle_layout(self):
        
        label = QLabel(text="Select your favorite wine:")

        select_box_layout = QVBoxLayout()
        select_box_layout.addWidget(label)
        select_box_layout.addSpacing(10)

        options_list = [
            'red', 'sparkling', 'white', 'rosé', 'fortified'
        ]

        for option in options_list:
            select_box_layout.addWidget(QRadioButton(option))

        select_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.middle_layout = select_box_layout


class Widget6(WidgetFormMixin, QWidget):

    def set_middle_layout(self):
        
        label1 = QLabel(text="Your information")
        label2 = QLabel(text="User age: ")

        select_box_layout = QVBoxLayout()
        select_box_layout.addWidget(label1)
        select_box_layout.addSpacing(10)
        select_box_layout.addWidget(label2)
        select_box_layout.addSpacing(10)

        

        select_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.middle_layout = select_box_layout

class MainWindow(QMainWindow):
    def __init__(self, screen, title=""):
        super().__init__()
        props = Property(**{
            "width":1000,
            "height":600,
            "screen": screen,
            "title": title,
        })
        props.center_window()
        
        self.title = title
        self.page_index = 0
        self.resize(props.width, props.height)
        self.move(props.left, props.top)
        self.setWindowTitle(title)

        self.stacked_widget = QStackedWidget()


        p1 = Widget1(props)
        p2 = Widget2(props)
        p3 = Widget3(props)
        p4 = Widget4(props)
        p5 = Widget5(props)
        p6 = Widget6(props)

        self.stacked_widget.addWidget(p1)
        self.stacked_widget.addWidget(p2)
        self.stacked_widget.addWidget(p3)
        self.stacked_widget.addWidget(p4)
        self.stacked_widget.addWidget(p5)
        self.stacked_widget.addWidget(p6)


        p1.next_button.clicked.connect(self.next_page)

        p2.next_button.clicked.connect(self.next_page)
        p2.pervious_button.clicked.connect(self.prev_page)

        p3.next_button.clicked.connect(self.next_page)
        p3.pervious_button.clicked.connect(self.prev_page)

        p4.next_button.clicked.connect(self.next_page)
        p4.pervious_button.clicked.connect(self.prev_page)

        p5.next_button.clicked.connect(self.next_page)
        p5.pervious_button.clicked.connect(self.prev_page)

        p6.next_button.clicked.connect(self.next_page)
        p6.pervious_button.clicked.connect(self.prev_page)

        self.setCentralWidget(self.stacked_widget)
        


    def next_page(self):
        if self.page_index < self.stacked_widget.count() - 1:
            self.page_index += 1
            self.stacked_widget.setCurrentIndex(self.page_index)

    def prev_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.stacked_widget.setCurrentIndex(self.page_index)
        

def render_window():
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    w = MainWindow(screen, title="Wine AI")
    w.show()
    sys.exit(app.exec_())

