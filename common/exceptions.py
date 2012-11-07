# Copyright 2012 WebMark committers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Exceptions that may happen in all the webmark code."""
class WebMarkException(Exception):
    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message: %s " % repr(self.msg)
        if self.screen is not None:
            exception_msg = "%s; Screenshot: available via screen " \
                % exception_msg
        if self.stacktrace is not None:
            exception_msg = "%s; Stacktrace: %s " \
                % (exception_msg, str(self.stacktrace))
        return exception_msg