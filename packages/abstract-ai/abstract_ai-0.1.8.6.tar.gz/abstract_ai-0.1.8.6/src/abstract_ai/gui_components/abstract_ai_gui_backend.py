"""
abstract_ai module
-------------------

`abstract_ai` is a  feature-rich Python module for interacting with the OpenAI GPT-3 and 4 API.
It provides an easy way to manage requests and responses with the AI and allows for detailed
interaction with the API, giving developers control over the entire process. This module manages
data chunking for large files, allowing the user to process large documents in a single query.
It is highly customizable, with methods allowing modules to maintain context, repeat queries,
adjust token sizes, and even terminate the query loop if necessary.

Main Components:
- GptManager: The central class managing the interactions and flow between various components.
- ApiManager: Manages the OpenAI API keys and headers.
- ModelManager: Manages model selection and querying.
- PromptManager: Handles the generation and management of prompts.
- InstructionManager: Encapsulates instructions for the GPT model.
- ResponseManager: Manages the responses received from the model.

Dependencies:
- abstract_webtools: Contains tools for handling web-related tasks.
- abstract_gui: GUI related tools and components.
- abstract_utilities: Utility functions and classes for general operations.
- abstract_ai_gui_layout: Defines the general layout for the AI GUI.

Key Features:

#Dual Input System
- `Request` and `Prompt Data` sections for straightforward data incorporation.
- Automatic division of prompt data into manageable chunks based on user-specified parameters.

#Intelligent Chunking
- Dynamically segments data considering the set percentage for expected completion per API query and the maximum token limit.
- Executes iterative queries through a response handler class until data processing completes.

#Iterative Query Execution
- Handles documents split into multiple chunks (e.g., 14 chunks result in at least 14 API queries), with real-time adaptive query decisions.

#Instruction Set
- `bot_notation`: allows the module to create notes about the current data chunk to be recieved upon the next query, this
  is such that they can keep context, and understand why the previous selections were made.
- `additional_response`: Allows repeated query execution until a specified condition is met, bypassing token limitations.
- `select_chunks`: allows the module to review either the previous or next chunk of data alongside the current or by itself,
  if needed, the loop will essentially impliment additional_response for this.
- `token_size_adjustment`: allows the module to adjust the size of the chunks being sent, this is a neat feature because they
  do get finicky about this and it can be used in combination with any of the above. 
- `abort`: Authorizes termination of the query loop to conserve resources.
- `suggestions`: Provides a system for leaving future improvement notes.


Author: putkoff
Date: 10/31/2023
Version: 0.1.7.84
Url: 'https://github.com/AbstractEndeavors/abstract_ai',
"""
import os
import pyperclip
from abstract_ai import (ApiManager,
               ModelManager,
               PromptManager,
               ResponseManager,
               SaveManager,
               InstructionManager,
               get_value_from_object)

from abstract_ai.gui_components.abstract_ai_gui_shared import instructions_keys,all_token_keys,test_options_keys
from abstract_ai.gui_components.generate_readme import read_me_window
from abstract_webtools import (UrlManager,
                               SafeRequest,
                               url_grabber_component)
from abstract_gui import (get_event_key_js,
                          text_to_key,
                          AbstractWindowManager,
                          NextReadManager,
                          AbstractBrowser)

from abstract_utilities import (get_any_value,
                                create_new_name,
                                get_sleep,
                                eatAll,
                                safe_json_loads,
                                read_from_file,
                                make_list,
                                ThreadManager,
                                HistoryManager,
                                get_file_create_time,
                                safe_read_from_json)

