# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This module contains the main Task and Workflow classes that will
be employed by all GeneSys modules
"""

from abc import abstractmethod
from importlib import import_module
from genericpath import exists
from pymongo import MongoClient
from gridfs import GridFS
import io
import json
import os


##############################################################################
##############################################################################
##############################################################################
##############################################################################


class Task():
    """
    This class encapsulates de commom functionality that all tasks from GeneSys
    share, and establishes the basic structure that allows to the manipulation of
    all Task's subclasses objects
    """

    _returned_info = "" # protected, not private
    _returned_value = -1
    _db_connection = "mongodb://mongo:27017/" # os.environ.get('MONGO_DB') if os.environ.get('MONGO_DB') else "mongodb://mongo:27017/" # La ruta web al contenedor mongo, si es que lo vamos a usar
    _containerized:bool = False # If set to True, _db_connection will be employed to save files in the DB instead of the local system

    def __init__(self, containerized:bool):
        self._containerized = containerized
    
    @abstractmethod    
    def get_parameters(self) -> dict:
        """Allow parameterization of a Task
        """
        parameters = {}
        parameters['returned_info'] = self._returned_info
        parameters['returned_value'] = self._returned_value
        parameters['containerized'] = self._containerized
        return parameters

    @abstractmethod    
    def set_parameters(self, parameters):
        """Will update the values of the parameters of a Task
        """
        self._returned_info = parameters['returned_info']
        self._returned_value = parameters['returned_value']
        self._containerized = parameters['containerized']

    def set_containerization(self, containerized:bool):
        self._containerized = containerized

    '''def set_db_connection(self, db_con:str): # No es necesario por ahora
        self._db_connection = db_con#'''

    ###### TASK EXECUTION ######

    @abstractmethod
    def run(self):
        """Will be the main function of a Task to realize a specific job
        """
        pass

    # def cancel ¿cómo cancelar una tarea en Python?

    # I/O   
    @staticmethod
    def instantiate(class_str):
        """Instantiate a class object of a Task by its path class

        :param class_str: the name of the class
        :type class_str: str

        :return: a instance of a Task
        :rtype: Task
        """

        # Class reflection
        try:
            module_path, class_name = class_str.rsplit('.', 1) # It fails if the name of the class contains dots
            module = import_module(module_path)
            klass = getattr(module, class_name)
        except (ImportError, AttributeError):
            raise ImportError(class_str)        
        # Dynamic instantiation
        instance = klass()
        return instance
    
    def to_dict(self):
        """Generate a dictionary from its parameters and generate a readable structure
            to replicate a Task Object later

        :return: a string object with the elements of a Task
        :rtype: str
        """
        dict = {}
        dict["type"] = self.__class__.__module__ + "." + self.__class__.__name__
        dict.update( self.get_parameters() )
        return dict
    
        # use "json_string = json.dumps(dict)" to get a json object in json_string variable (it requires import json)

    @staticmethod
    def from_dict(dictionary):
        """Read a dictionary (or json structure) and create a Object Task
            with all values with which the previous object Task was saved.
            This is the method that allows replicating any child of Task only knowing its class

        :return: a replicate instance of the Task previosly saved on a json file or dictionary
        :rtype: Task
        """
        # Dynamic instantiation & parameterization
        instance = Task.instantiate(dictionary["type"]) # instantiation of a Task object using the name of the class stored in the dictionary
        instance.set_parameters(dictionary)
        return instance

    def __str__ (self):
        """Allows stream a Task on output
        :return: a dictionary transform to readable str
        :rtype: str
        """
        return str(self.to_dict())
    
    @abstractmethod
    def show_info(self):
        """
        Shows basic information of the task that can be
        useful for the user. It allows us to maintain __str__
        method as a function that returns all the class' parameters
        as a string, while "show_info" would return only the
        parameters that might be useful for the user in order to
        understand what is happening in an instance of the class
        """
        pass



##############################################################################
##############################################################################
##############################################################################
##############################################################################


class Workflow(Task):
    """
    This class stores a list of Task objects which can be executed, saved or
    re-applied over different data in order to make efficient bioinformatic analyses
    """

    __tasks = [] # empty list of tasks
    __results_file = "workflow_results.txt" # Path to a .txt file that will save the returned info and returned value of the workflow
    _returned_value = -1

    def __init__(self, tasks = [], containerized=False):
        super().__init__(containerized=containerized)
        for task in tasks:
            task.set_containerization(containerized) # All the tasks will use the same executionn context as the workflow
            self.__tasks.append(task)

    def get_parameters(self) -> dict:
        """Returns a dictionary with all parameters needed to
            initialize the class object to apply a Task.
            It allows to implement Reflection
        """
        parameters = super().get_parameters()
        parameters['tasks'] = self.__tasks
        parameters['results_file'] = self.__results_file
        return parameters

    def set_parameters(self, parameters: dict):
        """Update the parameters to specific arguments
            for a Task necessary for a Task to apply its functionality.
        """
        super().set_parameters(parameters)
        self.__tasks = parameters['tasks'] # PRE: there is a tag called "tasks" previously defined in the dictionary
        self.__results_file = parameters['results_file']
    
    def get_returned_value(self) -> int:
        return self._returned_value
    
    """
    GET METHODS
    """
        
    def get_tasks(self) -> list:
        """
        Returns the list of Task objects that represent a pipeline/workflow.
        """
        return self.__tasks
    
    def get_len_workflow(self):
        """
        Returns the number of Task objects that are in the current workflow.
        """
        return len(self.__tasks)
    
    def add_task(self, new_task, name = "", descp = ""):
        """Add a Task to the Workflow.
        :param new_task: Task to add in the workflow.
        :param name: Title/Name of the Task. Defaults to "" (None).
        :param descp: Description to explain what the Task does. 
        """
        self.__tasks.append(new_task)

    
    def remove_last_task(self):
        """
        Removes the last task that was added to the workflow.
        """
        if self.get_len_workflow() > 0:
            (self.__tasks).pop()
        return 0


    def clean(self):
        """
        Removes all tasks from the workflow, leaving it empty:
        """
        while self.get_len_workflow() > 0:
            self.remove_last_task()
        return 0


    def run(self):
        """
        Sequentially apply all tasks in the Workflow to a given object.
        It could be, for example, a DataObject or a DataFrame.
        :param obj: Object to apply the Workflow.
        :type obj: DataObject, DataFrame
        :return: The object with all the Tasks applied.
        :rtype: DataObject, DataFrame
        """
        try:
            self._returned_info = ""
            for task in self.__tasks:
                task.run() # It requires that each task can be applied right after the previous one with their own parameters
                task_dict = task.to_dict()
                self._returned_info += '\n--------------\nTASK ' + str(task_dict['type']) + '\n\n' + str(task_dict['returned_info']) + '\nRETURNED VALUE: ' + str(task_dict['returned_value']) + '\n\n'
            self._returned_value = 0
            self.__save_results() # generate de results .txt file
        except SystemExit:
            print("\n\n\nWorkflow stopped forcefully\n\n")

        
    def __save_results(self):
        try:
            info = self._returned_info + "\n\n--------------\nWORKFLOW'S RETURNED VALUE: " + str(self._returned_value)

            if self._containerized:
                # Connect to the database and save the file
                client = MongoClient(self._db_connection)
                db = client['mydb']
                fs = GridFS(db)
                # Save results to Mongodb
                string_io = io.StringIO(info) # Convert string to StringIO
                string_io.seek(0)
                fs.put(string_io.getvalue().encode('utf-8'), filename=self.__results_file) # Save StringIO content to MongoDB as a .txt file

            else:
                with open(self.__results_file, 'w+') as results_file:
                    results_file.write(info)
        except Exception as e:
            print(f"Error. Unable to write workflow's results on file {self.__results_file}: {str(e)}")

    
    def generate_json(self, path = "./workflow.json"):
        """
        Generate an external file to save every task of the workflow
        :param path: file where dictionary generates will be saved
        :type: str
        """
        if self._containerized:
            client = MongoClient(self._db_connection)
            db = client['mydb']
            fs = GridFS(db)
            f_json = io.TextIOWrapper()
            try:
                list_dict_task = [] # List of dictionaries where each dictionary encapsulates a task
                for task in self.get_tasks():
                    list_dict_task.append(task.to_dict())
                json.dump(list_dict_task, f_json)
                f_json.seek(0)
                content = f_json.read()
                f_json_string = io.StringIO(content)
                fs.put(f_json_string.getvalue().encode('utf-8'), filename=path)
                return 0
            except:
                print("Error. Unable to write on file {}".format(path))

        else:
            if exists(path):
                print("File {} already exists, so it will be overwritten".format(path))
            try:
                open(path, "w")
            except:
                print("Error. Unable to open or create {}".format(path))
            try:
                list_dict_task = [] # List of dictionaries where each dictionary encapsulates a task
                for task in self.get_tasks():
                    list_dict_task.append(task.to_dict())
                with open(path, "w+") as f_json:
                    json.dump(list_dict_task, f_json)
                return 0
            except:
                print("Error. Unable to write on file {}".format(path))


    def get_from_json(self, json_path = "./workflow.json", containerized:bool = False):
        self.clean() # First, we delete all previous data from the workflow
        if containerized:
            try:
                client = MongoClient(self._db_connection)
                db = client['mydb']
                fs = GridFS(db)
                file = fs.find_one({"filename": json_path})
                file_content = file.read().decode('utf-8')
                data = json.load(file_content)

                 # Iterate over the data of the file, which corresponds to a list of dictionaries, each dictionary corresponding to a task
                for task in data:
                    new_task = Task(containerized=containerized)
                    new_task = new_task.from_dict(task)
                    self.add_task(new_task=new_task)
                return 0
            except Exception as e:
                print(f"Error. Unable to read{json_path}: {e}")

        else:
            if exists(json_path):
                try:
                    # Read and parse the json file
                    with open(json_path, "r") as file:
                        data = json.load(file)
                    
                    # Iterate over the data of the file, which corresponds to a list of dictionaries, each dictionary corresponding to a task
                    for task in data:
                        new_task = Task(containerized=containerized)
                        new_task = new_task.from_dict(task)
                        self.add_task(new_task=new_task)
                    return 0
                except Exception as e:
                    print(f"Error. Unable to open {json_path}: {e}")
            else:
                print("Error. Unable to find path {}".format(json_path))

   
    def to_dict(self):
        try:
            dict_workflow = {} # List of dictionaries where each dictionary encapsulates a task
            dict_workflow['Containerized:'] = self._containerized
            dict_workflow['Results file:'] = self.__results_file
            dict_workflow['Returned value:'] = self._returned_value
            i = 0
            for task in self.get_tasks():
                i += 1
                dict_workflow[f'Task {i}:'] = task.to_dict()
            return dict_workflow
        except Exception as e:
            print("Error while turning the workflow into dictionary format: %s", e)
    
    """
    STR
    """

    def __str__(self):
        """
        Saves info about the pipeline/workflow.
        """
        result = '\n'
        for task in self.get_tasks():
            result += (task.__str__()) + '\n---------------\n'
        result += 'results file: ' + str(self.__results_file) + '\n'
        return result
    
    def show_info(self):
        """
        Shows info about the pipeline/workflow.
        """
        result = '\n'
        for task in self.get_tasks():
            result += (task.show_info()) + '\n---------------\n'
        result += 'Results file: ' + str(self.__results_file) + '\n'
        return result
        
