# spell_picker_5e
Generating spellbooks for 5e.  

The functions let you specify:
- Schools
- Classes
- Spells per level

The fundamental function is `total_contructor` which takes a list of schools, a list of classes, and a list of spells per level.  It defaults to all schools and classes and 0 spells per level.  For the spells per level it starts at cantrips and moves up.  If you put in too few values it will assume zero spells past where you start.  But you always have to start at cantrips! So:

[4,3,3,2]

Will give you 4 cantrips, 3 1st and 2nd spells and 2 3rd level.

To skip lower level spells you need to input zero values:

[0,0,0,3]

Will give 3 3rd level spells.

`total_constructor` build the spellbook DataFrame.
`spellbook_csv_export(spellbook_df)` gives a csv file.
`spellbook_text_file(spellbook_df)` gives a txt file.
`build_everything(args)` does all of the above and takes arguments as specified in the code!
