from abstract import BCFerriesAbstractObject
import dateutil.parser, time

class BCFerriesScheduledCrossing(BCFerriesAbstractObject):
  def __init__(self, name, sailing_time, time_row):
    self.name = name
    self.sailing_time = sailing_time
    scheduled_dep, actual_dep, arrival, self.status, _ = [x.text for x in time_row]
    self.scheduled_departure = dateutil.parser.parse(scheduled_dep) if scheduled_dep else None
    self.actual_departure = dateutil.parser.parse(actual_dep) if actual_dep else None
    self.arrival = dateutil.parser.parse(arrival) if arrival else None

  def is_early(self):
    return (self.actual_departure or self.scheduled_departure) < self.scheduled_departure

  def is_late(self):
    return (self.actual_departure or self.scheduled_departure) > self.scheduled_departure

  def is_departed(self):
    return (self.actual_departure or self.scheduled_departure) >= time.now()
