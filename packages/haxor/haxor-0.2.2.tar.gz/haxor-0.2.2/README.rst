haxor
=====

.. image:: https://api.travis-ci.org/avinassh/haxor.png?branch=master
    :target: http://travis-ci.org/avinassh/haxor
.. image:: https://coveralls.io/repos/avinassh/haxor/badge.png?branch=master
    :target: https://coveralls.io/r/avinassh/haxor?branch=master
.. image:: https://pypip.in/v/haxor/badge.png
    :target: https://pypi.python.org/pypi/haxor/
.. image:: https://pypip.in/d/haxor/badge.png
    :target: https://pypi.python.org/pypi/haxor/

Unofficial Python wrapper for official Hacker News API.

Installation
------------

::

    pip install haxor

Usage
-----

import and initialization:

::

    from hackernews import HackerNews
    hn = HackerNews()

Get certain user info by user id (i.e. username on Hacker News)

::

    user = hn.get_user('pg')
    # >>> user.user_id
    # pg
    # >>> user.karma
    # 155040

Stories, comments, jobs, Ask HNs and even polls are just items and they
have unique item id. To get info of an item by item id:

::

    item = hn.get_item(8863)
    # >>> item.title
    # "My YC app: Dropbox - Throw away your USB drive"
    # >>> item.type
    # story
    # >>> item.kids
    # [ 8952, 9224, 8917, ...]

To get item ids of current top stories:

::

    top_story_ids = hn.top_stories()
    # >>> top_story_ids
    # [8432709, 8432616, 8433237, ...]

To get current largest item id:

::

    max_item = hn.get_max_item()
    # >>> max_item
    # 8433746

Examples
--------

Get top 10 stories: 

::

    for story_id in hn.top_stories(limit=10):
        print hn.get_item(story_id)

    # <hackernews.Item: 8432709 - Redis cluster, no longer vaporware>
    # <hackernews.Item: 8432423 - Fluid Actuators from Disney Research Make Soft, Safe Robot Arms>
    # <hackernews.Item: 8433237 - Is Capturing Carbon from the Air Practical?>
    # ...
    # ...


Find all the 'jobs' post from Top Stories:

::

    for story_id in hn.top_stories():
        story = hn.get_item(story_id)
        if story.item_type == 'job':
            print story

    # <hackernews.Item: 8437631 - Lever (YC S12) hiring JavaScript experts, realtime systems engineers, to scale DerbyJS>
    # <hackernews.Item: 8437036 - Product Designer (employee #1) to Organize the World's Code – Blockspring (YC S14)>
    # <hackernews.Item: 8436584 - Django and iOS Hackers Needed – fix healthcare with Drchrono>
    # ...
    # ...


Find Python jobs from monthly who is hiring thread:

::

    # Who is hiring
    # https://news.ycombinator.com/item?id=8394339

    who_is_hiring = hn.get_item(8394339)

    for comment_id in who_is_hiring.kids:
        comment = hn.get_item(comment_id)
        if 'python' in comment.text.lower():
            print comment.item_id

    # 8395568
    # 8394964
    # ...
    # ...


API Reference
-------------

Class: ``HackerNews``
---------------------

**Parameters:**

+-------------+--------+------------+--------------------------------------------------+-----------+
| Name        | Type   | Required   | Description                                      | Default   |
+=============+========+============+==================================================+===========+
| ``version`` | string | No         | specifies Hacker News API version                | ``v0``    |
+-------------+--------+------------+--------------------------------------------------+-----------+

``get_item``
^^^^^^^^^^^^

Description: Returns ``Item`` object

**Parameters:**

+---------------+--------------+------------+----------------------------------------------------+-----------+
| Name          | Type         | Required   | Description                                        | Default   |
+===============+==============+============+====================================================+===========+
| ``item_id``   | string/int   | Yes        | unique item id of Hacker News story, comment etc   | None      |
+---------------+--------------+------------+----------------------------------------------------+-----------+

``get_user``
^^^^^^^^^^^^

Description: Returns ``User`` object

**Parameters:**

+---------------+----------+------------+----------------------------------------+-----------+
| Name          | Type     | Required   | Description                            | Default   |
+===============+==========+============+========================================+===========+
| ``user_id``   | string   | Yes        | unique user id of a Hacker News user   | None      |
+---------------+----------+------------+----------------------------------------+-----------+

``top_stories``
^^^^^^^^^^^^^^^

Description: Returns list of item ids of current top stories

**Parameters:**

+-------------+--------+------------+--------------------------------------------------+-----------+
| Name        | Type   | Required   | Description                                      | Default   |
+=============+========+============+==================================================+===========+
| ``limit``   | int    | No         | specifies the number of stories to be returned   | None      |
+-------------+--------+------------+--------------------------------------------------+-----------+

``get_max_item``
^^^^^^^^^^^^^^^^

Description: Returns current largest item id

Class: ``Item``
---------------

From `Official HackerNews Item`_:

+--------------------+-------------------------------------------------------------------------------------------------------------------+
| Property           | Description                                                                                                       |
+====================+===================================================================================================================+
| item\_id           | The item’s unique id.                                                                                             |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| deleted            | ``true`` if the item is deleted.                                                                                  |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| item\_type         | The type of item. One of “job”, “story”, “comment”, “poll”, or “pollopt”.                                         |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| by                 | The username of the item’s author.                                                                                |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| submission\_time   | Creation date of the item, in Python ``datetime``.                                                                |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| text               | The comment, Ask HN, or poll text. HTML.                                                                          |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| dead               | ``true`` if the item is dead.                                                                                     |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| parent             | The item’s parent. For comments, either another comment or the relevant story. For pollopts, the relevant poll.   |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| kids               | The ids of the item’s comments, in ranked display order.                                                          |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| url                | The URL of the story.                                                                                             |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| score              | The story’s score, or the votes for a pollopt.                                                                    |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| title              | The title of the story or poll.                                                                                   |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| parts              | A list of related pollopts, in display order.                                                                     |
+--------------------+-------------------------------------------------------------------------------------------------------------------+
| raw                | original JSON response.                                                                                           |
+--------------------+-------------------------------------------------------------------------------------------------------------------+

Class: ``User``
---------------

From `Official HackerNews User`_:

+-------------+------------------------------------------------------------------------------------+
| Property    | Description                                                                        |
+=============+====================================================================================+
| user\_id    | The user’s unique username. Case-sensitive.                                        |
+-------------+------------------------------------------------------------------------------------+
| delay       | Delay in minutes between a comment’s creation and its visibility to other users.   |
+-------------+------------------------------------------------------------------------------------+
| created     | Creation date of the user, in Python ``datetime``.                                 |
+-------------+------------------------------------------------------------------------------------+
| karma       | The user’s karma.                                                                  |
+-------------+------------------------------------------------------------------------------------+
| about       | The user’s optional self-description. HTML.                                        |
+-------------+------------------------------------------------------------------------------------+
| submitted   | List of the user’s stories, polls and comments.                                    |
+-------------+------------------------------------------------------------------------------------+
| raw         | original JSON response.                                                            |
+-------------+------------------------------------------------------------------------------------+

LICENSE
-------

::

    The MIT License (MIT)

    Copyright (c) 2013 Avinash Sajjanshetty <a@sajjanshetty.com>

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the
    “Software”), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
    CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
    TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. _Official HackerNews Item: https://github.com/HackerNews/API/blob/master/README.md#items
.. _Official HackerNews User: https://github.com/HackerNews/API/blob/master/README.md#users