class GptManager:
    """
    The GptManager class in the abstract_ai module is a complex management system that uses modules to control AI interactions.
    This class initiates window management, browser management, next read management, threading, history management, model management,
    and instruction management. Various update methods set and manage values for the model, API, and instructions, among others.
    It also handles events related to model and instructions, as well as query submissions.
    
    Methods:

    1) __init__() - Initializes types and states of class attributes.

    2) initialize_keys() - Sets up the required keys for events and values on the GUI.

    3) update_api_mgr() - Updates the API manager with new values from GUI.

    4) update_all() - Update instructions manager, model manager, API manager, and other key parts of GptManager with current GUI values.

    5) update_model_mgr() - Updates model manager with latest model name from GUI.

    6) model_event_check() - Checks for model related event and then updates model manager.

    7) unlist_self() - Helper function to unpack a list and assign its value from keys.

    8) get_output_response() - Helper function to format output of a response for easy readability on GUI.

    9) update_text_with_responses() - Formats and displays the response received from GPT model on the GUI.

    10) update_instruction_mgr() - Updates instructions manager with environment values from GUI.

    11) delegate_instruction_text() - Updates instructions section on GUI with values from response.

    12) instruction_event_check() - Checks for instruction related events and then updates instruction manager.

    13) get_new_api_call_name() - Generates a new unique name for the API call.

    14) check_response_mgr_status() - checks if the Response Manager has completed the query process. It returns a Boolean indicating the status.

    15) submit_query() - manages the process of submitting queries to the GPT AI. It starts by disabling the '-SUBMIT_QUERY-'
                         button and then starts a new thread for the get_query method. The method continues to update the progress bar until a response
                         is received, or until the test mode has started, in which case it updates the UI with the test output. After the response is received,
                         the last response file is updated and the text in the UI is updated with the response. The '-SUBMIT_QUERY-' button is then enabled again.

    16) get_query() - handles the operation of querying the AI model. It continues to query until a response is received or until the API call process is stopped.

    17) update_prompt_mgr() - initializes the prompt manager with the information needed for querying the GPT AI model.

    18) update_chunk_info() - updates necessary fields in the chunk info section of the GUI. It gets the chunk data and number from the Prompt
                              Manager's relevant methods and updates the GUI fields.

    19) adjust_chunk_display() - manages the GUI's chunk navigation buttons 'Back' and 'Forward'. It ensures that the navigation is within the
                                 limits of the total chunks and updates the GUI with the correct chunk.

    20) get_chunk_display_numbers() - This helper method retrieves the number of chunks that need to be displayed on the GUI.

    21) determine_chunk_display() - determines the chunk to be displayed based on the chunk navigation buttons 'Back' or 'Forward'.

    22) add_to_chunk() - adds the user's entered request to the request chunk. It also updates the 'chunk_text_number' in the GUI.

    23) clear_chunks() - clears the currently displayed chunk data from the GUI.

    24) chunk_event_check() - checks if any events related to the chunk UI elements were triggered and performs the necessary actions.

    25) append_output() - appends a line of text to the 'other' section of feedback on the GUI.

    26) get_url() - retrieves the URL entered by the user in the corresponding input field of the UI.

    27) get_url_manager() - returns the processed URL. It uses the UrlManager and SafeRequest classes from the abstract_webtools module to process and safe-proof the URL.

    28) query_event_check() - checks if the '-SUBMIT_QUERY-' event was triggered. If it was, it creates a new API call name, initializes the query
                              submission process, and submits the query using the submit_query method.

    29) get_dots() - This is a helper method used in the update_progress_chunks method. It manages the progress tracking visual indication in the UI.
                     It updates the dots string depending on the current state of the dots. If the dots string is full of dots, it resets it to empty.

    30) update_progress_chunks() - updates the progress bar and text status in the GUI, depending on the amount of chunks processed. If the process
                                   is completed, it updates the UI with a sent status and enables the '-SUBMIT_QUERY-' button again.
                                   uses the helper get_dots method for dynamic visual indication of the processing.

        Overall, this class manages each operation in the process of user interaction, query formation, API calling, and result displaying,
        thereby making customized and complex conversations with the GPT model possible.
    """
    def __init__(self):
        """
        initializes the GptManager. It starts by setting the window manager and defining a new window for the chat GPT console. The manager
        for API events is also initiated and the window starts listening for events. The method also initializes the managers for handling the
        AI's responses, the instruction handling, and the submission of queries to the AI. It finally sets a few more internal state variables
        and kicks off the UI's main loop.
 	"""
	self.window_mgr = AbstractWindowManager()
        self.window_name = self.window_mgr.add_window(window_name="Chat GPT Console",layout=get_total_layout())
        self.window_mgr.set_current_window(self.window_name)
        self.window = self.window_mgr.get_window_method(self.window_name)
        self.api_call_list=[]
        self.instruction_bool_keys=[]
        self.values = None
        self.event = None
        self.chunk_title=None
        self.start_query=False
        
        self.browser_mgr = AbstractBrowser(window_mgr=self)
        self.next_read_mgr=NextReadManager()
        self.thread_mgr = ThreadManager()
        self.history_mgr = HistoryManager()
        self.model_mgr = ModelManager()
        self.instruction_mgr = InstructionManager()
        
        self.response=False
        self.updated_progress = False
        self.test_bool=False
        self.output_list=[]
        self.latest_output=[]
        self.request_list=[]
        self.new_response_path_list=[]
        self.response_directories_list=[]
        self.response_path_list = self.aggregate_conversations()
        self.initialize_keys()
        self.loop_one=False
        self.bool_loop=False
        self.window_mgr.while_window(window_name=self.window_name, event_handlers=self.while_window)
        
    def initialize_keys(self):
        """sets up the necessary key definitions for handling events and values from the GUI. It defines the keys
        needed to check the event, the chunk history, the token percentage dropdowns, the instruction keys, and others.
        This is essential for the proper functioning and interaction of the GptManager with the GUI.
 	"""
	self.event_check_keys = ['chunk_event_check',
                                 'response_event_check',
                                 'url_event_check',
                                 'listbox_event_check',
                                 'test_event_check',
                                 'instruction_event_check',
                                 'model_event_check',
                                 'query_event_check',
                                 'readme_event_check',
                                 'browser_event_query']
        self.chunk_history_name = self.history_mgr.add_history_name('chunk')
        self.toke_percentage_dropdowns = ['-COMPLETION_PERCENTAGE-',
                                          '-PROMPT_PERCENTAGE-']
        self.additions_key_list = self.browser_mgr.key_list+['-FILE_TEXT-',
                                                             '-ADD_FILE_TO_CHUNK-',
                                                             '-ADD_URL_TO_CHUNK-']
        self.instruction_pre_keys = instructions_keys
        for key in self.instruction_pre_keys:
            self.instruction_bool_keys.append(text_to_key(text=key,section='bool'))
        self.sectioned_chunk_text_number_key= text_to_key('chunk text number')
        self.sectioned_chunk_data_key = text_to_key('chunk sectioned data')
        self.chunk_display_keys=self.get_bool_and_text_keys(
            all_token_keys
            )
        
    
    def update_api_mgr(self):
        """
        updates the API manager with new values from the GUI. The values include the API content type,
        header, environment, and key.
 	"""
	self.content_type=self.window_mgr.get_from_value(text_to_key("content_type"),delim='')
        self.header=self.window_mgr.get_from_value(text_to_key("header"),delim='')
        self.api_env=self.window_mgr.get_from_value(text_to_key("api_env"),delim='')
        self.api_key=self.window_mgr.get_from_value(text_to_key("api_key"),delim='')
        self.api_mgr = ApiManager(content_type=self.content_type,header=self.header,api_env=self.api_env,api_key=self.api_key)

    def update_all(self):
        """
        updates all the needed managers. It updates the Model Manager, Instruction Manager, API Manager,
        Prompt Manager, and Response Manager with the values currently entered in the GUI.
 	"""
	self.update_model_mgr()
        self.update_instruction_mgr()
        self.update_api_mgr()
        self.update_prompt_mgr()
        self.update_response_mgr()
        self.check_test_bool()
        
