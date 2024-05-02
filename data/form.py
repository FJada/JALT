import data.form_filler as ff
import logging

# Directly specify the absolute path to the error log file
log_file_path = './server/error.log'

# Configure the logger
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define the field names for the dropdown form
SELECTED_TRAIN_LINE = 'selected_train_line'

# Define the available train lines for the dropdown
TRAIN_LINES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'J', 'L', 'M', 'N', 'Q', 'R', 'S', 'Z', '1', '2', '3', '4', '5', '6', '7']

BOROUGHS = ['Queens', 'Manhattan', 'Bronx', 'Brooklyn', 'Staten Island']

ENDPOINTS = {
    'A': '/endpointA',
    'B': '/endpointB',
    'C': '/endpointC',
    'D': '/endpointD',
    'E': '/endpointE',
    'F': '/endpointF',
    'G': '/endpointG',
    'J': '/endpointJ',
    'L': '/endpointL',
    'M': '/endpointM',
    'N': '/endpointN',
    'Q': '/endpointQ',
    'R': '/endpointR',
    'S': '/endpointS',
    'Z': '/endpointZ',
    '1': '/endpoint1',
    '2': '/endpoint2',
    '3': '/endpoint3',
    '4': '/endpoint4',
    '5': '/endpoint5',
    '6': '/endpoint6',
    '7': '/endpoint7',

}

# Define the dropdown form fields
DROPDOWN_FORM_FLDS = [
    {
        ff.FLD_NM: 'Instructions',
        ff.QSTN: 'Select a train line:',
        ff.INSTRUCTIONS: True,
    },
    {
        ff.FLD_NM: SELECTED_TRAIN_LINE,
        ff.QSTN: '',
        ff.CHOICES: TRAIN_LINES,
        ff.PARAM_TYPE: ff.PATH,  # Use PATH for dropdown
        ff.OPT: False,
        'endpoints': ENDPOINTS,
    },
]


def get_form() -> list:
    """
    Returns the dropdown form fields.
    """
    try:
        return DROPDOWN_FORM_FLDS
    except Exception as e:
        logger.error(f"Error getting dropdown form: {str(e)}")
        raise


def get_form_descr() -> dict:
    """
    For Swagger!
    """
    try:
        return ff.get_form_descr(DROPDOWN_FORM_FLDS)
    except Exception as e:
        logger.error(f"Error getting dropdown form description: {str(e)}")
        raise


def get_fld_names() -> list:
    """
    Returns the names of the form fields.
    """
    try:
        return ff.get_fld_names(DROPDOWN_FORM_FLDS)
    except Exception as e:
        logger.error(f"Error getting field names: {str(e)}")
        raise


def main():
    try:
        # print(f'Form: {get_form()=}\n\n')
        print(f'Form: {get_form_descr()=}\n\n')
        # print(f'Field names: {get_fld_names()=}\n\n')
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")


if __name__ == "__main__":
    main()
