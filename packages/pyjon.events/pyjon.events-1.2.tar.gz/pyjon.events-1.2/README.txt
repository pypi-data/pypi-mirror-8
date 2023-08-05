What is it ?
============

Pyjon.Events is an easy-to-use event dispatcher metaclass for your objects :
Just add it to any of your class, and you can add event listeners and dispatch events.

You can define arguments passed to your listener when you add it.
You can also define argument passed to the listener when emiting an event.

Example
=======

For our example, we will define a person class.
Just import the module, and add it to your class (Python2 example)::

    from pyjon.events import EventDispatcher
    
    class Person(object):
        __metaclass__ = EventDispatcher
        
        def __init__(self, name):
            # just a sample initialization, you can do whatever you want, of course.
            self.name = name
            
        def run(self, meters=1):
            print "I'm running for %d meters !" % meters
            self.emit_event('ran', meters)
            self.emit_event('moved', meters=meters)
            
        def walk(self, meters=1):
            print "I'm walking for %d meters !" % meters
            self.emit_event('walked', meters)
            self.emit_event('moved', meters=meters)
        
        def sleep(self):
            print "sleeping..."
            self.emit_event('sleeping')
            time.sleep(5)
            self.emit_event('sleeped')
            print "Wow... had a good night !"

For Python3, just replace this::

    class Person(object):
        __metaclass__ = EventDispatcher

with this::

    class Person(metaclass = EventDispatcher):
    
Now, let's instanciate our class and subscribe to events::
    
    >>> henry = Person('henry')
    
    >>> def handle_movement(meters=None):
    ...     print "he moved for %d meters" % meters
        
    >>> def handle_person_movement(who, meters=None):
    ...     print "%s moved for %d meters" % (who, meters)
    
    >>> henry.add_listener('moved', handle_movement)
    
    >>> henry.add_listener('moved', handle_person_movement, "henry")
    
    >>> henry.walk(5)
    I'm walking for 5 meters !
    he moved for 5 meters
    henry moved for 5 meters
        
    >>> def handle_advanced_movement(meters, who, movement_type):
    ...     print "%s %s for %d meters" % (who, movement_type, meters)
    
    >>> henry.add_listener('walked', handle_advanced_movement, "henry", "walked")
    
    >>> henry.add_listener('ran', handle_advanced_movement, "henry", "ran")
    
    >>> henry.walk(5)
    I'm walking for 5 meters !
    henry walked for 5 meters
    he moved for 5 meters
    henry moved for 5 meters
    
    >>> henry.run(5)
    I'm running for 5 meters !
    henry ran for 5 meters
    he moved for 5 meters
    henry moved for 5 meters
    
That's simple isn't it ?
        