#model handling
    def update_model_mgr(self):
        """updates the Model Manager with the latest model name from the GUI.
 	"""
	self.model_mgr = ModelManager(input_model_name=self.window_mgr.get_from_value(text_to_key('model')))
        self.window_mgr.update_value(key=text_to_key('model'),value=self.model_mgr.selected_model_name)
        self.window_mgr.update_value(key=text_to_key('endpoint'),value=self.model_mgr.selected_endpoint)
        self.window_mgr.update_value(key=text_to_key('max_tokens'),value=self.model_mgr.selected_max_tokens)
        
    def model_event_check(self):
        """checks if there was a model-related event and, if there was, updates the Model Manager.
 	"""
	if self.event in "-MODEL-":
            self.update_model_mgr()
        else:
            return False
        return True
    
##response hanling
    def unlist_self(self,keys):
        """A helper method that takes a list of keys as a parameter, iterates over each key, and checks if
           the value of the corresponding key in the class is a non-empty list. If it is, it updates the class's attribute with the last element in the list.
 	"""
	for key in keys:
            value = getattr(self,key)
            if isinstance(value,list) and value:
                value = value[-1]
            setattr(self,key,value)
    def get_output_response(self,model="None",title="None",request="None",response="None"):
        """A helper method that formats the output string of a response in a clear and readable manner.
           It includes information about the model, title, user request, and AI response.
 	"""
	model = f"#MODEL#{self.get_new_line(1)}{self.last_model}{self.get_new_line(2)}"
        title = f"#TITLE#{self.get_new_line(1)}{str(title)}{self.get_new_line(2)}"
        request = f"#USER REQUEST#{self.get_new_line(1)}{str(request)}{self.get_new_line(2)}"
        response = f"#RESPONSE#{self.get_new_line(2)}{str(response)}{self.get_new_line(2)}"
        return f"{model}{title}{request}{response}"
        
    def update_text_with_responses(self):
        """gets the latest response from the AI, formats it using the get_output_response helper method,
           and updates the GUI's '-RESPONSE-' key with the formatted string.
 	"""
	output_keys = []
        self.last_prompt= get_any_value(safe_json_loads(self.current_output),'prompt')
        self.last_response = get_any_value(safe_json_loads(self.current_output),'response')
        self.last_file_path= get_any_value(safe_json_loads(self.current_output),'file_path')
        self.last_title= get_any_value(safe_json_loads(self.current_output),'title')
        self.unlist_self(["last_prompt","last_title","last_file_path","last_prompt"])
        self.last_content = get_any_value(safe_json_loads(self.last_response),'content')
        self.last_api_response = get_any_value(safe_json_loads(self.last_response),'api_response')
        self.last_model =get_any_value(safe_json_loads(self.last_response),'model')
        self.unlist_self(["last_model","last_api_response","last_content"])
        self.window_mgr.update_value(key=text_to_key('title input'),value=self.last_title)
        response_content = self.last_content
        if self.last_api_response:
            response_content=self.last_api_response
            self.delegate_instruction_text()
        self.window_mgr.update_value('-RESPONSE-',self.get_output_response(model=self.last_model,
                                                                           title=self.last_title,
                                                                           request=self.request_list[-1],
                                                                           response=response_content))
#instructions handling handling
    def update_instruction_mgr(self):
        """
        updates the Instruction Manager with the environment values from the GUI. If the '-instructions-'
        key in the UI is set, it also updates the Instruction Manager's attributes for each instruction key.
 	"""
	for i,key in enumerate(self.instruction_pre_keys):
            value = self.window_mgr.get_from_value(text_to_key(text=key,section="BOOL"))
            if value:
                value = self.window_mgr.get_from_value(text_to_key(text=key,section="TEXT"))
                if value == '':
                    value = True
            setattr(self, self.instruction_pre_keys[i], value)
        self.api_response=True
        if not self.window_mgr.get_from_value(text_to_key(text='instructions',section="BOOL")):
            self.api_response=False
            for i,key in enumerate(self.instruction_pre_keys):
                setattr(self, self.instruction_pre_keys[i], None)
        self.instruction_mgr = InstructionManager(api_response=self.api_response,
                                                  notation=self.notation,
                                                  suggestions=self.suggestions,
                                                  abort=self.abort,
                                                  generate_title=self.generate_title,
                                                  additional_responses=self.additional_responses,
                                                  additional_instruction=self.additional_instruction,
                                                  request_chunks=self.request_chunks,
                                                  prompt_as_previous=self.prompt_as_previous,
                                                  token_adjustment=self.token_adjustment)
        for key in self.instruction_pre_keys:
            bool_key = text_to_key(key,section='BOOL')
            text_key = text_to_key(key,section='TEXT')
            value = getattr(self.instruction_mgr, key)
            if not bool(value) or value == "return false":
                value = ''
            elif key in self.instruction_mgr.instructions_js:
                value=self.instruction_mgr.instructions_js[key]
            if value not in ['True','False',True,False]:
                self.window_mgr.update_value(key=text_key,value=value)
                
    def delegate_instruction_text(self):
        """
        updates the instructions section in the GUI with the values in the latest response. If the instruction
        key isn't in the GUI's value list, it appends the instruction to the '-other-' section of feedback in the GUI.
 	"""
	for key in self.instruction_pre_keys:
            value = get_any_value(safe_json_loads(self.last_content),key)
            setattr(self,'last_'+key,value)
            self.unlist_self(['last_'+key])
            instruction_key = text_to_key(key,section='feedback')
            if instruction_key not in self.window_mgr.get_values():
                if value:
                    self.append_output(text_to_key(text='other',section='feedback'),f"{key}: {value}"+'\n')
            else:
                self.window_mgr.update_value(key=instruction_key,value=value)

    def instruction_event_check(self):
        """
        checks if there was an instruction-related event and updates the Instruction Manager if there was one.
        It then updates the Prompt Manager with the latest instructions.
 	"""
	if self.event in self.instruction_bool_keys:
            self.update_instruction_mgr()
            self.update_prompt_mgr() 

