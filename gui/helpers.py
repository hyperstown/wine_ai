from PyQt5.QtWidgets import QRadioButton, QLineEdit


def get_data_radio(widget):
        for child in widget.children():
            if isinstance(child, QRadioButton) and child.isChecked():
                return child.text()
        return ''


def get_data_check_p1(p1):
    return {
        "non_alcoholic_wines": p1.check1.isChecked(),
        "alcoholic_wines": p1.check2.isChecked(),
        "is_drunk": p1.check3.isChecked(),
        "is_vegan": p1.check4.isChecked(),
}

def get_data_input(widget, many=False):
    
    data = []

    for child in widget.children():
        if isinstance(child, QLineEdit):
            try:
                if many:
                    if child.text():
                        data.append(int(child.text())) # meh
                else:
                    return int(child.text())
            except ValueError:
                if many:
                    return tuple()
                return -1
    
    if many:
        return tuple(data)
    return -1
