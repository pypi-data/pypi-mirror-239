Kringle
==========

Kringle is a solution manager for Advent of Code.

At the moment Kringle is bare bones and extremly opinionated. The first assumption it 
makes is that is being called from a directory where there is a solution.py file and a 
input.txt file. The second assumption is that the solution file is going to contain 
three methods, parse(data), part_1(parsed_data), and part_2(parsed_data). It does check,
allowing for both part_1 and part_2 methods to not be implemented yet.

The current flow is simple. It loads the solution module, loads and parses the input 
data, then runs both parts, passing them the parsed input data.


Installation
------------

``pip install kringle``


License
-------

Kringle is distributed under the terms of the `MIT license <https://spdx.org/licenses/MIT.html>`_.