##query events
    def get_new_api_call_name(self):
        """
        A helper method that generates and appends a new unique API call name to the api_call_list.
 	"""
	call_name = create_new_name(name='api_call',names_list=self.api_call_list)
        if call_name not in self.api_call_list:
            self.api_call_list.append(call_name)
    def query_event_check(self):
        """
        checks if the '-SUBMIT_QUERY-' event was triggered. If it was, it creates a new API call name, initializes
        the query submission process, and submits the query using the submit_query method.
	"""
	if self.event == "-SUBMIT_QUERY-":
            self.get_new_api_call_name()
            self.start_query= False
            self.updated_progress=False
            self.response_mgr.re_initialize_query()
            self.submit_query()
        else:
            return False
        return True
    
    def get_dots(self):
        """
        This is a helper method used in the update_progress_chunks method. It manages the progress tracking visual
        indication in the UI. It updates the dots string depending on the current state of the dots. If the dots string
        is full of dots, it resets it to empty.
        """
	count = 0
        stop = False
        dots = ''
        for each in self.dots: 
            if each == ' ' and stop == False:
                dots+='.'
                stop = True
            else:
                dots+=each
        self.dots = dots
        if stop == False:
            self.dots = '   '
        get_sleep(1)
        status='Testing'
        if self.test_bool == False:
            status = "Updating Content" if not self.updated_progress else "Sending"
        self.window_mgr.update_value(key='-PROGRESS_TEXT-', value=f'{status}{self.dots}')
        
    def update_progress_chunks(self,done=False):
        """
        updates the progress bar and text status in the GUI, depending on the amount of chunks processed. If the
        process is completed, it updates the UI with a sent status and enables the '-SUBMIT_QUERY-' button again.
        uses the helper get_dots method for dynamic visual indication of the processing.
	"""
	chunk = int(self.token_dist[0]['chunk']['total'])
        i_query = int(self.response_mgr.i_query)
        if done == True:
            self.window['-PROGRESS-'].update_bar(100, 100)
            self.window_mgr.update_value(key='-QUERY_COUNT-', value=f"a total of {chunk} chunks have been sent")
            self.window_mgr.update_value(key='-PROGRESS_TEXT-', value='SENT')
            self.updated_progress = True
        else:
            self.get_dots()
            self.window['-PROGRESS-'].update_bar(min(i_query,1), min(chunk,2))
            self.window_mgr.update_value(key='-QUERY_COUNT-', value=f"chunk {i_query+1} of {min(chunk,1)} being sent")
            
    def check_response_mgr_status(self):
        """
        checks if the Response Manager has completed the query process. It returns a Boolean indicating the status.
	"""
	if not self.test_bool:
            return self.response_mgr.query_done
        return self.start_query
    
    def submit_query(self):
        """
        manages the process of submitting queries to the GPT AI. It starts by disabling the '-SUBMIT_QUERY-'
        button and then starts a new thread for the get_query method. The method continues to update the progress
        bar until a response is received, or until the test mode has started, in which case it updates the UI with the
        test output. After the response is received, the last response file is updated and the text in the UI is updated
        with the response. The '-SUBMIT_QUERY-' button is then enabled again.
	"""
	self.request_list.append(self.request)
        self.window["-SUBMIT_QUERY-"].update(disabled=True)
        self.dots = '...'
        self.start_query=False
        while self.check_response_mgr_status() == False or self.start_query == False:
            self.update_progress_chunks()
            if not self.updated_progress:
                self.update_all()
                if self.test_bool == False:
                    self.thread_mgr.add_thread(name=self.api_call_list[-1],target_function=self.get_query,overwrite=True)
                    self.thread_mgr.start(self.api_call_list[-1])
                else:
                    self.latest_output=[safe_read_from_json(self.test_file_path)]
                self.start_query=True    
                self.updated_progress = True
        if not self.test_bool:
            self.latest_output=self.thread_mgr.get_last_result(self.api_call_list[-1])
        self.output_list.append(self.latest_output)
        self.request_list.append(self.request)
        self.update_progress_chunks(done=True)
        self.update_last_response_file()
        self.update_text_with_responses()
        self.window["-SUBMIT_QUERY-"].update(disabled=False)
        if not self.window_mgr.get_values()['-REUSE_CHUNK_DATA-']:
            self.window_mgr.update_value(key=text_to_key('prompt_data'),value='')
        self.response=False
        
    def get_query(self):
        """
        handles the operation of querying the AI model. It continues to query until a response is
        received or until the API call process is stopped.
	"""
	while not self.response_mgr.query_done:
            if self.response:
                self.thread_mgr.stop(self.api_call_list[-1])
            self.response = self.response_mgr.initial_query()
            if self.response_mgr.query_done:
                print('Response Recieved')
        self.thread_mgr.stop(self.api_call_list[-1],result=self.response)
        
