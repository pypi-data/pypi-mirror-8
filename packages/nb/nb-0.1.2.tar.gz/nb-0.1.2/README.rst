Nota Bene
==========================

Nota Bene is a simple program that keeps tracks of your notes. It functions similar to git. You add your notes to it, and it provides you with a list of your notes and their tags. What is different about Nota Bene is that, your tags have to be in your files, you cannot tag them via NB.

Note Structure
-------------------------

Nota Bene depends on your notes having a certain structure. It looks for YAML front matter in your note. If you provide a title and tags in the YAML front matter of your note, NB will store that information along with your note's path. This way you can filter your notes using the tags in them.

This way, NB can keep track of notes without caring about the markup you use in your notes.

YAML Front Matter
************************

YAML front matter should look like this:

::

    ---
    title: My Interesting Title
    tags: [life, unverse, everything]
    date: 2014-11-30 18:18:18
    ---


Date can also be in the followin format:

::

    date: 2014-11-30

But these two are the only acceptable date formats. If you format dates differently, sorting behavior is undefined.

See http://jekyllrb.com/docs/frontmatter/ for details.

Why?
-------------------------

Nota Bene is a simle tool that I wrote for myself in a couple of hours. I don't even know whether I will use it or not, but hey, here it is.

License
------------------------
Copyright (c) 2014 Eren Inan Canpolat

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

