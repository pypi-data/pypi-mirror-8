===============
logstashHandler
===============

logstashHandler is a basic logging handler for sending to a logstash instance via UDP or TCP encoded as json.


Basic usage
===========

Setup an input on the relevant logstash server::

  input {
    udp {
      port => 12345
      codec => json
    }
  }

Setup handler and ship logs::

  python
  from logstashHandler import logstashHandler

  lhandler = logstashHandler(host='mylogserver.example.com',port=12345,proto='UDP')
  logger.addHandler(lhandler)
  logger.warn("Something went wrong")


To send additional fields to logstash, use the keyword extra and send a dict starting with extraFields::

    logger.warn('DANGER DANGER',extra={'extraFields':{'name':'W. Robinsson', 'planet':'Unkown'}})


The default level field name and individual level names can be overridden as so::

   levels = {'ERROR': 3, 'WARNING': 2, 'INFO': 1, 'DEBUG': 0}
   lhandler = logstashHandler(
       host='mylogserver.example.com', 
       port=12345,proto='UDP',
       levels=levels,
       levelLabel='severity'
   )



More info can be found on the github page.
