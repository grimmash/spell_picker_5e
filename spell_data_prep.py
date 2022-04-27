import pandas as pd

# Data Load and prep
spell_df = pd.read_csv("Spells.csv")
spell_df['Classes'].fillna("Unknown", inplace=True)
spell_df.head()

# Variables

# Get schools from input
school_list = spell_df['School'].unique()
print(school_list)

# Get classes from input
classes_raw = spell_df['Classes'].unique()

# Clean up the classes
class_list = []

for phrase in classes_raw:
    #print(phrase.split(","))

    listed_phrase = phrase.split(",")
    for word in listed_phrase:
        word = word.strip()
        #print(word)
        class_list.append(word)

class_list = list(set(class_list))
print(class_list)


# functions

# map binary flags

def class_mapper(class_value, class_lookup_column):
    '''
    Maps the input classes to columns for binary flag filtering by class
    '''
    if class_value in class_lookup_column:
        return 1
    else:
        return 0


def spell_list_length_validator(some_list):
    new_list = some_list
    length_value = len(some_list)
    diff = 10 - length_value
    if length_value < 10:
        for i in range(diff):
            new_list.append(0)
            result = new_list
    else:
        result = some_list
    return result


def spellbook_validator(valid_schools=school_list,
                        valid_classes=class_list,
                        spells_per_level=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
    '''
    Validates if your list of schoosl, classes and spell levels is consitent with the input sata and 5e spell levels.
    '''

    if (not all(x in school_list for x in valid_schools)):
        print("Please make sure your arcane schools are from the following list:")
        for i in school_list:
            print("    " + i)
    elif (not all(x in class_list for x in valid_classes)):
        print("Please make sure your classes are from the following list:")
        for i in class_list:
            print("    " + i)
    elif (len(spells_per_level) > 10):
        print("You have more than 10 spell levels enumerated!  Please enter less than 10 levels.")

    else:
        print("Schools chosen: ")
        for i in valid_schools:
            print("    " + i)
        print("Classes chosen: ")
        for i in valid_classes:
            print("    " + i)
        print("Spells Chosen: ")
        for i, x in zip(spells_per_level, range(0, len(spells_per_level))):
            print("    Level " + str(x) + " spells: " + str(i))


def filtered_spell_list(valid_schools=school_list,
                        valid_classes=class_list):
    '''
    Filters the raw spell list by the schools and classes you define
    '''
    # filter by schools(s)
    df = spell_df[spell_df['School'].isin(valid_schools)]
    # filter by class(es)
    df2 = df[(df[valid_classes] == 1).any(axis=1)]
    return df2


def spellbook_generator(df, levels=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
    new_df = pd.DataFrame()
    level_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i, x in zip(levels, level_list):
        temp_df = df[df["Spell Level"] == x]
        if i > temp_df.shape[0]:
            sample_df = temp_df
        else:
            sample_df = temp_df.sample(i, replace=False)
        new_df = new_df.append(sample_df)
    return new_df


def total_constructor(valid_schools=school_list,
                      valid_classes=class_list,
                      spells_per_level=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
    spellbook_validator(valid_schools, valid_classes, spells_per_level)
    levels = spell_list_length_validator(spells_per_level)
    pool_of_spells = filtered_spell_list(valid_schools, valid_classes)
    spellbook = spellbook_generator(pool_of_spells, levels)
    spellbook.drop(class_list, axis=1, inplace=True)
    return spellbook


def spellbook_export(df, file_name):
    df.to_csv(file_name, index=False)

# Data Cleanup
# add columns for schools and classes for quick filtering
spell_df = pd.concat([spell_df,pd.DataFrame(columns=class_list)])

# Prepare the spell input data to have binary flags by class
for value in class_list:
    spell_df[value] = spell_df.apply(lambda x: class_mapper(value, x['Classes']), axis=1)

# map spell level names to int
spell_level_dict = {"Cantrip":0,
                   "1st":1,
                   "2nd":2,
                   "3rd":3,
                   "4th":4,
                   "5th":5,
                   "6th":6,
                   "7th":7,
                   "8th":8,
                   "9th":9}

spell_df["Spell Level"] = spell_df["Level"].map(spell_level_dict)