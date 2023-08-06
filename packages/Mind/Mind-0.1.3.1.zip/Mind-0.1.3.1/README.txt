Mind
=====
Library for games in Python
Mind.Knowledge:
	part of library for data saving.
	Mind.Knowledge.data_bytes:
		function that data(number, string...) converts to bytes
	Mind.Knowledge.Knowledge:
		class for all data in programm
	Mind.Knowledge.bytes_data:
		function that bytes converts to data(numbers, strigns...)
	Mind.Knowledge.load:
		function that loads saved data and returns Knowledge object
Mind.Orientation:
	part of library for maps.
	Mind.Orientation.MapError:
		exception for points outside the map
	Mind.Orientation.MAP:
		basic map class
	Mind.Orientation.point:
		basic point class
	Mind.Orientation.group_of_points:
		class for group of points
	Mind.Orientation.rect:
		bacis map rect class
	Mind.Orientation.tiled_map (only if tiledtmxloader can be imported):
		class for map in tiled
Mind.Test:
	part of library for testing other parts (it just helps people to get library)
	Mind.Test.test_know:
		test Mind.Knowledge.Knowledge
	Mind.Test.test_load:
		test Mind.Knowledge.load (test_know must be runed first!)
	Mind.Test.test_map:
		test Mind.Orientation.MAP and other map objects
	Mind.Test.test_tiled_map:
		test Mind.Orientation.tiled_map