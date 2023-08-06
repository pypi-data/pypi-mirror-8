Mind
=====
Library for games in Python
Mind.Knowledge:
	part of library for data saving.
	Mind.Knowledge.Knowledge:
		class for all data in programm
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