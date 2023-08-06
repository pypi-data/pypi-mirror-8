# Note: This README is saved as a txt file but could be run as
# python code if it would help you learn about the package.

from Logger import *
from enum import Enum

### Documentation - Logger ###

# Create a new logger
#  The first argument, False:
#  This specifies if new logs should be automatically printed
#
#  The second argument, "LOG START"
#  This is the header; the first line to be printed to the log
#
#  The third optional argument (not shown here)
#  This specifies how the time is rendered by the logger
#  This should be a string, and can contain the following
#  %y - Year; %m - Month; %d - Day;
#  %H - Hour; %M - Minute; %S - Second;

logger = Logger(False, "LOG START")

# Add a log to the logger
#  The arguments specify the type of log and the text to be logged
#  More Log Types can be added in a new Enum.

logger.log(LogType.INFO, "Command Parsed")


## Main Methods

# This prints all new logs and moves the pointer forward to the current one
#  New refers to any logs since the last time the logs were read
#  The position of New in the list is held by a pointer variable
#  The position of the pointer is not changed by autoprint

logger.printNew()

# This method prints everything regardless of the pointer position

logger.printAll()


## Pointer Methods

# Sets Pointer to 0 - the start of the log
logger.setPointerToStart()

# Sets the Pointer to the end of the log
logger.setPointerToEnd()

# Gets the Pointer value
logger.getPointer()

# Sets the Pointer value
#  If the argument is < 0 it becomes zero
#  If the argument is > log length it becomes log length
logger.setPointer(3)

# Adds to the Pointer
#  Prevents Illegal Values
logger.incrementPointer() # Adds 1 by default
logger.incrementPointer(3)# Optional Argument

# Takes from the Pointer
#  Prevents Illegal Values
logger.decrementPointer() # Takes 1 by default
logger.decrementPointer(3)# Optional Argument


## Misc. Methods

# Gets new values and returns as list
#  Moves Pointer forward
logger.getNew()

# Gets all values and returns as list
logger.getAll()


## Use of a custom Enum for additional log values

# New Enum to be used with additional values to the normal Enum
#  Underscores are replaced with spaces when the message is formatted
class DisasterType(Enum):
    OH_CRAP = 0
    OVERHEATING_CORE = 1

# Create a log with the new Enum Type as an argument
logger.log(DisasterType.OH_CRAP, "Critical Error: Shutting Down Reactor Core")


## Final Print

print("\n All Logs added \n")

# Printing all the logs
logger.printAll()
