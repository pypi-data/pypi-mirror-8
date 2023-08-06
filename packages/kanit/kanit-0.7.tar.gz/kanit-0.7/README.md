=====
KANIT
=====

Kanban board management system by Clay Dowling <clay@lazarusid.com>

Installing
==========

The easiest way to install kanit is to run the easy_install program::

	sudo easy_install kanit

If you prefer the latest and greatest, you can download the zip archive
from the source repository, and run the install tool::

	wget https://github.com/LazarusID/kanit/archive/master.zip
	cd kanit-master
	sudo python setup.py install


Purpose
=======

A good task tracking system for a project is important if the project
has any complexity at all.  If you're a one-person project, a real
kanban board with post it notes is probably sufficient for the task.
Even if you're a multi-person project, as long as you all work in the
same space, the post it notes are probably sufficient.

That all goes to heck if you're a multi-person, multi-site project,
e.g. if you and your buddies are working on a skunkworks project
from your homes.  Even if you're a single person project, sometimes
you need the whiteboard where you're tracking progress to sketch out
an idea.

That's where Kanit comes in.  You manage your project by writing a
bunch of text files, all in the same folder, one for each task.  You
keep your task backlog in a separate folder, and move them into your
current sprint by copying the files into the task folder.  When the 
sprint is done, the files are moved into another folder and archived.

Stories
=======

First, a bit of terminology: when I say "story", that's interchangable
with "task."  Right now, Kanit only has one unit of measurement: the
file.  In future versions, you'll be able to establish parent-child
relationships between these files, so you can have a full hierarchy
of features, stories and tasks.  Or whatever you want to call them.  The
system just won't care.

To create a story, just create a text file (in the folder you're using
for your project management files).  Kanit assumes that these text files
are proper ReStructured Text files, which can be processed by the python
docutils suite.  You should give the text file a name that is 
descriptive of what it contains.

In the file, you should have a proper title, using '===' style bars
above and below.

Kanit will make use of two fields if they are available: status and points.

Status is the task's current status.  You can use whatever set of stati
is appropriate to your situation.  I use "Not Started," "In Process,"
and "Done," but your workflow might need to accomodate a QA team or 
signoff by a stakeholder.  The important thing is to establish a standard
for what you and your team should be using.


Using Kanit
===========

Kanit is incredibly simple to use::

	kanity.py tasks

This assumes that your task list lives in a folder called "tasks" under
your current folder.

In a multi-person project the task folder is probably under source
control (it should be if it isn't).  Let me suggest a couple of best
practices:

1. Before changing the status of a task, update your local checkout.

2. After changing anything in a task file, especially a status, commit
   your changes.

Of course this is no substitute for good communication within your team.
You should talk to them via whatever communications mechanism you have
set up and make sure that you aren't grabbing a task somebody else is
working on.  Mentioning that you are taking a task may also prompt some
important discussion.  Things that they may have realized about the task
that they didn't know when the task was written.

Status Ordering
---------------

Each story is displayed in a list, with the lists organized by their
status.  By default this list is sorted alphabetically.  If in the
folder there is a file "kanit.conf" this file will be read for
information about the sort order you would prefer for the status.

kanit.conf is a JSON file.  If you would like to control the sort order,
create a dictionary in this file with a key of "status.order", and
assign it a list of the values you would like to use for status, in the
order you would like to see them.  Any status that does not appear in
this list will appear after the listed stati sorted in alphabetical
order.

The file I use in my own development looks something like this::

	{
		"status.order": ["Not Started", "In Process", "Done"]
	}

Directory Structure
-------------------

Allow me to suggest the following directory structure::

	tasks 
		|
		+-backlog
		|
		+-archive

The backlog folder will contain stories which you have written, but
haven't yet pulled into a sprint to work on.  It may also happen that in
the course of working on a story, you decide to defer action on it.  I
typically give it a status of "Deferred" so that it is easier to spot,
then move it to the backlog folder.

The archive folder is where I store old sprints.  I zip up everything
with a "Done" status in the sprint folder into an appropriate named
file, such as `archive\sprint-01.zip`  After confirming that the files
really are in the archive, I then delete them from the tasks folder.


