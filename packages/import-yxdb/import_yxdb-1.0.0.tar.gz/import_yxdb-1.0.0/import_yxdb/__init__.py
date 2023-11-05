# import packages
import pandas as pd
from yxdb import yxdb_reader






def yxdb_to_dict(file, names=None, usecols=None, skiprows=0, nrows=None, import_summary=False):
    '''
    This function imports a yxdb file and return it as a dictionary.

    Parameters
    ----------
    file : string
        Name of the the yxdb-file. If only the file name is provided the current directy is used for the location of the yxdb-file. Include path if the file is located in a different folder.
    names : list, or None, optional
        List of column names to import. If None, then all columns are imported. The default is None.
    usecols : list, or None, optional
        List of column names to import. 
        If None, then parse all columns.
        If list of int, then indicates list of column numbers to be parsed (0-indexed).
        If list of string, then indicates list of column names to be parsed.
        The default is None.
    skiprows : integer, optional
        The number of lines to skip at the start of the file. The default is 0.
    nrows : integer or None, optional
        The number of rows to parse (after skiprows have been applied). If None, then all rows will be imported. The default is None.
    import_summary : boolean, optional
        Select if the import function should return an overview of columns and rows imported. The default is False.

    Returns
    -------
    dict_yxdb : dict
        Returns a dictionary in which the keys contains the column names, and the values contains the data for the respective column.

    '''
    
    
    # define file
    My_yxdb = yxdb_reader.YxdbReader(path=file)
    

    # ----------------------------------------------------
    # Defines the columns to be extracted
    # ----------------------------------------------------

    # extract from yxdb-metadata a dict with column names as keys and column location(number/index) as values
    Dict_with_columns = My_yxdb._record._name_to_index

    # defines the keys as a list
    List_with_columns = Dict_with_columns.keys()

    # Check if Usecols have been specificed by user
    if isinstance(usecols, list) and names==None:

        # if Usecol has been specified as integers
        if all([isinstance(item, int) for item in usecols])==True:
            names=[]
            for key in Dict_with_columns.keys():
                for value in usecols:
                    if Dict_with_columns[key]==value:
                        names = names + [key]

        # if Usecol has been specified as strings
        if all([isinstance(item, str) for item in usecols])==True:
            names = usecols

    # Only keep column names that match the user-defined columns
    if names!=None:
        List_with_columns = [x for x in List_with_columns if x in names]


    # ----------------------------------------------------
    # Defines empty dict with empty lists for the relevant columns - used to store the extracted data
    # ----------------------------------------------------

    # Create empty dict to store extracted data with column names as keys AND Creates empty list for all column names in the dict
    dict_yxdb = dict()
    for i in List_with_columns:
        dict_yxdb[i] = []


    # ----------------------------------------------------
    # Extract all (user-defined) rows and columns 
    # ----------------------------------------------------

    # loop through all records for a specific column (i) and append value their respects columns lists
    rowNumber = 0
    while My_yxdb.next():
        
        # Check if all user-defined inputs have been defiend and if so -> terminate
        if nrows!=None and rowNumber>=skiprows+nrows:
            My_yxdb.close()
            break

        # check if RowNumber complies with user-defined input
        if rowNumber>=skiprows:
        
            # loop through all columns in the source data
            for i in List_with_columns:

                dict_yxdb[i] += [My_yxdb.read_name(i)]
                #dict_yxdb[i] += [My_yxdb.read_index(Dict_with_columns[i])]
        
        rowNumber = rowNumber+1


    # ----------------------------------------------------
    # Controlling the extracted data
    # ----------------------------------------------------

    if import_summary==True:
        # Check number of records loaded for each column
        print("------------------------------------")
        print("Records loaded")
        print("------------------------------------")
        for i in List_with_columns:
            print(i+": "+str(len(dict_yxdb[i] )))


    return dict_yxdb






def yxdb_to_pandas(file, names=None, usecols=None, skiprows=0, nrows=None, import_summary=False):
    '''
    This function imports a yxdb file and return it as a pandas dataframe.

    Parameters
    ----------
    file : string
        Name of the the yxdb-file. If only the file name is provided the current directy is used for the location of the yxdb-file. Include path if the file is located in a different folder.
    names : list, or None, optional
        List of column names to import. If None, then all columns are imported. The default is None.
    usecols : list, or None, optional
        List of column names to import. 
        If None, then parse all columns.
        If list of int, then indicates list of column numbers to be parsed (0-indexed).
        If list of string, then indicates list of column names to be parsed.
        The default is None.
    skiprows : integer, optional
        The number of lines to skip at the start of the file. The default is 0.
    nrows : integer or None, optional
        The number of rows to parse (after skiprows have been applied). If None, then all rows will be imported. The default is None.
    import_summary : boolean, optional
        Select if the import function should return an overview of columns and rows imported. The default is False.

    Returns
    -------
    dict_yxdb : dict
        Returns a pandas dataframe.

    '''
    
    # Create DataFrame
    return pd.DataFrame(yxdb_to_dict(file=file, names=names, usecols=usecols, skiprows=skiprows, nrows=nrows, import_summary=import_summary))


















# test yxdb_to_dict
#dict_yxdb = yxdb_to_dict(file="\\\\Fsdkhq001\\cos419$\\Log_proj\\SandOP\\GLAM\\2023_Model\\01_Data\\05_Tableau\\GLAM data prepped.yxdb")

# test yxdb_to_pandas
#df_yxdb = yxdb_to_pandas(file="\\\\Fsdkhq001\\cos419$\\Log_proj\\SandOP\\GLAM\\2023_Model\\01_Data\\05_Tableau\\GLAM data prepped.yxdb")
