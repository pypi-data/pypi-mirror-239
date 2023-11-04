class InstructionManager:
    def __init__(self,notation=True,suggestions=True,abort=True,generate_title=True,additional_responses=True,additional_instruction=False,test_it=False,request_chunks=False):
        self.notation=notation
        self.suggestions=suggestions
        self.abort=abort
        self.generate_title=generate_title
        self.additional_instruction=additional_instruction
        self.additional_responses=additional_responses
        self.request_chunks=request_chunks
        self.test_it=test_it
        self.instructions_js = {}
        self.initialize_instructions()
        self.instructions=self.get_instructions()
    def get_additional_responses(self):
        """
        Determines the additional response based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the response is determined.
            
        Returns:
            str: The determined response.
        """
        if isinstance(self.additional_responses,str):
            return self.additional_responses
        if self.additional_responses:
            return "This parameter, usually set to True when the answer cannot be fully covered within the current token limit, initiates a loop that continues to send the current chunk's prompt until the module returns a False value. This option also enables a module to have access to previous notations"
        return "return false"
    def get_generate_title(self):
        """
        Retrieves the notation based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the notation is determined.
            
        Returns:
            str: The determined notation.
        """
        if isinstance(self.generate_title,str):
            return self.generate_title
        if self.generate_title:
            return 'A parameter used for title generation of the chat. To maintain continuity, the generated title for a given sequence is shared with subsequent queries.'
        return "return false"
    def get_notation(self):
        """
        Retrieves the notation based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the notation is determined.
            
        Returns:
            str: The determined notation.
        """
        if isinstance(self.notation,str):
            return self.notation
        if self.notation:
            return "A useful parameter that allows a module to retain context and continuity of the prompts. These notations can be used to preserve relevant information or context that should be carried over to subsequent prompts."
        return "return false"
    def get_suggestions(self):
        """
        Retrieves the suggestions based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the suggestion is determined.
            
        Returns:
            str: The determined suggestions.
        """
        if isinstance(self.suggestions,str):
            return self.suggestions
        if self.suggestions:
            return "': A parameter that allows the module to provide suggestions for improving efficiency in future prompt sequences. These suggestions will be reviewed by the user after the entire prompt sequence is fulfilled."
        return "return false"
    def get_abort(self):
        """
        Retrieves the abort based on the input value.
        
        Args:
            bool_value (bool or str): Input value based on which the abort is determined.
            
        Returns:
            str: The determined abort.
        """
        if isinstance(self.abort,str):
            return self.abort
        if self.abort:
            return "if you cannot fullfil the request, return this value True; be sure to leave a notation detailing whythis was"
        return "return false"


    def get_request_chunks(self):
        if self.request_chunks:
            return "you may request that the previous chunk data be prompted again, if selected, the query itterate once more with the previous chunk included in the prompt. return this value as True to impliment this option; leave sufficient notation as to why this was neccisary for the module recieving the next prompt"
        return "return false"
    def initialize_instructions(self):
        self.example_format={}
        self.instructions_js = {}
        if 'response' not in self.instructions_js and "api_response" not in self.instructions_js:
            self.instructions_js["api_response"]="place response to prompt here"
            self.example_format["api_response"]=""
        if self.notation or self.test_it:
           self.instructions_js["notation"]=self.get_notation()
           self.example_format["notation"]=""
        if self.instructions_js or self.test_it:
            self.instructions_js["suggestions"]=self.get_suggestions()
            self.example_format["suggestions"]=""
        if self.additional_responses or self.test_it:
            self.instructions_js["additional_responses"]=self.get_additional_responses()
            self.example_format["additional_responses"]=False
        if self.abort or self.test_it:
            self.instructions_js["abort"]=self.get_abort()
            self.example_format["abort"]=False
        if self.generate_title or self.test_it:
            self.instructions_js["generate_title"]= self.get_generate_title()
            self.example_format["generate_title"]=""
        if self.request_chunks or self.test_it:
            self.instructions_js["request_chunks"]= self.get_request_chunks()
            self.example_format["request_chunks"]=False
        if self.additional_instruction or self.test_it:
            self.instructions_js["additional_instruction"]= self.additional_instruction
            self.example_format["additional_instruction"]="..."
        return self.instructions_js
    def get_instructions(self,instructions_js=None):
        """
        Retrieves instructions for the conversation.

        Returns:
            None
        """
        if instructions_js == None:
            instructions_js = self.initialize_instructions()
        instructions = "your response is expected to be in JSON format with the keys as follows:\n"
        if self.test_it:
            instructions += 'this query is a test, please place a test response in every key\n'
        instructions += '\n'
        for i,key in enumerate(instructions_js.keys()):
            instructions+=f"{i}) {key} - {instructions_js[key]}\n"
        instructions += '\nbelow is an example of the expected json dictionary response format, with the default inputs:\n' + str(self.example_format)
        return instructions
