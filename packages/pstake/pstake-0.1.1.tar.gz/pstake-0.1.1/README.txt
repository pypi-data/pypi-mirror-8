PSTricks Converter
==================

`PSTricks <http://tug.org/PSTricks/main.cgi/>`__ is a system that allows
drawing virtually `any
<http://tug.org/PSTricks/main.cgi?file=Examples/Gallery/Gallery>`__\ `thing
<http://tug.org/PSTricks/main.cgi?file=Examples/Gallery3D/Gallery3D>`__ inside
TeX/LaTeX.  The quality of the drawings is unbeatable.

Pstake is a simple tool that uses `LaTeX <http://www.latex-project.org>`__ and
`imagemagick <http://www.imagemagick.org>`__ to compile and convert PSTricks
into an image file.  The source PSTricks commands are stored in a .tex file,
and pstake will wrap it around a boilerplate, use LaTeX to generate an EPS
file, and use imagemagick to convert it to the destination format.  Currently
only .png is supported because it's the most convenient format for web pages.

.. vim: set ff=unix ft=rst fenc=utf8:
