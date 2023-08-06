#!/usr/bin/env python
#
# Copyright 2011 Rodrigo Ancavil del Pino
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
from tornadows import soaphandler
from tornadows import webservices
from tornadows import xmltypes
from tornadows.soaphandler import webservice

class CurrentTempService(soaphandler.SoapHandler):
     """ Service that return the current temperature, not uses input parameters """
     @webservice(_params=None,_returns=xmltypes.Integer)
     def getCurrentTemperature(self):
          c = 29
          return c

if __name__ == '__main__':
     service = [('CurrentTempService',CurrentTempService)]
     app = webservices.WebService(service)
     ws  = tornado.httpserver.HTTPServer(app)
     ws.listen(8080)
     tornado.ioloop.IOLoop.instance().start()
