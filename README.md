# doclib
Tool for managing and filing documents


## commands

### config commands

set file association

    doclib assoc EXT APPLICATION



### project commands

list projects:

    doclib proj ls

create new project

    doclib proj add PROJECT [--desc DESCRIPTION]

delete a project

    doclib proj rm PROJECT [--force]

rename a project

    doclib proj mv PROJECT NEWNAME

copy a project

    doclib proj cp PROJECT NEWNAME

get info about a project

    doclib proj info PROJECT

### document commands

list documents in a project

    doclib doc ls PROJECT

add new (revision of) document:

    doclib doc add PROJECT DOCNAME PATH [--link / --copy] [--desc DESCRIPTION]
        [--notlatest] [--rev REVISION] [--tag TAG1 TAG2 ...]

delete a document:

    doclib doc rm PROJECT DOCNAME [--force] [--rev REVISION]

rename a document:

    doclib doc mv PROJECT DOCNAME [NEWNAME] [--project NEWPROJ]

copy a document:

    doclib doc cp PROJECT DOCNAME [NEWNAME] [--project NEWPROJ]

get info about a document:

    doclib doc info PROJECT DOCNAME

open a document:

    doclib doc open PROJECT DOCNAME [--rev REVISION]

set current revision:

    doclib doc cur PROJECT DOCNAME REVISION

tag a document:

    doclib doc tag PROJECT DOCNAME [TAG1 TAG2 ...]

### tag commands

list tags:

    doclib tag ls

delete tags:

    doclib tag rm [TAG1 TAG2 ...]

search documents with tags:

    doclib tag search [TAG1 TAG2 ...] [--project PROJECT]
