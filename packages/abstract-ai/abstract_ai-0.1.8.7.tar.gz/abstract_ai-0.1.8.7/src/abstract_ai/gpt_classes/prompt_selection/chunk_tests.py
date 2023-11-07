from abstract_gui import AbstractWindowManager
from PromtBuilder import *
from abstract_ai import ModelManager,InstructionManager

prompt_mgr = PromptManager(dist_number=None,
              bot_notation=None,
              generate_title=None,
              chunk_descriptions=None,
              request_chunks=None,
              prompt_as_previous=None,
              token_adjustment=None)

prompt_mgr.create_prompt
calculate_token_distribution(
 role='assistant',
 completion_percentage=40,
 prompt_data=None,
 request=None,
 token_dist=None,
 bot_notation=None,
 chunk=None,
 chunk_type=None)

