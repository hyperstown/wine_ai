from PyQt5.QtCore import pyqtSlot, QRect, Qt, QCoreApplication
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout

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

        if not getattr(self, 'first_page', False):
            h_layout.addWidget(self.pervious_button)
        
        if not getattr(self, 'last_page', False):
            h_layout.addWidget(self.next_button)
        v_layout.addLayout(h_layout)

        v_layout.addWidget(exit_button)
        self.setLayout(v_layout)

    @pyqtSlot()
    def exit_window(self):
        QCoreApplication.instance().quit()