##chunk info
    def update_prompt_mgr(self,prompt_data=None,token_dist=None,completion_percentage=None,bot_notation=None,chunk=None,chunk_type="CODE"):
        """
        initializes the prompt manager with the information needed for querying the GPT AI model.
	"""
	self.role=self.window_mgr.get_from_value('-ROLE-')
        if completion_percentage == None:
            completion_percentage=self.window_mgr.get_from_value('-COMPLETION_PERCENTAGE-')
        self.completion_percentage=completion_percentage
        if prompt_data == None:
            prompt_data = self.window_mgr.get_from_value('-PROMPT_DATA-')
        self.prompt_data=prompt_data
        self.chunk_type=chunk_type
        self.request=self.window_mgr.get_from_value(text_to_key('request'))
        self.token_dist=token_dist
        self.bot_notation=bot_notation
        self.chunk=chunk
        self.prompt_mgr = PromptManager(instruction_mgr=self.instruction_mgr,
                                   model_mgr=self.model_mgr,
                                   role=self.role,
                                   completion_percentage=self.completion_percentage,
                                   prompt_data=self.prompt_data,
                                   request=self.request,
                                   token_dist=self.token_dist,
                                   bot_notation=self.bot_notation,
                                   chunk=self.chunk,
                                   chunk_type=self.chunk_type)
        self.chunk_text_number_actual = 0
        self.window_mgr.update_value(key='-QUERY-',value=self.prompt_mgr.create_prompt(self.chunk_text_number_actual))
        self.token_dist = self.prompt_mgr.token_dist
        if len(prompt_data) == 0:
            self.chunk_text_number_display=0
        else:
            self.chunk_text_number_display = 1
        self.window_mgr.update_value(key='-CHUNK_TEXT_NUMBER-',value=self.chunk_text_number_display)
        self.update_chunk_info(self.chunk_text_number_actual)
        
    def update_chunk_info(self,chunk_iteration):
        """
        updates necessary fields in the chunk info section of the GUI.
        It gets the chunk data and number from the Prompt Manager's relevant methods and updates the GUI fields.
 	"""
	if self.token_dist:
            if chunk_iteration < len(self.token_dist) and chunk_iteration >=0:
                self.chunk_dist_section = self.token_dist[chunk_iteration]
                self.window_mgr.update_value(key=self.sectioned_chunk_data_key, value=self.chunk_dist_section['chunk']['data'])
                for key in self.chunk_display_keys:
                    spl = key[1:-1].lower().split('_')
                    if spl[0] in self.chunk_dist_section:
                        if spl[-1] in self.chunk_dist_section[spl[0]]:
                            self.window_mgr.update_value(key=key,value=self.chunk_dist_section[spl[0]][spl[-1]])
                            
    def adjust_chunk_display(self,num):
        """
        manages the GUI's chunk navigation buttons 'Back' and 'Forward'.
        It ensures that the navigation is within the limits of the total chunks and updates the GUI with the correct chunk.
 	"""
	self.chunk_text_number_actual+=num
        self.chunk_text_number_display+=num
        self.window_mgr.update_value(key='-QUERY-',value=self.prompt_mgr.create_prompt(self.chunk_text_number_actual))
        self.update_chunk_info(chunk_iteration=self.chunk_text_number_actual)
        
        self.window_mgr.update_value(key='-CHUNK_TEXT_NUMBER-',value=self.chunk_text_number_display)        
    def get_chunk_display_numbers(self):
        """
        This helper method retrieves the number of chunks that need to be displayed on the GUI.
 	"""
	self.chunk_text_number_display = int(self.window_mgr.get_from_value('-CHUNK_TEXT_NUMBER-'))
        if self.chunk_text_number_display >0:
            self.chunk_text_number_actual = self.chunk_text_number_display-1
            
    def determine_chunk_display(self,event):
        """
        determines the chunk to be displayed based on the chunk navigation buttons 'Back' or 'Forward'.
 	"""
	self.get_chunk_display_numbers()
        if len(self.prompt_data)>0:
            if self.event == '-CHUNK_TEXT_BACK-':
                if self.chunk_text_number_actual >0:
                    self.adjust_chunk_display(-1)
            elif self.event == '-CHUNK_TEXT_FORWARD-':
                if self.chunk_text_number_display < len(self.token_dist):
                    self.adjust_chunk_display(1)

    def update_chunk_info(self,chunk_iteration):
        if self.token_dist:
            if chunk_iteration < len(self.token_dist) and chunk_iteration >=0:
                self.chunk_dist_section = self.token_dist[chunk_iteration]
                self.window_mgr.update_value(key=self.sectioned_chunk_data_key, value=self.chunk_dist_section['chunk']['data'])
                for key in self.chunk_display_keys:
                    spl = key[1:-1].lower().split('_')
                    if spl[0] in self.chunk_dist_section:
                        if spl[-1] in self.chunk_dist_section[spl[0]]:
                            self.window_mgr.update_value(key=key,value=self.chunk_dist_section[spl[0]][spl[-1]])

    def add_to_chunk(self,content):
        """
        adds the user's entered request to the request chunk. It also updates the 'chunk_text_number' in the GUI.
 	"""
	if self.window_mgr.get_from_value('-AUTO_CHUNK_TITLE-'):
            if self.chunk_title:
                content="# SOURCE #\n"+self.chunk_title+'\n# CONTENT #\n'+content+"\n# END SOURCE #"+self.chunk_title
        if self.window_mgr.get_from_value('-APPEND_CHUNKS-'):
            content = self.window_mgr.get_from_value('-PROMPT_DATA-')+'\n\n'+content
        self.window_mgr.update_value(key='-PROMPT_DATA-',value=eatAll(content,['\n']))
        self.history_mgr.add_to_history(name=self.chunk_history_name,data=content)
        return content
    
    def clear_chunks(self):
        """clears the currently displayed chunk data from the GUI.
 	"""
	content = ''
        self.window_mgr.update_value(key='-PROMPT_DATA-',value=content)
        self.history_mgr.add_to_history(name=self.chunk_history_name,data=content)
        return content
    
    ## chunk data keys
    def chunk_event_check(self):
        """
        checks if any events related to the chunk UI elements were triggered and performs the necessary actions.
 	"""
	if self.event in ['-CHUNK_TEXT_BACK-','-CHUNK_TEXT_FORWARD-']:
            self.determine_chunk_display(self.event)
        elif self.event in ['-REDO_CHUNKS-',
                            '-ADD_URL_TO_CHUNK-',
                            '-ADD_FILE_TO_CHUNK-',
                            '-COMPLETION_PERCENTAGE-',
                            '-PROMPT_PERCENTAGE-'] or self.script_event_js['found'] in ['-FILE_TEXT-',
                                                                                        '-ADD_FILE_TO_CHUNK-',
                                                                                        '-ADD_URL_TO_CHUNK-']:
            data=None
            completion_percentage=None
            if self.event == '-CLEAR_CHUNKS-':
                data = self.clear_chunks()
                self.chunk_type = None
                
            elif self.event in self.toke_percentage_dropdowns:
                data = self.window_mgr.get_from_value('-PROMPT_DATA-')
                other_percentage = self.get_remainder(self.window_mgr.get_values()[self.event])
                for key in self.toke_percentage_dropdowns:
                    if key != self.event:
                        remainder_key=key
                        
                self.window_mgr.update_value(key=remainder_key,value=other_percentage)
                completion_percentage = other_percentage
                if self.event == '-COMPLETION_PERCENTAGE-':
                    completion_percentage = 100 - other_percentage
                    
            elif self.event == '-UNDO_CHUNKS-':
                data = self.history_mgr.undo(self.chunk_history_name)
                self.window_mgr.update_value(key='-PROMPT_DATA-',value=data)
                
            elif self.event == '-REDO_CHUNKS-':
                data = self.history_mgr.redo(self.chunk_history_name)
                self.window_mgr.update_value(key='-PROMPT_DATA-',value=data)
                
            elif self.event == '-ADD_URL_TO_CHUNK-':
                self.chunk_title=self.window_mgr.get_values()[text_to_key('-CHUNK_TITLE-',section='url')]
                data = self.add_to_chunk(self.window_mgr.get_values()['-URL_TEXT-'])
                self.chunk_type=self.url_chunk_type
                
            elif self.script_event_js['found']=='-ADD_FILE_TO_CHUNK-':
                self.chunk_title=self.window_mgr.get_values()[text_to_key('-CHUNK_TITLE-',section='files')]
                data = self.add_to_chunk(self.window_mgr.get_values()[self.script_event_js['-FILE_TEXT-']])
                self.chunk_type='CODE'
            self.update_prompt_mgr(prompt_data=data,completion_percentage=completion_percentage)
        else:
            return False
        return True
    def append_output(self,key,new_content):
        """
        appends a line of text to the 'other' section of feedback on the GUI.
 	"""
	self.window_mgr.update_value(key=key,value=self.window_mgr.get_from_value(key)+'\n\n'+new_content)
        
    def get_url(self):
        """
        retrieves the URL entered by the user in the corresponding input field of the UI.
 	"""
	url = self.window_mgr.get_values()['-URL-']
        if url==None:
            url_list =self.window_mgr.get_values()['-URL_LIST-']
            url = safe_list_return(url_list)
        return url
    
    def get_url_manager(self,url=None):
        """
        returns the processed URL. It uses the UrlManager and SafeRequest classes from the abstract_webtools
        module to process and safe-proof the URL.
 	"""
	url = url or self.get_url()
        url_manager = UrlManager(url=url)    
        return url_manager

    def url_event_check(self):
        """
        Checks if a URL event has been triggered.

        An event is triggered when a user interacts with the URL management interface.
        This function prompts the SafeRequest module to return the HTML content or the
        BeautifulSoup object of the specified URL.

        Returns:
            bool: True if a URL event has been triggered, otherwise False
        """
        if self.event in ['-GET_SOUP-',
                          '-GET_SOURCE_CODE-',
                          '-ADD_URL-']:
            url_manager = self.get_url_manager()
            if self.event in ['-GET_SOUP-',
                              '-GET_SOURCE_CODE-']:
                self.chunk_title=None
                data=self.window_mgr.get_values()['-URL_TEXT-']
                url=None
                if url_manager.url:
                    url = url_manager.url
                if self.event=='-GET_SOUP-':
                    self.url_chunk_type='SOUP'
                    data = url_grabber_component(url=url)
                    self.window_mgr.update_value(key='-URL_TEXT-',value=data)
                elif url_manager.url and self.event=='-GET_SOURCE_CODE-':
                    url_list =self.window_mgr.get_values()['-URL_LIST-']
                    if url_list:
                        url = UrlManager(url=self.window_mgr.get_values()['-URL_LIST-'][0]).url
                        self.chunk_title=url
                        self.window_mgr.update_value(key=text_to_key('-CHUNK_TITLE-',section='url'),value=url)
                    request_manager = SafeRequest(url_manager=url_manager)
                    if self.event == '-GET_SOURCE_CODE-':
                        self.url_chunk_type='URL'
                        data = request_manager.source_code
                else:
                    print(f'url {url} is malformed... aborting...')
            elif self.event == '-ADD_URL-':
                url = url_manager.url
                url_list = make_list(self.window_mgr.get_values()['-URL_LIST-']) or make_list(url)
                if url_list:
                    if url not in url_list:
                        url_list.append(url)
                self.window_mgr.update_value(key='-URL_LIST-',args={"values":url_list})
        else:
            return False
        return True

