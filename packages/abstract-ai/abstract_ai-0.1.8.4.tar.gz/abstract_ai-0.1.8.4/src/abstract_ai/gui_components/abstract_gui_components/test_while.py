from abstract_window_manager import AbstractWindowManager,GUIManager
from abstract_next_read_manager import NextReadManager
from abstract_gui import make_component
window_mgr=AbstractWindowManager()
next_read_mgr=NextReadManager()
next_read_mgr.execute_queue()
window_name = window_mgr.add_window('test',[make_component("text","text window"),make_component("Button","Exit")])
window = window_mgr.get_window_method(window_name=window_name)
enum = window_mgr.get_any_enumeration(window_name=window_name)
if enum==0:
    input(enum)
def event_handler(event, values,window,):
    if event == None:
        print('exiting...')
    return True  # Return True to continue the loop
def get_screen_size():
    return make_component("Window").get_screen_size()
# Define a function to manage the event loop
 
window_mgr.while_window(window_name=window, event_handlers=event_handler)

