# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file provides a full Kivy GUI for GeneSys app generic workflow manipulation
"""

from . import patric_protein_processing

from modules.baseobjects import Workflow
from utils.check_format_utils import check_json_format, check_txt_format

import threading # We will use multithreading to execute long tasks while allowing the user to keep using GeneSys' UI
import ctypes

import kivy
kivy.require('2.3.0') # replace with your current kivy version!
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This screen allows the user to choose where to save the workflow in json format
# and the name of the .json file
class GenerateJsonScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(GenerateJsonScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 2
        self.cols = 2
        
        # Add text boxes
        self.add_widget(Label(text="Introduce the pathname where to save .json workflow (./workflow.json by default): "))
        self.jsonpathname = TextInput(multiline=False)
        self.add_widget(self.jsonpathname)

        # Create a button with margins
        exec_generate_json_button = Button(text='Generate .json file',
                                           size_hint=(None, None),
                                           size=(300, 100),
                                           halign='center',
                                           on_press=self.generate_json)
        exec_generate_json_button.bind(texture_size=exec_generate_json_button.setter('size'))
        self.add_widget(exec_generate_json_button)

        # Button to return to workflow screen
        exec_return_to_workflow_screen = Button(text='Return to workflow menu',
                                                size_hint=(None, None),
                                                halign='center',
                                                size=(300, 100),
                                                on_press=self.return_to_workflow_screen)
        exec_return_to_workflow_screen.bind(texture_size=exec_return_to_workflow_screen.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_return_to_workflow_screen)

    # Call the script that isolates gene codes with the given arguments
    def generate_json(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        if self.jsonpathname.text.__eq__(""):
            self.jsonpathname.text = "./workflow.json"
        json_pathname = self.jsonpathname.text
        if check_json_format(json_pathname):
            self.__workflow.generate_json(path=json_pathname) # Call to generate_json Workflow class method
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            workflow_screen = WorkflowScreen(workflow=self.__workflow)
            self.parent.add_widget(workflow_screen)
        else:
            self.jsonpathname.text = "NOT A JSON FORMAT"

    def return_to_workflow_screen(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = WorkflowScreen(workflow=self.__workflow)
        self.parent.add_widget(workflow_screen)

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This screen allows the user to give a .json path which will load a workflow
# previously saved in that path
class GenerateWorkflowFromJsonScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(GenerateWorkflowFromJsonScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 2
        self.cols = 2
        
        # Add text boxes
        self.add_widget(Label(text="Introduce the pathname of the .json workflow (<./workflow.json> by default): "))
        self.jsonpathname = TextInput(multiline=False)
        self.add_widget(self.jsonpathname)

        # Create a button with margins
        exec_generate_workflow_button = Button(text='Load workflow from json',
                                               size_hint=(None, None),
                                               size=(300, 100),
                                               halign='center',
                                               on_press=self.generate_workflow)
        exec_generate_workflow_button.bind(texture_size=exec_generate_workflow_button.setter('size'))
        self.add_widget(exec_generate_workflow_button)

        # Button to return to workflow screen
        exec_return_to_workflow_screen = Button(text='Return to workflow menu',
                                                halign='center',
                                                size_hint=(None, None),
                                                size=(300, 100),
                                                on_press=self.return_to_workflow_screen)
        exec_return_to_workflow_screen.bind(texture_size=exec_return_to_workflow_screen.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_return_to_workflow_screen)

    def generate_workflow(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Load workflow from json file
        json_pathname = self.jsonpathname.text
        if json_pathname == "":
            json_pathname = "./workflow.json"
        if check_json_format(json_pathname):
            self.__workflow.get_from_json(json_path=json_pathname)            
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            workflow_screen = WorkflowScreen(workflow=self.__workflow)
            self.parent.add_widget(workflow_screen)
        else:
            self.jsonpathname.text = "NOT A JSON FORMAT"

    def return_to_workflow_screen(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = WorkflowScreen(workflow=self.__workflow)
        self.parent.add_widget(workflow_screen)

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class WorkflowScreen(GridLayout):
    # Botón que permita cancelar el workflow actualmente en ejecución. ¿Cómo hago que funcione el workflow si cambio de pantalla? Si vuelves al menú principal, haz que se cancele automáticamente. Nuevo campo booleano en Workflow que indique si se está ejecutando o no, y lo usas para determinar si hay que cancelarlo o no
    # Label que te diga si actualmente hay alguna tarea ejecutándose o no. Requerirá un booleano en la clase Workflow que especifique si se está ejecutando el objeto workflow o no.
    # Clustering y módulos de ciencia de datos
    __workflow = None # This class stores a GeneSys workflow and implements ways to manipulate it

    def __init__(self, workflow=Workflow(), **kwargs): # It receives a workflow set as a new, empty workflow by default
        super(WorkflowScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.

        self.workflow_thread = None # This is the reference to the thread that will run the workflow
        self.__workflow = workflow
        self.rows = 9
        self.cols = 1

        self.add_tasks_button = Button(text='Add tasks to the workflow',
                                       halign='center',
                                       on_press=self.open_add_tasks)
        self.add_widget(self.add_tasks_button)

        rm_last_task_button = Button(text='Remove last task from the workflow',
                                     halign='center',
                                     on_press=self.rm_last_task)
        self.add_widget(rm_last_task_button)

        clean_workflow_button = Button(text='Clean workflow',
                                       halign='center',
                                       on_press=self.clean_workflow)
        self.add_widget(clean_workflow_button)

        # Save workflow button that generates a json with the current workflow parameters and objects
        self.save_workflow_button = Button(text='Save workflow in .json format',
                                           halign='center',
                                           on_press=self.save_workflow)
        self.add_widget(self.save_workflow_button)

        # Load workflow button that fills the workflow with the data stored in a json file
        self.load_workflow_button = Button(text='Load workflow from a .json file',
                                           halign='center',
                                           on_press=self.load_workflow)
        self.add_widget(self.load_workflow_button)

        self.run_workflow_button = Button(text='Run workflow',
                                          halign='center',
                                          on_press=self.run_workflow)
        self.add_widget(self.run_workflow_button)

        self.cancel_workflow_button = Button(text='Cancel workflow',
                                             halign='center',
                                             on_press=self.cancel_workflow)
        self.add_widget(self.cancel_workflow_button)
        self.cancel_workflow_button.disabled = True

        # Show current workflow in a non-editable text window
        self.show_workflow_info()
    
    def open_add_tasks(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = patric_protein_processing.PatricTaskScreen(workflow=self.__workflow)
        self.parent.add_widget(task_screen)

    def rm_last_task(self, instance):
        self.__workflow.remove_last_task()
        for widget in self.children: # Remove the current widget that we are using for the workflow
            if hasattr(widget, 'id') and widget.id == 'WorkflowScrollView': # Remove the widget if it has the ID attribute set and it is our workflow's scrollbar
                self.remove_widget(widget)
                break
        self.show_workflow_info()

    def clean_workflow(self, instance):
        self.__workflow.clean()
        for widget in self.children: # Remove the current widget that we are using for the workflow
            if hasattr(widget, 'id') and widget.id == 'WorkflowScrollView': # Remove the widget if it has the ID attribute set and it is our workflow's scrollbar
                self.remove_widget(widget)
                break
        self.show_workflow_info() # Show the current workflow in a new widget

    def save_workflow(self, instance): # Poder elegir dónde lo guardamos y cómo llamar al fichero .json, lo que requiere una nueva ventana
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        save_workflow_screen = GenerateJsonScreen(workflow=self.__workflow)
        self.parent.add_widget(save_workflow_screen)

    def load_workflow(self, instance): # We want to choose where to save JSON file and which name should be goven to it, so we define a specific screen for it
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        load_workflow_screen = GenerateWorkflowFromJsonScreen(workflow=self.__workflow)
        self.parent.add_widget(load_workflow_screen)

    def run_workflow(self, instance):
        # Execute the workflow in a separated thread
        self.workflow_thread = threading.Thread(target=self.execute_workflow) # We must specifically define a funciton that runs the workflow, otherwise the workflow will be executed before calling to task_thread.start()
        self.run_workflow_button.disabled = True # Disable buttons
        self.add_tasks_button.disabled = True
        self.save_workflow_button.disabled = True
        self.load_workflow_button.disabled = True
        #self.main_menu_button.disabled = True
        self.cancel_workflow_button.disabled = False # Able cancel button
        self.workflow_thread.start()

    def execute_workflow(self):
        self.__workflow.run()
        from kivy.clock import Clock # Update the UI from the main thread using Clock
        Clock.schedule_once(lambda dt: self.on_task_complete(self.__workflow.show_info())) # Creates an anonymous function that takes the dt parameter and calls self.on_task_complete once the thread ends its execution
                                                                                           # (the execution may end wether the workflow is completed or wether it is stopped forcefully).
                                                                                           # The anonymous function receives information about the workflow as a parameter as the context of execution of the thread
                                                                                           # does not have access to the workflow itself (because it is being executed in a different context than our main app)

    def on_task_complete(self, workflow_data=""):
        # Create the popup content
        message_text = "Your Genesys workflow is completed:\n\n"
        if len(self.__workflow.get_tasks()) == 0: # If the workflow has no tasks, we show a message telling so
            message_text += "The workflow has no tasks."
        else:
            message_text += workflow_data
        message_label = Label(text=message_text,
                              size_hint=(None, None),
                              size=(600, 260),
                              halign='center',
                              valign='middle',
                            )
        message_label.bind(texture_size=message_label.setter('size'))
        message_scroll_view = ScrollView(size_hint=(None, None), size=(600, 260)) # We add information about workflow's execution in a scroll type widget
        message_scroll_view.add_widget(message_label)
        
        # Create the popup box where to show the message
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        close_button = Button(text="Close", size_hint=(None, None), halign='center', size=(150, 50))
        box.add_widget(message_scroll_view) # Add the message and the close button to the layout
        box.add_widget(close_button)
        popup = Popup(title="Workflow completed!", content=box, size_hint=(None, None), size=(700, 400)) # Create popup. Size property must be set dinamicaly
        close_button.bind(on_press=popup.dismiss) # Bind the close button to close the popup
        popup.open() # Open the popup

        # Change buttons
        self.run_workflow_button.disabled = False # Recover the button functionality (in case we changed of screen, this line will not have any effect)
        self.add_tasks_button.disabled = False
        self.save_workflow_button.disabled = False
        self.load_workflow_button.disabled = False
        #self.main_menu_button.disabled = False
        self.cancel_workflow_button.disabled = True

    def cancel_workflow(self, instance):
        if self.workflow_thread is not None: # Kill workflow's execution
            self._kill_thread(self.workflow_thread)
            self.workflow_thread = None
    
    def _kill_thread(self, thread):
        # Here we exit the execution of the thread while paying attention to some scenarios
        # that might occur when trying to do so
        if not thread.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("Nonexistent thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def show_workflow_info(self): # Workflow info is shown through a function because it might be called from other methods that modify the workflow
        scroll_view = ScrollView(size_hint=(None, None), size=(Window.width, 250))
        scroll_view.bar_width = 10  # Adjust the scrollbar width here
        workflow_info_label = Label(text='Current Workflow:\n'+self.__workflow.show_info(),
                                    size_hint=(None, None),
                                    size=(Window.width, 250), # Width = Window width / number of columns defined in the view
                                    halign='center',
                                    valign='middle',
                                )
        workflow_info_label.bind(texture_size=workflow_info_label.setter('size'))
        scroll_view.add_widget(workflow_info_label)
        scroll_view.id = 'WorkflowScrollView' # It is crucial to asign an ID to this widget as we may need to remove it when we clean the workflow
        self.add_widget(scroll_view)