#test tools management
    def check_test_bool(self):
        """
        Checks the status of the `self.test_bool` attribute.

        `self.test_bool` is updated based on the user interaction with the testing tools interface.
        """
        if self.window_mgr.get_values():
            self.test_file_path = self.window_mgr.get_values()['-TEST_FILE_INPUT-']
            self.window_mgr.update_value('-TEST_FILE-',self.test_file_path)
            if self.event=='-TEST_RUN-':
                self.test_bool=self.window_mgr.get_values()['-TEST_RUN-']
                if self.test_bool:
                    status_color = "green"
                    self.window_mgr.update_value(key='-PROGRESS_TEXT-', value='TESTING')
                    if self.test_file_path:
                        self.test_bool=os.path.isfile(self.test_file_path)
                else:
                    status_color = "light blue" 
                    self.window_mgr.update_value(key='-PROGRESS_TEXT-', value='Awaiting Prompt')
                self.window_mgr.update_value(key='-PROGRESS_TEXT-', args={"value":'TESTING',"background_color":status_color})
    def test_event_check(self):
        """
        Checks if a testing event has been triggered.

        A testing event is triggered when a user interacts with the testing features within the module.

        Returns:
            bool: True if a testing event has been triggered, otherwise False
        """
        if self.event in ['-TEST_RUN-','-TEST_FILES-']:
            self.check_test_bool()
        else:
            return False
        return True

