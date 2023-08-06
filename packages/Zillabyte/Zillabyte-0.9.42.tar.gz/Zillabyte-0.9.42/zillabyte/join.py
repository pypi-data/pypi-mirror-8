# OPERATION Join
# PYTHON_SYNTAX 
#   lhs_stream.join_with( 
#     name = "name",                                                   # optional
#     stream = rhs_stream_object,
#     fields = "join_field" OR ["lhs_join_field", "rhs_join_field"],
#     emits = "stream",                                                # optional
#     options = {options} 
#   )
# PYTHON_NOTES 
# A "join" may only emit a single stream.
# 
# The following options can be used in a join:
# 
# Mandatory:
# 
#  * **"fields"** : specifies the fields to join on. The value must be a STRING or a length-2 ARRAY. If value = a STRING, the LH and RH join fields will both be set to this STRING. If value = a length-2 ARRAY, the LH join field will be set to array[0] and the RH join field will be set to array[1].
# 
# Optional:
#
#  * **"type"** : specifies the join type. The default is "left". Options are ["inner", "outer", "left", "right"]
#  * **"emits"** : specifies the stream to emit. A "join" may only emit a single stream.
# 
# PYTHON_EXAMPLE 
#  
# word_stream = employee_stream.join_with(\
#   name = "join",\
#   stream = budget_stream,\
#   fields = ["occupation", "number"],\
#   options = {"type" : "left"}\
# )
from counter import Counter
from helper import Helper
class Join:
  def __init__(self, app):
    self._app = app

  def build_node(self, name, lhs_stream, rhs_stream, emits, fields, options):
    self._name = name if name else "join_"+Counter.get()
    self._type = "join"
    self._lhs_stream = lhs_stream._name
    self._rhs_stream = rhs_stream._name

    if emits == None:
      emits = ["stream_"+Counter.get()]
    elif isinstance(emits, basestring):
      emits = [emits]
    self._emits = emits

    if fields:
      if isinstance(fields, list) and len(fields) == 2:
        self._lhs_fields = fields[0]
        self._rhs_fields = fields[1]
      elif isinstance(fields, basestring):
        self._lhs_fields = fields
        self._rhs_fields = fields

    self._join_type = "inner"
    if options:
      if options["type"]:
        self._join_type = options["type"]

    Helper.check_name("join", self._name, self._app._names)
    Helper.check_join(self)
    Helper.check_emits("join", self._emits, self._app._streams)

  def run_operation(self):
    print "Joins can only be instantiated on our cluster, sorry!"
