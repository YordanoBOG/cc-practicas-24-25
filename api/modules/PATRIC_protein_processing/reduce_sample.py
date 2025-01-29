import subprocess
import io
from pymongo import MongoClient
from gridfs import GridFS

from api.modules.baseobjects import Task
from api.utils.fasta_processing_utils import save_fasta_string, get_fasta_content
from api.utils.biopython_utils import get_coincidence_percentage

class ReduceSample(Task):
    __limit_percentage = 85
    __pathname_to_reduced_proteins = ""
    __fasta_pathname = ""
    __proteins = {} # We have to store the proteins as an attribute because they will be accesed from more than one method
    __reduced_proteins = {}

    ###### INIT ######

    def __init__(self, containerized:bool=False, fasta_pathname="./proteins.fasta", 
                 pathname_to_reduced_proteins="./reduced_proteins.fasta",
                 percentage=85):
        super().__init__(containerized=containerized)
        self.__fasta_pathname = fasta_pathname
        self.__pathname_to_reduced_proteins = pathname_to_reduced_proteins
        self.__limit_percentage = percentage
    
    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['pathname_to_reduced_proteins'] = self.__pathname_to_reduced_proteins
        parameters['fasta_pathname'] = self.__fasta_pathname
        parameters['proteins'] = self.__proteins
        parameters['reduced_proteins'] = self.__reduced_proteins
        parameters['limit_percentage'] = self.__limit_percentage
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__pathname_to_reduced_proteins = parameters['pathname_to_reduced_proteins']
        self.__fasta_pathname = parameters['fasta_pathname']
        self.__proteins = parameters['proteins']
        self.__reduced_proteins = parameters['reduced_proteins']
        self.__limit_percentage = parameters['limit_percentage']

    # Return information that might be useful for the user
    def show_info(self):
        reduce_sample_dict = self.to_dict()
        reduce_sample_dict.pop('returned_info') # We remove returned info as it is too long to be worth to be showed
        reduce_sample_dict.pop('proteins')
        reduce_sample_dict.pop('reduced_proteins')
        return str(reduce_sample_dict)
    
    ###### FILL CLASS VALUES METHODS #####

    def __get_proteins_from_fasta(self):
        get_prot_res = None
        if self._containerized:
            client = MongoClient("mongodb://mongo:27017/")
            db = client['mydb']
            fs = GridFS(db)
            get_prot_res = get_fasta_content(fasta_path=self.__fasta_pathname, db=fs)
        else:
            get_prot_res  = get_fasta_content(fasta_path=self.__fasta_pathname)  # Returns a tuple where the first element is a boolean of the result
        if get_prot_res[0]:
            self.__proteins = get_prot_res[1]
        else:
            print(f"\n\nUnexpected error occurred while getting the proteins from the fasta file: {get_prot_res[1]}")
            self._returned_info = f"Unexpected error occurred while getting the proteins from the fasta file: {get_prot_res[1]}"


    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self._returned_value = -1
        self._returned_info = ""
        self.__get_proteins_from_fasta() # Fill self.__proteins
        self.__reduce_proteins()

        
    def __reduce_proteins(self):
        temp_proteins = list(self.__proteins.values()) # Copy the values (not the keys) of the initial set of proteins in a temporary list. BEWARE, it may be a superfitial copy
        temp_proteins_index = 0 # We will use an index to access the list, as we will process the proteins
                                # by operating from the current position
                                # whose protein we are analyzing
        while temp_proteins_index < len(temp_proteins):
            prot = temp_proteins[temp_proteins_index]
            if prot not in self.__reduced_proteins.values(): # If the current protein that it is being processed has not been added to the final reduced proteins dictionary yet
                self._returned_info += "\n-----------------------\nComparing protein\n<" + str(prot) + ">\n"
                compare_proteins_index = temp_proteins_index+1 # We will start comparing the current protein with those that are right after the next position of the list
                while compare_proteins_index < len(temp_proteins): # This loop will not be executed for the last protein of the list
                    compared_prot = temp_proteins[compare_proteins_index]
                    self._returned_info += "...with protein:\n<" + str(compared_prot) + ">\n\n"
                    if self.__biopython_compare(prot, compared_prot): # Check if the e_value between two proteins is smaller than the limit e_value of the class (using Biopython tools)
                        # Remove current compared_prot from the temporary list, since it is a protein too similar to "prot"
                        # We do not update "compare_proteins_index" since the current position now stores a new protein to compare
                        self._returned_info += " which did not return a smaller percentage. It is deleted from the protein list.\n\n\n"
                        temp_proteins.pop(compare_proteins_index)
                    else:
                        self._returned_info += " which returned a smaller percentage. It is NOT deleted from the protein list.\n\n\n"
                        compare_proteins_index += 1 # The current compared protein has not been deleted, so we compare the next protein
                
                # Include the current protein in the final proteins dictionary
                dict_protein_element = self.__find_first_matching_item(prot) # Search for the current protein in the proteins class dictionary
                                                                             # It should match only one element as we should have removed
                                                                             # repeated proteins from the .fasta file in a previous task
                if dict_protein_element[0]:
                    # We should enter here always
                    self.__reduced_proteins[dict_protein_element[0]] = dict_protein_element[1] # Asign the key and item values to the returned tuple from __find_first_matching_item
                    self._returned_info += "\nProtein <" + str(prot) + "> with code <" + str(dict_protein_element[0]) + "> has been saved to the reduced proteins dictionary\n"
                else:
                    self._returned_info += "\nThere was no match for protein <" + str(prot) + "> in the protein dictionary\n"
            else:
                # This should never be executed as we are assuming that there are no repeated proteins in the list
                self._returned_info += "\nProtein <" + str(prot) + "> was already in the reduced proteins list\n"
            temp_proteins_index += 1

        self.__generate_reduced_fasta() # Save the reduced proteins sample in a new fasta file

    
    # This function uses the utils.biopython_utils library to catch the similarity percentage from a comparisson between two proteins
    # Returns True if the stored percentage of the class is smaller than the given percentage of the comparisson
    # Note: the bigger the percentage is, the similar the proteins are
    def __biopython_compare(self, prot_one, prot_two):
        result = False
        try:
            percentage = get_coincidence_percentage(prot_one, prot_two)
            self._returned_info += "Similarity percentage " + str(percentage)
            #res_eval[0] # The first returned value is the E-value
            if percentage > self.__limit_percentage:
                result = True
                self._returned_info += " HIGHER THAN limit " + str(self.__limit_percentage)
            else:
                pass
                self._returned_info += " SMALLER THAN limit " + str(self.__limit_percentage)
        except Exception as e:
            self._returned_info += f"Error: {e}"
        return result


    # Returns the first element from self.__proteins that matches a specific item value, correspondign to a certain protein string
    def __find_first_matching_item(self, value):
        for key, val in self.__proteins.items():
            if val == value:
                return key, val
        return False, False # Returns False if no match is found
    

    # Create a .fasta file with the reduced protein sample in the pathname specified in class' parameters
    def __generate_reduced_fasta(self):
        try:
            fasta_content = "" # Contenido a guardar en un documento en la base de datos
            if self._containerized:
                fasta_inutil = open(self.__pathname_to_reduced_proteins, 'w') # Este fasta no lo vamos a guardar
                client = MongoClient("mongodb://mongo:27017/")
                db = client['mydb']
                fs = GridFS(db)
                for protein_key, protein_string in self.__reduced_proteins.items():
                    save_fasta_result = save_fasta_string(protein_string, protein_key, fasta_inutil)
                    fasta_content += save_fasta_result[0]
                    self._returned_info += save_fasta_result[1]
                fasta_file = io.StringIO(fasta_content)
                file_id = fs.put(fasta_file.getvalue().encode('utf-8'), filename=self.__pathname_to_reduced_proteins)
            else:
                touch_fasta = subprocess.run(['touch', self.__pathname_to_reduced_proteins]) # Create the fasta file
                if touch_fasta.returncode == 0:
                    fasta_file = open(self.__pathname_to_reduced_proteins, 'w')
                else:
                    self._returned_info += f"\n\nUnexpected error occurred while creating the reduced proteins .fasta file: {touch_fasta.stderr}"
                for protein_key, protein_string in self.__reduced_proteins.items():
                    save_fasta_result = save_fasta_string(protein_string, protein_key, fasta_file)
                    self._returned_info += save_fasta_result[1]
                fasta_file.close()

            self._returned_info += f"\n\n.fasta file {self.__pathname_to_reduced_proteins} was writen succesfully"
            self._returned_value = 0
        except Exception as e:
            self._returned_info += f"\n\nUnexpected error occurred while getting protein strings from protein codes: {e}"



