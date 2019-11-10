
class Strings:

    menu = """
Break Queue Commands

/break 30 - Queue a 30 minute break
/break 5 - Queue a 5 minute break

/break lunch - Queue a 30 minute break
/break brb - Queue a 5 minute break

/break end - Remove yourself from the queue
/break status - List the active break queue

/break history - List the commands ran in the last 12 hours
/break log - List a verbose log of what the queue did in the last hour

/break settings - List the break queue global settings
/break settings option_name - List a specific break queue global setting
/break settings option_name option_value - Set a specific break queue setting to a new value

/break add @employee minutes - Add an employee to the queue manually
/break remove @employee - Remove an employee from the queue
/break push @employee - Push an employee from queued to cleared

/break help - This menu

Aliases:

lunch: lunch, bye, lnch, unch, food, eats, hungry, tacos, munch, munching, munchin, kcmunchkin
brb: brb, out, now, please, pls, plz, plox, coffee
end: end, hi, clear, en, ed, adios, back, bacl, thanks, edn, nde, ned, tanks, ermahgerd, nd
help: help, -h, -help, --h, --help, h
push: push, send, clear, gogogo
add: add, create
remove: remove, unpush, pull
settings: settings, setting, option, options


Short Commands:

/lunch - Queue a 30 minute break
/brb - Queue a 5 minute break
/end - Remove yourself from the queue
/back - Remove yourself from the queue    
    """


string_instance = Strings()