## response tools management
    #response file management
    def listbox_event_check(self):
        """
        Checks if a listbox event has been triggered.

        A listbox event is triggered when a user interacts with the listbox GUI component.
        This function updates the GUI with the content of the selected file.

        Returns:
            bool: True if a listbox event has been triggered, otherwise False
        """
        if self.script_event_js['found'] in ['-BROWSER_LIST-',
                                             '-FILES_LIST-']:
            if self.script_event_js['found'] == '-FILES_LIST-':
                if not hasattr(self,'last_selected_in_list'):
                    self.last_selected_in_list=None
                current_select = self.window_mgr.get_values()[self.event]
                if current_select:
                    current_select=current_select[0]
                    if self.last_selected_in_list == current_select:
                        if os.path.isfile(current_select):
                            data = safe_read_from_json(current_select)
                            self.window_mgr.update_value(text_to_key('-FILE_TEXT-',section=self.script_event_js['section']),str(data))
                    self.last_selected_in_list = current_select
            file_path = self.window_mgr.get_values()[self.script_event_js['-DIR-']]
            files_list = self.window_mgr.get_values()[self.script_event_js['-BROWSER_LIST-']]
            if not os.path.isfile(file_path) and files_list:
                file_path = os.path.join(file_path,files_list[0])
                if not os.path.isfile(file_path):
                    self.browser_event_query(svalues=self.window_mgr.get_values(),event=self.event,window=self.window)
                    file_path=None
            if file_path:
                try:
                    if os.path.splitext(file_path)[-1] == '.docx':
                        contents = read_docx(file_path)
                    else:
                        contents = read_from_file_with_multiple_encodings(file_path)
                    self.window_mgr.update_value(key=self.script_event_js['-FILE_TEXT-'],value=safe_json_loads(contents))
                    self.chunk_title=os.path.basename(files_list[0])
                    self.window_mgr.update_value(key=text_to_key('-CHUNK_TITLE-',section='files'),value=self.chunk_title)
                except:
                    print(f"cannot read from path {file_path}")
        else:
            return False
        return True

    def update_last_response_file(self):
        """
        Updates the path to the last file that recorded a response.

        This function also updates the GUI with the contents of the new file.
        """
        if self.test_bool:
            self.last_response_file=self.test_file_path
        else:
            self.last_response_file = self.response_mgr.save_manager.file_path
        self.last_directory=os.path.dirname(self.last_response_file)
        self.window_mgr.update_value(key='-DIR_RESPONSES-',value=self.last_directory)
        self.update_response_list_box()
        self.window["-DIRECTORY_BROWSER_RESPONSES-"].InitialFolder=self.last_directory
        self.window["-FILE_BROWSER_RESPONSES-"].InitialFolder=self.last_directory
        self.initialize_output_display()
        
    def update_response_list_box(self):
        """
        Update the List Box component that displays saved responses.

        This function is often called after a new API response has been received and saved.
        """
        for data in self.latest_output:
            file_path = get_any_value(data,'file_path')
            if file_path in self.new_response_path_list:
                self.new_response_path_list.remove(file_path)
            self.new_response_path_list.append(file_path)
        files_list = self.window['-FILES_LIST_RESPONSES-'].Values
        if file_path in self.new_response_path_list:
            if file_path in files_list:
                files_list.remove(file_path)
        files_list=self.new_response_path_list+files_list
        self.window_mgr.update_value('-FILES_LIST_RESPONSES-',args={"values":files_list})

    def aggregate_conversations(self,directory:str=None):
        """
        Aggregates conversations from JSON files in the specified directory.

        Args:
            directory (str): The directory containing the JSON files. If none, it will take the current working directory.

        Returns:
            list: A list of aggregated conversations.
        """
        if directory == None:
            directory = os.getcwd()
        json_files, lsAll = [], []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".json"):
                    file = os.path.join(root, file)
                    json_files.append((get_file_create_time(file), file))
        sorted_json_files = sorted(json_files, key=lambda x: x[0])
        aggregated_conversations = []
        chat_log_file = open("chat_log.txt", "w")
        model = 'gpt'
        for file in sorted_json_files:
            file = file[1]
            data = safe_read_from_json(file)
            if data:
                relevant_values={}
                relevant_keys = ['id', 'object', 'created', 'model']
                for key in relevant_keys:
                    value = get_any_value(data,key)
                    if value:
                        relevant_values[key]=value
                if len(relevant_values.keys())==len(relevant_keys):
                    if file not in aggregated_conversations:
                        aggregated_conversations.append(file)
                    dir_name=os.path.dirname(file)
                    if dir_name not in self.response_directories_list:
                        self.response_directories_list.append(dir_name)
           
        #self.next_read_mgr.add_to_queue(self.window_mgr.update_value,'-FILES_LIST_RESPONSES-',args={"values":aggregated_conversations})
        return aggregated_conversations

    ##response output display functions
    def update_response_mgr(self):
        self.response_mgr = ResponseManager(prompt_mgr=self.prompt_mgr,api_mgr=self.api_mgr)

    def initialize_output_display(self):
        """
        Initializes the display of the latest output in the GUI.
        """
        self.current_output=self.latest_output[-1]
        self.response_text_number_actual=0
        self.response_text_number_display=1
        self.window_mgr.update_value(key='-RESPONSE_TEXT_NUMBER-',value=self.response_text_number_display)
        self.update_output(output_iteration=0)
        
    def get_output_display_numbers(self):
        """
        Retrieves the actual and display numbers of the current output for navigation purposes.
        """
        self.response_text_number_display = int(self.window_mgr.get_from_value('-RESPONSE_TEXT_NUMBER-'))
        self.response_text_number_actual = self.response_text_number_display-1
        
    def determine_output_display(self,event):
        """
        Determines the output to display based on the navigation event.

        Args:
            event: The navigation event that occurred
        """
        self.get_output_display_numbers()
        if self.event == '-RESPONSE_TEXT_BACK-':
            if self.response_text_number_actual >0:
                self.adjust_output_display(-1)
        elif self.event == '-RESPONSE_TEXT_FORWARD-':
            if self.response_text_number_display < len(self.latest_output):
                self.adjust_output_display(1)
                
    def update_output(self,output_iteration):
        """
        Updates the displayed output based on the given iteration.

        Args:
            output_iteration (int): The index of the output to display.
        """
        if output_iteration < len(self.latest_output) and output_iteration >=0:
            self.current_output = self.latest_output[output_iteration]
            self.update_text_with_responses()
            
    def adjust_output_display(self,num):
        self.response_text_number_actual+=num
        self.response_text_number_display+=num
        self.update_output(output_iteration=self.response_text_number_actual)
        self.window_mgr.update_value(key='-RESPONSE_TEXT_NUMBER-',value=self.response_text_number_display)
        
    ##collate responses in the responses file list 
    def response_event_check(self):
        """
        Checks if a response event has been triggered.

        A response event is triggered when a user interacts with the response management interface.

        Returns:
            bool: True if a response event has been triggered, otherwise False
        """
        if self.event == "-COLLATE_RESPONSES_BOOL-":
            if self.window_mgr.get_values()["-COLLATE_RESPONSES_BOOL-"]:
                files_list = self.window['-FILES_LIST_RESPONSES-'].Values
                if len(files_list)>0:
                    collator = FileCollator(files_list)
                    collated_responses=collator.get_gollated_responses(files_list,key_value = 'query_response')
                    self.window_mgr.update_value('-FILE_TEXT_RESPONSES-',collated_responses)
                    
        elif self.event in ['-RESPONSE_TEXT_BACK-','-RESPONSE_TEXT_FORWARD-']:
            self.determine_output_display(self.event)
            
        elif self.event == 'Copy Response':
            active_tab_key = self.window_mgr.get_values()['-TABS-']  # get active tab key
            # Construct the key for multiline text box
            multiline_key = active_tab_key.replace('TAB','TEXT')
            if multiline_key in self.window_mgr.get_values():
                text_to_copy = self.window_mgr.get_values()['-FILE_TEXT-']
                pyperclip.copy(text_to_copy)
        else:
            return False
        return True
    
    def readme_event_check(self):
        """
        Checks if the Generate README event has been triggered.

        The Generate README event is triggered when a user opts to generate a README file for the prompt.

        Returns:
            bool: True if the Generate README event has been triggered, otherwise False
        """
        if self.event=="-GENERATE_README-":
            files_list = self.window['-FILES_LIST_FILES-'].Values
            result,files_list=read_me_window(files_list)
            data = ''
            for file_path in files_list:
                if os.path.isfile(file_path):
                    file_contents = read_from_file(file_path)
                    self.chunk_title= os.path.basename(file_path)
                    data+=self.add_to_chunk(file_contents)
            self.chunk_type="CODE"
            self.update_prompt_mgr(prompt_data=data)
            self.window_mgr.append_output('-REQUEST-',result)
        else:
            return False
        return True
    
    
    def browser_event_query(self,values=None,event=None,window=None):
        values=None or self.window_mgr.get_values()
        event=None or self.window_mgr.get_event()
        window=None or self.window
        self.browser_mgr.handle_event(self,values,event,window)
    @staticmethod
    def get_remainder(num):
        return 100-int(num)
    
    @staticmethod
    def get_new_line(num=1):
        new_line = ''
        for i in range(num):
            new_line +='\n'
        return new_line
    #text and bool handling
    @staticmethod
    def get_bool_and_text_keys(key_list,sections_list=[]):
        keys = []
        for text in key_list:
            keys.append(text_to_key(text))
            for section in sections_list:
                keys.append(text_to_key(text,section=section))
        return keys

    def perform_event_checks(self):
        """
        Iterates through the different event checks to see if any has been triggered.

        The function stops checking once an event has been triggered.
        """
        for event_check in self.event_check_keys:
            # Use getattr to get the method by name, then call it
            method = getattr(self, event_check)
            self.bool_loop = method()
            # If you want to stop checking once bool_loop is True (or some condition), you can break here
            if self.bool_loop:  # Assuming self.bool_loop should stop the loop when True
                break
        self.loop_one=True
## while loop
    def while_window(self,event,values,window):
        self.event,self.values,window=event,values,window
        if self.loop_one == False:
            self.update_all()
            for browser_event in ['-SCAN_FILES-',
                                  '-SCAN_RESPONSES-']:
                self.browser_event_query(self.values,browser_event,self.window)
        self.next_read_mgr.execute_queue()
        self.script_event_js = get_event_key_js(event = self.event,key_list=self.additions_key_list)
        self.perform_event_checks()
