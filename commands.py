commands={}
# using a dictionary containing function objects as values saves from hassle


def initialize_commands(browser_instance):
    global commands
    commands={'backward':browser_instance.back,
              'forward':browser_instance.forward,
              'quit':browser_instance.quit,
              'reload':browser_instance.reload,
              'down':browser_instance.scroll_down,
              'up':browser_instance.scroll_up,
              'stop_scroll':browser_instance.stop_scrolling,
              'type':browser_instance.enter_text,
              'next_input':browser_instance.next_input,
              'previous_input':browser_instance.previous_input,
              'submit':browser_instance.submit,
              'click':browser_instance.findLink,
              'search':browser_instance.search,
              'open_new_tab':browser_instance.open_new_tab,
              'close_tab':browser_instance.close_tab,
              'change_tab':browser_instance.switch_tab,
              'erase':browser_instance.clear_text
        }
