def is_press_8_button_controller(lbot, button):
    controlerValues = lbot.getController()
    if controlerValues is not None:
        return controlerValues.get(button)

