'''This is the main class for using the model in other Python3 programs.

   Added to the surgeo namespace.'''

import csv
import io
import itertools
import operator
import os
import sqlite3
import sys

import surgeo

###############################################################################


class SurgeoModel(object):
    '''Contains data references and methods for running a BISG model.

    Attributes:
        self.db: an sqlite3 database connection shared for all methods
    Methods:
        guess_race: takes zip and surname and returns a string.
        race_data: takes zip and surname and returns a SurgeoResult object.
        process_csv: takes to paths. Reads path one. Processed result to path 2

    '''

    def __init__(self):
        # Load entire db to memory for performance DISK DATABSE
        db_path = os.path.join(os.path.expanduser('~'),
                               '.surgeo',
                               'census.db')
        if not os.path.exists(db_path):
            raise surgeo.SurgeoError('DB does not exist. Run surgeo.data'
                                     '_setup() or run program with '
                                     '\'--setup\' option.')
        self.db = sqlite3.connect(db_path)

    def guess_race(self, zcta, surname):
        '''zcta and surname go in and a simple race string comes out.

        Args:
            zcta: zip code, string or int
            surname: string
        Returns:
            result.probable_race: string
        Raises:
            None

        '''
        # Check for existence of zip code. Return bad result if bad.
        try:
            cursor = self.db.cursor()
            # Will throw type error if not in db
            cursor.execute('''SELECT state, logical_record FROM
                           geocode_data WHERE zcta=?''', (zcta,))
            state, logical_record = cursor.fetchone()
            cursor.execute('''SELECT pctwhite, pctblack FROM
                           surname_data WHERE name=?''', 
                           (surname.upper(),))
            num_white, num_black = cursor.fetchone()
            # DB entries present is in database, so run it.
            result = surgeo.model.model1.run_model(zcta,
                                                   surname.upper(),
                                                   self.db)
        except TypeError:
            result = SurgeoErrorResult()
        return result.probable_race

    def race_data(self, zcta, surname):
        '''zcta and surname goes in, formatted SurgeoResult comes out.

        Args:
            zcta: zip code, string or int
            surname: string
        Returns:
            result: SurgeoResult object
        Raises:
            None

        '''

        # Check for existence of zip code. Return bad result if bad.
        try:
            cursor = self.db.cursor()
            cursor.execute('''SELECT state, logical_record FROM
                           geocode_data WHERE zcta=?''', (zcta,))
            state, logical_record = cursor.fetchone()
            cursor.execute('''SELECT pctwhite, pctblack FROM
                           surname_data WHERE name=?''', 
                           (surname.upper(),))
            num_white, num_black = cursor.fetchone()            
            # data is in database, so run it.
            result = surgeo.model.model1.run_model(zcta,
                                                   surname.upper(),
                                                   self.db)
        except TypeError:
            result = SurgeoErrorResult()
        return result

    def process_csv(self,
                    filepath_in,
                    filepath_out,
                    verbose=True):
        '''This takes a csv filepath and creates new csv with race data.

        Args:
            filepath_in: file path of csv from which data is read
            filepath_out: file path of csv where data is written
            verbose: True/False which determines if updates are printed
        Returns:
            None
        Raises:
            None

        '''

        # Open file, determine if zip and name in header
        tempfile = open(filepath_in, 'rU')
        number_of_rows = len(tempfile.readlines())
        tempfile.close()
        with open(filepath_in, 'rU') as input_csv:
            csv_reader = csv.reader(input_csv)
            row_1 = next(csv_reader)
            number_of_columns = len(row_1)
            for index, item in enumerate(row_1):
                if type(item) is str:
                    if 'zip' in item.lower() or 'zcta' in item.lower():
                        zip_index = index
                    if 'last nam' in item.lower() or 'surname' in item.lower():
                        surname_index = index
            # zip/name index required. If no index for zip/name, raise error
            try:
                zip_index
                surname_index
            except NameError:
                raise surgeo.SurgeoError('.csv row 1 lacks \'zip\' or ' +
                                         '\'surname\' fields.')
            # Go through all lines, amended lines with new data, and stage.
            # Writing to string buffer rather than file.
            line_buffer = io.StringIO()
            csv_writer = csv.writer(line_buffer)
            # Write header row first by splicing together
            chopped_header_row = row_1[:number_of_columns]
            header_remainder = ['surname', 'zip', 'probable_race',
                                'probable_race_percentage', 'hispanic',
                                'white', 'black', 'asian_or_pi',
                                'american_indian', 'multiracial']
            header_row = [item for item in itertools.chain(chopped_header_row,
                                                           header_remainder)]
            csv_writer.writerow(header_row)
            if verbose is True:
                sys.stdout.write('\rReading from {}\n'.format(filepath_in))
            # You already did a next() before on the iterator, line 2
            for index, entry in enumerate(csv_reader, start=1):
                surname = entry[surname_index]
                zcta = entry[zip_index]
                # Invoke object's race_data
                try:
                    cursor = self.db.cursor()
                    cursor.execute('''SELECT state, logical_record FROM
                                      geocode_data WHERE zcta=?''', (zcta,))
                    state, logical_record = cursor.fetchone()
                    # Zip code is in database, so run it.
                    result = surgeo.model.model1.run_model(zcta,
                                                           surname.upper(),
                                                           self.db)
                except TypeError:
                    result = SurgeoErrorResult()
                result_list = [result.surname,
                               result.zcta,
                               result.probable_race,
                               result.probable_race_percentage,
                               result.hispanic,
                               result.white,
                               result.black,
                               result.asian_or_pi,
                               result.american_indian,
                               result.multiracial]
                # Chop row in the event that rows are a different length
                chopped_row = entry[:number_of_columns]
                # Splice new row together
                new_row = [item for item in
                           itertools.chain(chopped_row, result_list)]
                csv_writer.writerow(new_row)
            if verbose is True:
                sys.stdout.write('Writing to {}.'.format(filepath_out))
            with open(filepath_out, 'w+') as f:
                f.write(line_buffer.getvalue())
            line_buffer.close()
            if verbose is True:
                sys.stdout.write('\nComplete.\n')


