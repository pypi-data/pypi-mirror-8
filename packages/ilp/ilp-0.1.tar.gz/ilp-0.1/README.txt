ILP(1)
======
slowpoke <mail+git@slowpoke.io>
:encoding: utf-8
:doctype: manpage

NAME
----
ilp - a tag-based file indexer

SYNOPSIS
--------

ilp <subcommand> [<args>]

ilp -i

DESCRIPTION
-----------

ilp is a command-line utility which indexes files, and organizes them
with tags. It will not touch the files on disk, but instead keep track of them
in a database, much like the mlocate utility found on many UNIX or UNIX-like
system. To uniquely identify a file, ilp stores it as a hash of its
contents.

OPTIONS
-------

<subcommand>::
    All functionality of ilp is implemented in subcommands, similar to
    git or other VCS. See 'SUBCOMMANDS' for an overview, or use the command
    "help".

-i::
    Start an interactive shell, where you can issue subcommands directly.

SUBCOMMANDS
-----------

Much like a VCS such as git, ilp does all the work with various
subcommands. You can either issue them as an argument to the command line
utility, or start an interactive shell with '-i' and issue them directly.

ilp index [-r] <path> [<path>...]::
    Add one or more files to the index. The '-r' switch turns on recursive
    indexing, in which case <path> can be either a file or directory, and will
    add all files below a given directory to the index.

ilp forget [-r] <path> [<path>...]::
    Counterpart to the *index* subcommand. Removes files from the index.
    Correspondingly, '-r' turns on recursive removing.

ilp tag [-r] <path> <tag> [<tag>...]::
    Tag a file with one or more tags. Similar to *index* and *forget*, '-r' will
    apply the tags recursively to all files below a given directory.

ilp untag [-r] <path> <tag> [<tag>...]::
    Counterpart to tag. Remove tags from a file. '-r' works the same way.

ilp deltag <tag> [<tag>...]::
    Delete tags from the database. Note that tags are automatically created when
    first used, so this command has no counterpart.

ilp list <what>::
    List items on the index. <what> can be 'files' or 'tags'.

ilp info [-t] <what>::
    Get info on files or tags. Since filenames and tags can't be meaningfully
    differentiated, '-t' ('--tag') needs to be passed if information on a tag is
    wanted.

ilp search <query>::
    Search files on the index. See 'SEARCH QUERIES' for how a query works.

ilp clear [-y]::
    Purge the database. This won't do anything unless '-y' ('--yes') is passed.

SEARCH QUERIES
--------------

ilp uses a simple DSL for search queries, which is based on basic set
operations. It requires a bit of understanding about how tagging in ilp
works. If you just want a quick start (it might be all you need, it's rather
intuitive already), see 'EXAMPLE QUERIES'.

Basically, every tag is regarded as a set of all files it is tagging. That might
sound counterintuitive at first (because you would probably expect the relation
to be the other way round), but makes searching through tagged files incredibly
easy, yet powerful - because every operation on a set results in a new set, on
which more operations can be applied. Think of it in terms of Venn diagrams.

For example, if you want to have all files which are tagged both "foo" and
"bar", you'd simply do a logical and on the two sets, and the resulting set is
your wanted result.

This works analogously (and intuitively!) with logical or and not. Even
exclusive or (xor) works, and is quite useful, too - you can use it to find all
files which are either tagged "foo" or "bar", but not both.

Here's a simple overview of the language in Pseudo-BNFL:

    <query>    := [<operator>] <tag> [<query>]
    <operator> := "or" | "and" | "not" | "xor"

EXAMPLE QUERIES
~~~~~~~~~~~~~~~

A simple search query might look like

    foo and bar

or

    foo not bar
    
Something more complex could be

    foo xor bar not baz spam

Notice that if you just write multiple tags, the last given operator is always
implied. The query could have been written explicitly as 

    foo xor bar not baz not spam

If no operator is given at all, "or" is implied. That means
search for "foo bar" is the same as searching for "foo or bar" (or even "or foo
or bar").

TRIVIA
------

If you have wondered what ilp stands for, its an acronym for Index Librorum
Prohibitorum - the infamous (and since 1966 defunct) list of books prohibited by
the Vatican. It's really just the first thing that came to mind in relation to
indexing files, and "ilp" sounded catchy and is short to type. Besides, Latin
names make everything sound more awesome.
