import sys

from PyQt5.QtCore import Qt #,QCoreApplication, pyqtSlot, QRect
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, 
    QTextEdit, QComboBox, QVBoxLayout, QHBoxLayout, QMainWindow,
    QStackedWidget, QCheckBox, QRadioButton, QLineEdit
)
from PyQt5.QtGui import QIntValidator

from wine_ai.engine import WineHelperGUI

from .mixins import WidgetFormMixin
from .helpers import get_data_check_p1, get_data_radio, get_data_input

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
        
        label = QLabel(text="Select your favorite type of wine:")

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
        self.label2 = QLabel(text="User age: ")

        select_box_layout = QVBoxLayout()
        select_box_layout.addWidget(label1)
        select_box_layout.addSpacing(10)
        select_box_layout.addWidget(self.label2)
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


        self.p1 = Widget1(props)
        self.p2 = Widget2(props)
        self.p3 = Widget3(props)
        self.p4 = Widget4(props)
        self.p5 = Widget5(props)
        self.p6 = Widget6(props)

        self.stacked_widget.addWidget(self.p1)
        self.stacked_widget.addWidget(self.p2)
        self.stacked_widget.addWidget(self.p3)
        self.stacked_widget.addWidget(self.p4)
        self.stacked_widget.addWidget(self.p5)
        self.stacked_widget.addWidget(self.p6)

        self.stacked_widget.currentChanged.connect(self.determine_action)


        self.p1.next_button.clicked.connect(self.next_page)

        self.p2.next_button.clicked.connect(self.next_page)
        self.p2.pervious_button.clicked.connect(self.prev_page)

        self.p3.next_button.clicked.connect(self.next_page)
        self.p3.pervious_button.clicked.connect(self.prev_page)

        self.p4.next_button.clicked.connect(self.next_page)
        self.p4.pervious_button.clicked.connect(self.prev_page)

        self.p5.next_button.clicked.connect(self.next_page)
        self.p5.pervious_button.clicked.connect(self.prev_page)

        
        self.p6.pervious_button.clicked.connect(self.prev_page)
        # TODO remove next button from last page
        # add page when you specify price range
        # remove prev button from the first page

        self.setCentralWidget(self.stacked_widget)


    def next_page(self):
        if self.page_index < self.stacked_widget.count() - 1:
            self.page_index += 1
            self.stacked_widget.setCurrentIndex(self.page_index)

    def prev_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.stacked_widget.setCurrentIndex(self.page_index)
            
    def determine_action(self, page_index):
        if page_index == 5:
            print("getting full data")
            data = self.get_full_data() # TODO format data

            self.p6.label2.setText(data.get("result", "No result"))
            


    def get_full_data(self):

        data = {
            "user_age": get_data_input(self.p1),
            "daytime": get_data_radio(self.p2),
            "type_of_meeting": get_data_radio(self.p3),
            "type_of_dish": get_data_radio(self.p4),
            "favorite_wine": get_data_radio(self.p5),
            "price_range": (),
            **get_data_check_p1(self.p1)
        }
        
        engine = WineHelperGUI(data)
        
        engine.reset()
        engine.run()

        return engine.result

         
                
        

def render_window(args=[]):
    app = QApplication(args)
    screen = app.primaryScreen()
    w = MainWindow(screen, title="Wine AI")
    w.show()
    sys.exit(app.exec_())
