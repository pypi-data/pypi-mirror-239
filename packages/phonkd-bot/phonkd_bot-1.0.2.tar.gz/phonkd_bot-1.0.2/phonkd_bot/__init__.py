"""
This class acts as the front end to the user. I seperated it from the main class to prevent the user
from seeing internal methods that may be confusing
"""

# external imports
from collections.abc import Callable
from traceback import extract_stack, format_list
from inspect import signature, currentframe
from discord import Message as message
from asyncio import run

# local import
from .api_handler import DiscordAPIHandler

api_handler = DiscordAPIHandler()
logger = api_handler.logger

def start() -> None:
    """
    Tells the framework to connect to the server, this method takes no parameters.
    """
    if not "on_message" in api_handler.client.callables.keys():
        logger.warning("The 'call_on_message' method has not been set.")

    run(api_handler.main())

def call_on_message(function: Callable[[message], str]) -> None:
    """
    Tells the framework what function to call when it receives a message.
    The framework will pass a discord message object when it invokes the function.
    Find out more regarding the discord message object here:
    https://discordpy.readthedocs.io/en/stable/api.html#discord.Message
    """

    try:
        # check if the object passed is a function
        if not callable(function):
            raise ValueError(f"Failed to set function: `{function}`, make sure that it is a callable object.")
        
        # check if the function only has 1 parameter
        parameters = signature(function).parameters
        if len(parameters) != 1:
            raise ValueError(f"Invalid number of parameters set in function '{function.__name__}', please only specify one.")
        
        api_handler.client.callables["on_message"] = function
        
    except Exception as e:
        caller_frame = currentframe().f_back
        caller_traceback = extract_stack(caller_frame)
        traceback_info = "".join(format_list(caller_traceback))
        logger.error(f"Error setting 'call_on_message' function: {e}\n{traceback_info}")