###############################################################################


class SurgeoResult(object):
    '''Result class containing BISG data.

    Attributes:
        self.surname: string
        self.zcta: string
        self.zip: string
        self.hispanic: float
        self.white: float
        self.black: float
        self.asian_or_pi: float
        self.american_indian: float
        self.multiracial: float
        self.probable_race: @property string
        self.probable_race_percentage: @property float
        self.as_string: @property string

    '''

    def __init__(self,
                 surname,
                 zcta,
                 hispanic,
                 white,
                 black,
                 asian_or_pi,
                 american_indian,
                 multiracial):
        self.surname = surname
        self.zcta = zcta
        self.zip = zcta
        self.hispanic = hispanic
        self.white = white
        self.black = black
        self.asian_or_pi = asian_or_pi
        self.american_indian = american_indian
        self.multiracial = multiracial

    @property
    def probable_race(self):
        rank_dict = {'Hispanic': self.hispanic,
                     'White': self.white,
                     'Black': self.black,
                     'Asian / Pacific Islander': self.asian_or_pi,
                     'American Indian / Alaskan Eskimo': self.american_indian,
                     'Multiracial': self.multiracial}
        most_probable_race = sorted(rank_dict.items(),
                                    key=operator.itemgetter(1),
                                    reverse=True)[0][0]
        return most_probable_race

    @property
    def probable_race_percentage(self):
        return max(self.hispanic,
                   self.white,
                   self.black,
                   self.asian_or_pi,
                   self.american_indian,
                   self.multiracial)

    @property
    def as_string(self):
        string = '\n'.join(['probable_race={}'.format(self.probable_race),
                            'probable_race_percent={}'.
                            format(self.probable_race_percentage),
                            'surname={}'.format(self.surname),
                            'zip={}'.format(self.zcta),
                            'hispanic={}'.format(self.hispanic),
                            'white={}'.format(self.white),
                            'black={}'.format(self.black),
                            'asian={}'.format(self.asian_or_pi),
                            'indian={}'.format(self.american_indian),
                            'multiracial={}'.format(self.multiracial)])
        return string

    @property
    def as_csv(self):
        original_string = str(self.as_string)
        original_as_list = original_string.split('\n')
        # Get rid of 'probable_race='
        original_as_list = [item.partition('=')[2] for item in
                            original_as_list]
        # Get rid of empties, and turn to csv
        original_as_list = [''.join(['\"', item, '\"']) for item in
                            original_as_list if item is not None]
        csv_string = ','.join(original_as_list) + '\n'
        return csv_string


class SurgeoErrorResult(object):
    '''Result class containing error data.

    Attributes:
        self.surname: string
        self.zcta: string
        self.zip: string
        self.hispanic: float
        self.white: float
        self.black: float
        self.asian_or_pi: float
        self.american_indian: float
        self.multiracial: float
        self.probable_race: @property string
        self.probable_race_percentage: @property float
        self.as_string: @property string

    '''

    def __init__(self):
        self.surname = 'Error'
        self.zcta = '00000'
        self.zip = '00000'
        self.hispanic = 0
        self.white = 0
        self.black = 0
        self.asian_or_pi = 0
        self.american_indian = 0
        self.multiracial = 0
        self.probable_race = 'Error'
        self.probable_race_percentage = 0
        self.as_string = '\n'.join(['probable_race=Error',
                                    'probable_race_percent=Error',
                                    'surname=Error',
                                    'zip=Error',
                                    'hispanic=Error',
                                    'white=Error',
                                    'black=Error',
                                    'asian=Error',
                                    'indian=Error',
                                    'multiracial=Error'])
