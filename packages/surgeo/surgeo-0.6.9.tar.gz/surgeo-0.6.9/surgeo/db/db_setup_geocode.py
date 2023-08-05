
import collections
import ftplib
import itertools
import os
import sqlite3
import sys
import time
import traceback
import zipfile


def setup_geocode_table(verbose):
    '''This sets up the geocoding database.

    Args:
        verbose: True/False for whether function outputs info.
    Returns:
        None
    Raises:
        None

    This function first downloads a geographic header file for each state. It
    then downloads file 00002 for each state. These are downloaded in zip
    format, and then unzipped. It then creates two tables, geocode_data and
    logical_race_data and populates the database. The geocode_data contains
    data for geographic areas. The logical record from the geocode_data
    directly correlates with a specific population in the geographic area,
    which is broken down by race.

    '''
    
    # For 'Other race" Iterative Proportional Fitting is used. Costants here.
    OTHER_RACE_HISPANIC_RATE = float(11.1)/100
    OTHER_RACE_WHITE_RATE = float(70.5)/100
    OTHER_RACE_BLACK_RATE = float(11.3)/100
    OTHER_RACE_API_RATE = float(7.0)/100
    OTHER_RACE_AI_RATE = float(.9)/100
    OTHER_RACE_MULTIRACIAL_RATE = float(.8)/100
    
    if verbose is True:
        sys.stdout.write('Downloading census files ... \t\t\n')
    # Created named tuple for organizing
    home_dir_path = os.path.expanduser("~")
    data_dir_path = os.path.join(home_dir_path, '.surgeo')
    # Download files from census server.
    ftp = ftplib.FTP('ftp.census.gov')
    ftp.login()
    ftp.cwd('census_2000/datasets/Summary_File_1')
    # List dir
    state_list = ftp.nlst()
    time.sleep(0)
    # Drop all elements prior to states
    state_list = itertools.dropwhile(lambda x: x != 'Alabama', state_list)
    # Make dropwhile object to list
    state_list = list(state_list)
    zip_files_downloaded = []
    for state in state_list:
        time.sleep(0)
        ftp.cwd('/')
        ftp.cwd(''.join(['census_2000/datasets/Summary_File_1',
                         '/',
                         state]))
        file_list = ftp.nlst()
        for item in file_list:
            time.sleep(0)
            if '00002_uf1.zip' in item or 'geo_uf1.zip' in item:
                if verbose is True:
                    print(''.join(['Downloading ', item]))
                file_path = os.path.join(data_dir_path, item)
                zip_files_downloaded.append(file_path)
                ftp.retrbinary('RETR ' + item, open(file_path, 'wb+').write)
    if verbose is True:
        sys.stdout.write('\t\t\t\t\tOK\n')
    # unzip files
    for zipfile_path in zip_files_downloaded:
        time.sleep(0)
        # Name of XXgeo_uf1.zip --> XXgeo.uf1
        # Name of XX00002_uf1.zip --> XX0000.uf1
        file_component = os.path.basename(zipfile_path).replace('.zip', '')
        file_component = file_component.replace('_', '.')
        if verbose is True:
            print('Writing {}'.format(file_component))
        dir_component = os.path.dirname(zipfile_path)
        # Zip file is now and iterator to save on ram.
        with zipfile.ZipFile(zipfile_path, 'r') as f:
            with f.open(file_component, 'r') as f2:
                with open(os.path.join(dir_component,
                          file_component),
                          'w+b') as f3:
                    for line in f2:
                        f3.write(line)
    # Now everything has been downloaded. Start commit to db
    try:
        db_path = os.path.join(os.path.expanduser('~'),
                               '.surgeo',
                               'census.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                          geocode_data(id INTEGER PRIMARY KEY,
                          state TEXT, summary_level TEXT, logical_record TEXT,
                          zcta TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS logical_race_data(id
                          INTEGER PRIMARY KEY, state TEXT, logical_record TEXT,
                          num_white REAL, num_black REAL, num_ai REAL,
                          num_api REAL, num_hispanic REAL, num_multi REAL)''')
        # now start loading to db
        list_of_filenames = os.listdir(data_dir_path)
        number_of_filenames = len(list_of_filenames)
        for index, filename in enumerate(list_of_filenames):
            time.sleep(0)
            # First the geographic header file
            if 'geo.uf1' in filename:
                if verbose is True:
                    try:
                        last_write
                    except NameError:
                        last_write = 1
                    if index > last_write:
                        sys.stdout.write('\rWriting geoheader: {} of {}'
                                         .format(index,
                                                 number_of_filenames))
                        last_write = index
                file_path = os.path.join(data_dir_path,
                                         filename)
                #
                DESIRED_SUMMARY_LEVEL = '871'
                # Only latin1 appears to work, even thoug site specifies ascii
                with open(file_path, 'r', encoding='latin-1') as f3:
                    for line in f3:
                        time.sleep(0)
                        state = line[6:8]
                        summary_level = line[8:11]
                        logical_record = line[18:25]
                        zcta = line[160:165]
                        # Only ZCTA wide numbers considered
                        if not summary_level == DESIRED_SUMMARY_LEVEL:
                            continue
                        cursor.execute('''INSERT INTO geocode_data(id,
                                          state, summary_level, logical_record,
                                          zcta) VALUES(NULL, ?, ?, ?, ?)''',
                                       (state,
                                        summary_level,
                                        logical_record,
                                        zcta))
        if verbose is True:
            sys.stdout.write('\rWriting geoheader: {} of {}\n'.format
                            (number_of_filenames, number_of_filenames))
        for index, filename in enumerate(list_of_filenames):
            time.sleep(0)
            # First the geographic header file
            if '00002.uf1' in filename:
                if verbose is True:
                    try:
                        last_write
                        last_write = 1
                    except NameError:
                        last_write = 1
                    if index > last_write:
                        sys.stdout.write('\rWriting race data: {} of {}'
                                         .format(index,
                                                 number_of_filenames))
                        sys.stdout.flush()
                        last_write = index
                file_path = os.path.join(data_dir_path,
                                         filename)
                with open(file_path, 'r', encoding='latin-1') as f4:
                    for line in f4:
                        # Remainder db input
                        table_p8 = line.split(',')[86:103]
                        state = line[5:7]
                        logical_record = line[15:22]
                        # Need to translate "Other race" into one of the
                        # six categories through proportional fitting.
                        num_other = table_p8[7]
                        OTHER_RACE_HISPANIC_RATE
                        OTHER_RACE_WHITE_RATE
                        OTHER_RACE_BLACK_RATE
                        OTHER_RACE_API_RATE
                        OTHER_RACE_AI_RATE
                        OTHER_RACE_MULTIRACIAL_RATE
                        other_hispanic = str(round(int(num_other) * 
                                                   OTHER_RACE_HISPANIC_RATE))
                        other_white = str(round(int(num_other) * 
                                                OTHER_RACE_WHITE_RATE))
                        other_black = str(round(int(num_other) * 
                                                OTHER_RACE_BLACK_RATE))
                        other_api = str(round(int(num_other) * 
                                              OTHER_RACE_API_RATE))
                        other_ai = str(round(int(num_other) * 
                                             OTHER_RACE_AI_RATE))
                        other_multiracial = str(round(int(num_other) * 
                                                OTHER_RACE_MULTIRACIAL_RATE))
                        # Breaking up table p8
                        total_pop = table_p8[0]
                        total_not_hispanic = table_p8[1]
                        num_white = str(int(table_p8[2]) + int(other_white))
                        num_black = str(int(table_p8[3]) + int(other_black))
                        num_ai = str(int(table_p8[4]) + int(other_ai))
                        num_asian = table_p8[5]
                        num_pacisland = table_p8[6]
                        num_api = str(int(num_asian) + 
                                      int(num_pacisland) +
                                      int(other_api))
                        num_other = table_p8[7]
                        num_multi = str(int(table_p8[8]) + 
                                        int(other_multiracial))
                        num_hispanic = str(int(table_p8[9]) +
                                           int(other_hispanic))  
                        cursor.execute('''INSERT INTO logical_race_data(
                                          id, state, logical_record,
                                          num_white, num_black,
                                          num_ai, num_api,
                                          num_hispanic, num_multi) VALUES(
                                          NULL, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                      (state,
                                       logical_record,
                                       num_white,
                                       num_black,
                                       num_ai,
                                       num_api,
                                       num_multi,
                                       num_hispanic))
        if verbose is True:
            sys.stdout.write('\rWriting blockfile: {} of {}\n'
                             .format(number_of_filenames, number_of_filenames))
            sys.stdout.write('Creating indices ... \t\t\t')
            sys.stdout.flush()
        cursor.execute('''CREATE INDEX IF NOT EXISTS zcta_index ON
                          geocode_data(zcta)''')
        cursor.execute('''CREATE INDEX IF NOT EXISTS logical_record_index ON
                          logical_race_data(logical_record)''')
        sys.stdout.write('OK\n')
        # Now commit
        connection.commit()
        connection.close()
    except sqlite3.Error as e:
        traceback.print_exc()
        connection.rollback()
        connection.close()
        raise e
