from functools import wraps

# from guerrilla.device.router.mode import MODE
# from guerrilla.device.router import Commands
from guerrilla.logging import logger, COLOR


def log(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        command = args[0] if args else ""
        expect_string = kwargs.get("expect_string", "")
        name = self.name

        log_message = f"From {COLOR.magenta(name):<{10}}     {COLOR.red('sent command:')} {command}"
        if expect_string:
            log_message += f" {COLOR.yellow('expecting:')} {expect_string}"
        logger.info(log_message)

        result = f(self, *args, **kwargs)

        logger.info(
            f"From {COLOR.magenta(name):<{10}} {COLOR.green('received  output:')} {result}"
        )

        return result

    return decorated


# def mode(target_mode, additional_command=None):
#     def transition_mode(self, from_mode, to_mode):
#         match (to_mode, from_mode):
#             case (MODE.MAIN, MODE.CONFIG):
#                 self.run(Commands.SYSTEM.EXIT)
#             case (MODE.MAIN, MODE.CONFIG_IF):
#                 self.run(Commands.SYSTEM.EXIT)
#                 self.run(Commands.SYSTEM.EXIT)
#             case (MODE.CONFIG, MODE.MAIN):
#                 self.run(Commands.SYSTEM.CONFIGURE)
#             case (MODE.CONFIG, MODE.CONFIG_IF):
#                 self.run(Commands.SYSTEM.EXIT)
#             case (MODE.CONFIG_IF, MODE.MAIN):
#                 self.run(Commands.SYSTEM.CONFIGURE)
#                 if additional_command:
#                     self.run(additional_command)
#             case (MODE.CONFIG_IF, MODE.CONFIG):
#                 if additional_command:
#                     self.run(additional_command)
#             case _:
#                 pass  # Do nothing

#     def decorator(func):
#         @wraps(func)
#         def wrapper(self, *fargs, **fkwargs):
#             current_mode = self.check_mode()

#             # Transition to the target mode
#             transition_mode(self, current_mode, target_mode)

#             result = func(self, *fargs, **fkwargs)

#             # Return to the original mode
#             transition_mode(self, target_mode, current_mode)

#             return result

#         return wrapper

#     # Check if target_mode is 'config-if' and no additional_command is provided
#     if target_mode == MODE.CONFIG_IF and additional_command is None:
#         raise ValueError(
#             "For 'config-if' mode, an additional_command must be provided."
#         )

#     return decorator
