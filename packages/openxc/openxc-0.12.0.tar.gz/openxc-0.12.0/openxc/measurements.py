"""Vehicle data measurement types pre-defined in OpenXC."""
import numbers
import sys
import inspect

import openxc.units as units
from .utils import Range, AgingData

try:
    unicode
except NameError:
    # Python 3
    basestring = unicode = str


def all_measurements():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and Measurement in obj.mro() and hasattr(
                obj, 'name'):
            yield obj


class Measurement(AgingData):
    """The Measurement is the base type of all values read from an OpenXC
    vehicle interface. All values encapsulated in a Measurement have an
    associated scalar unit (e.g. meters, degrees, etc) to avoid crashing a rover
    into Mars.
    """
    name = 'generic'
    DATA_TYPE = numbers.Number
    _measurement_map = {}
    unit = units.Undefined

    def __init__(self, name, value, event=None, override_unit=False, **kwargs):
        """Construct a new Measurement with the given name and value.

        Args:
            name (str):  The Measurement's generic name in OpenXC.
            value (str, float, or bool): The Measurement's value.

        Kwargs:
           event (str, bool): An optional event for compound Measurements.
           override_unit (bool): The value will be coerced to the correct units
               if it is a plain number.

        Raises:
            UnrecognizedMeasurementError if the value is not the correct units,
            e.g. if it's a string and we're expecting a numerical value
        """
        super(Measurement, self).__init__()
        self.name = name
        if (not isinstance(value, bool) and isinstance(value, numbers.Number)
                and override_unit):
            value = self.unit(value)
        self.value = value
        self.event = event

    def __repr__(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        """Set the value of this measurement.

        Raises:
            AttributeError: if the new value isn't of the correct units.
        """
        if self.unit != units.Undefined and new_value.unit != self.unit:
            raise AttributeError("%s must be in %s" % (
                self.__class__, self.unit))
        self._value = new_value

    @classmethod
    def from_dict(cls, data):
        """Create a new Measurement subclass instance using the given dict.

        If Measurement.name_from_class was previously called with this data's
        associated Measurement sub-class in Python, the returned object will be
        an instance of that sub-class. If the measurement name in ``data`` is
        unrecognized, the returned object will be of the generic ``Measurement``
        type.

        Args:
            data (dict): the data for the new measurement, including at least a
                name and value.
        """

        args = []

        if 'id' in data and 'data' in data:
            measurement_class = CanMessage
            args.append("Bus %s: 0x%x" % (data.get('bus', '?'), data['id']))
            args.append(data['data'])
            # TODO grab bus
        else:
            measurement_class = cls._class_from_name(data['name'])
            if measurement_class == Measurement:
                args.append(data['name'])
            args.append(data['value'])

        return measurement_class(*args, event=data.get('event', None),
                override_unit=True)

    @classmethod
    def name_from_class(cls, measurement_class):
        """For a given measurement class, return its generic name.

        The given class is expected to have a ``name`` attribute, otherwise this
        function will raise an execption. The point of using this method instead
        of just trying to grab that attribute in the application is to cache
        measurement name to class mappings for future use.

        Returns:
            the generic OpenXC name for a measurement class.

        Raise:
            UnrecognizedMeasurementError: if the class does not have a valid
                generic name
        """
        if not getattr(cls, '_measurements_initialized', False):
            cls._measurement_map = dict((m.name, m) for m in all_measurements())
            cls._measurements_initialized = True

        try:
            name = getattr(measurement_class, 'name')
        except AttributeError:
            raise UnrecognizedMeasurementError("No 'name' attribute in %s" %
                    measurement_class)
        else:
            cls._measurement_map[name] = measurement_class
            return name

    @classmethod
    def _class_from_name(cls, measurement_name):
        return cls._measurement_map.get(measurement_name, Measurement)


class NamedMeasurement(Measurement):
    """A NamedMeasurement has a class-level ``name`` variable and thus the
    ``name`` argument is not required in its constructor.
    """
    def __init__(self, value, **kwargs):
        super(NamedMeasurement, self).__init__(self.name, value, **kwargs)


class NumericMeasurement(NamedMeasurement):
    """A NumericMeasurement must have a numeric value and thus a valid range of
    acceptable values.
    """
    valid_range = None

    def percentage_within_range(self):
        return ((self.value.num - self.valid_range.min) /
                float(self.valid_range.spread)) * 100

    def within_range(self):
        return self.valid_range.within_range(self.value.num)


class StatefulMeasurement(NamedMeasurement):
    """Must have a class-level ``states`` member that defines a set of valid
    string states for this measurement's value.
    """
    DATA_TYPE = unicode
    states = None

    def valid_state(self):
        """Determine if the current state is valid, given the class' ``state``
        member.

        Returns:
            True if the value is a valid state.
        """
        return self.states is not None and self.value in self.states


class BooleanMeasurement(NamedMeasurement):
    DATA_TYPE = bool


class EventedMeasurement(StatefulMeasurement):
    DATA_TYPE = unicode


class PercentageMeasurement(NumericMeasurement):
    valid_range = Range(0, 100)
    unit = units.Percentage


class AcceleratorPedalPosition(PercentageMeasurement):
    name = "accelerator_pedal_position"

class FuelLevel(PercentageMeasurement):
    name = "fuel_level"


class VehicleSpeed(NumericMeasurement):
    name = "vehicle_speed"
    valid_range = Range(0, 321)
    unit = units.KilometersPerHour

class EngineSpeed(NumericMeasurement):
    name = "engine_speed"
    valid_range = Range(0, 8000)
    unit = units.RotationsPerMinute

class FuelConsumed(NumericMeasurement):
    name = "fuel_consumed_since_restart"
    valid_range = Range(0, 100)
    unit = units.Litre

class Latitude(NumericMeasurement):
    name = "latitude"
    valid_range = Range(-90, 90)
    unit = units.Degree

class Longitude(NumericMeasurement):
    name = "longitude"
    valid_range = Range(-180, 180)
    unit = units.Degree

class Odometer(NumericMeasurement):
    name = "odometer"
    valid_range = Range(0, 1000000)
    unit = units.Kilometer

class SteeringWheelAngle(NumericMeasurement):
    name = "steering_wheel_angle"
    valid_range = Range(-600, 600)
    unit = units.Degree

class TorqueAtTransmission(NumericMeasurement):
    name = "torque_at_transmission"
    valid_range = Range(-800, 1500)
    unit = units.NewtonMeter

class LateralAcceleration(NumericMeasurement):
    name = "lateral_acceleration"
    valid_range = Range(-5, 5)
    unit = units.MetersPerSecondSquared

class LongitudinalAcceleration(NumericMeasurement):
    name = "longitudinal_acceleration"
    valid_range = Range(-5, 5)
    unit = units.MetersPerSecondSquared


class BrakePedalStatus(BooleanMeasurement):
    name = "brake_pedal_status"

class HeadlampStatus(BooleanMeasurement):
    name = "headlamp_status"

class HighBeamStatus(BooleanMeasurement):
    name = "high_beam_status"

class ParkingBrakeStatus(BooleanMeasurement):
    name = "parking_brake_status"

class WindshieldWiperStatus(BooleanMeasurement):
    name = "windshield_wiper_status"


class IgnitionStatus(StatefulMeasurement):
    name = "ignition_status"
    states = ['off', 'accessory', 'run', 'start']

class TransmissionGearPosition(StatefulMeasurement):
    name = "transmission_gear_position"
    states = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh',
            'eighth', 'neutral', 'reverse', 'park']

class TurnSignalStatus(StatefulMeasurement):
    name = "turn_signal_status"


class ButtonEvent(EventedMeasurement):
    name = "button_event"
    states = ['up', 'down', 'left', 'right', 'ok']

class DoorStatus(EventedMeasurement):
    name = "door_status"
    states = ['driver', 'rear_left', 'rear_right', 'passenger']


class CanMessage(Measurement):
    name = 'can_message'


class UnrecognizedMeasurementError(Exception):
    pass


