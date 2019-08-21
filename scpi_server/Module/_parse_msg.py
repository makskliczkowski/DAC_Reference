# Functions that will parse information, contain current path, include message to be sent back, request will
# be proceeded after receiving value that user wants from us. The message will be provided in ASCI format.
import Lib

__methods__ = []
register_method = Lib.register_method(__methods__)


@register_method
def msg_parse_info(self):
    # to allow memory of current path we will save a string path and every time when we go to other path we
    # wil change the dictionary with inner functions from common or parser, thanks to that we don't need to
    # worry about getting in other dictionaries!
    self.current_branch = ""
    self.request = ""  # current request
    self.request_val = "0"  # current request value
    self.expect_request = False  # we will make functions in dictionary expect request

    self.terminator = '\n'
    self.command_separator = ';'
    # A semicolon separates two commands in the same message without changing
    # the current path.
    self.path_separator = ':'
    # When a colon is between two command keywords, it moves the current path down
    # one level in the command tree.
    self.parameters_separator = ','
    self.query = '?'


@register_method
def clear_path(self):
    self.current_branch = ""
    self.message = ""
    self.curr_dic_short = self.root_short
    self.curr_dic_long = self.root_long


@register_method
def find_path(self, path_temp):
    # we now check for instance of the path in the dictionary
    # we now check for instance of the path in the dictionary
    path = ''
    path = path.join(path_temp).upper()
    err_short = self.curr_dic_short.get(path)
    if err_short is not None:
        err_short()
    err_long = self.curr_dic_long.get(path)
    if err_long is not None:
        err_long()
    # ADD ERRRRORRORORORORR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    error = err_long == -1 and err_short == -1
    if error:
        self.response = "Wrong path, problem with: (No such directory) - " + str(path_temp) + "Try again\n"
        self.message = ""
    return error


@register_method
def find_in_common(self, path_temp):
    path = ''
    path = path.join(path_temp).upper()
    error = self.common.get(path)
    if error is None:
        self.response = "Wrong path, problem with: (No such directory) - " + str(path_temp) + "Try again\n"
        self.message = ""
    else:
        error()
    return error


# we define request sending function as it may be finishing command
@register_method
def request_sending(self, path_temp):
    self.request_val = path_temp
    path_temp.pop()
    error = self.find_path(self.request)  # now we can execute function from request
    self.request_val = ""
    self.request = ""
    if error:
        self.response = "Wrong path, problem with: (No such directory) - " + str(path_temp) + "Try again\n"
        self.message = ""
    return error


# three finishing commands are possible
#   -change the path
#   -request handle
#   -common request
@register_method
def msg_handle(self, msg):
    self.message = msg
    temp = list(str(self.message))
    self.message = ""
    if temp[0] == self.path_separator and self.current_branch == "":
        del temp[0]
        # we are at the root branch
    elif temp[0] == self.path_separator and not self.current_branch == "":
        self.response = "Can't access you path " + msg + ". Can't use : at the beginning. Try again\n"
        self.message = ""
        return
        # Later add error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # now we iterate on requested path
    path_temp = list()
    # our possibilities are:
    #   -terminator - finishes sentence and clears path
    #   -finish of temp - finishes sentence and leaves path
    #   -white space - can be omitted after : or ; or can mean that we wait for the request
    #   -: - we know that we need to change path
    #   -; - we start a new command either by resetting path with ;: or in the same directory
    for i in range(len(temp)):
        path_temp.append(temp[i])
        # terminator clears the path!
        if temp[i] == self.terminator:
            if self.expect_request:
                error = self.request_sending(path_temp)
                if error == -1:
                    return -1
            else:
                error = self.find_in_common(path_temp)
                if error == -1:
                    return -1
            error = 0
            return error  # 0 is returned when no error occurred!
        # if we get ; we pop it back, check for request and if no request needed then check in common
        # as it hasn't been already executed before, we just check if it's a command without parameters
        if temp[i] == self.command_separator:
            path_temp.pop()
            if self.expect_request:
                error = self.request_sending(path_temp)
                if error == -1:
                    return -1
            else:
                error = self.find_in_common(path_temp)
                if error == -1:
                    return -1
            path_temp = []
            continue
        # if we get :
        if temp[i] == self.path_separator:
            if temp[i - 1] == self.command_separator:
                # if we have combination ;: we need to clear path
                self.clear_path()
                path_temp = []
                continue
            path_temp.pop()  # remove : from the end
            error = self.find_path(path_temp)
            if error == -1:
                return -1
            str_path = ''
            str_path = str_path.join(path_temp)
            self.current_branch = self.current_branch + ":" + str_path
            path_temp = []
            continue
        # <WSP> handling and request processing
        if temp[i] == " " and (temp[i - 1] == self.path_separator or temp[i - 1] == self.command_separator):
            # ignore whitespaces after : or ;
            path_temp.pop()
            continue
        if temp[i] == " " and (temp[i - 1] != self.path_separator or temp[i - 1] != self.command_separator):
            # whitespace after command makes expecting response
            path_temp.pop()
            self.request = path_temp
            self.expect_request = True # we are waiting for request value before getting it done
            path_temp = []
            continue


@register_method
def space_handle(self):
    temp = list(self.request_val)
    for i in range(len(temp)):
        if temp[i] == " ":
            del temp[i]
    self.request_val = temp
    return
