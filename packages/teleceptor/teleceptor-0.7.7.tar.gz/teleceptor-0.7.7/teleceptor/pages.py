"""
    (c) 2014 Visgence, Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

# System Imports
import os,sys
import json
import cherrypy
import jinja2

#local Imports
from teleceptor import TEMPLATES
from teleceptor import api
from teleceptor.api import ResourceApi
from teleceptor.auth import AuthController, require, member_of, name_is
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=TEMPLATES))

class Root(object):
    auth = AuthController()
    api  = ResourceApi()

    @require()
    def index(self,sensor_id=None, *args, **kwargs):
        params = cherrypy.request.params

        sensors = api.Sensors()
        datastreams = api.DataStreams()
        sysdata = api.SysData()
        sysdata_dict = json.loads(sysdata.GET())

        sensorsList = json.loads(sensors.GET())['sensors']
        activeSensor = sensorsList[0] if len(sensorsList) > 0 else None

        if sensor_id is not None:
            try:
                activeSensor = json.loads(sensors.GET(sensor_id))["sensor"]
            except KeyError, ke:
                print "Error: no sensor with id %s", sensor_id
                print ke

        datastream = None
        if activeSensor is not None:
            dsList = json.loads(datastreams.GET(None, **{"sensor": activeSensor['uuid']}))
            datastream = dsList['datastreams'][0] if len(dsList['datastreams']) > 0 else None

        cherrypy.response.headers['Content-Type'] = 'text/html'

        returnData = {
            "sysdata":sysdata_dict,
            "sensorsList": sensorsList,
            "activeSensor": activeSensor,
            "activeSensorJSON": json.dumps(activeSensor),
            "datastreamJSON": json.dumps(datastream),
        }
        returnData.update(**kwargs);

        t = env.get_template("sensorsIndex.html")
        return t.render(returnData)

    index.exposed = True


    @require()
    def generateJson(self,**kwargs):
        t = env.get_template("generateJson.html")
        sysdata = api.SysData()
        sysdata_dict = json.loads(sysdata.GET())

        cherrypy.response.headers['Content-Type'] = 'text/html'
        return t.render({"sysdata":sysdata_dict})
        
    generateJson.exposed = True
        
        
    