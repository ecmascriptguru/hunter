import pandas as pd


def parse_target(file, encoding):
    read_map = {
        'xls': pd.read_excel, 'xlsx': pd.read_excel, 'csv': pd.read_csv,
        'gz': pd.read_csv, 'pkl': pd.read_pickle}
    ext = file.name.split('.')[-1]
    if read_map.get(ext, None):
        try:
            read_func = read_map.get(ext)
            content = read_func(file, encoding=encoding)

            content.columns = range(content.shape[1])
            columns = {"url": 0, "first_name": 1, "last_name": 2}
            for col in columns:
                content.rename(columns={content.columns[columns[col]]: col}, inplace=True)
            
            content = content[list(columns)]
            rows = [dict(row._asdict()) for row in content.itertuples()]
            # count = self.module.bulk_insert(rows, filename=secure_filename(file.filename))
            return True, "Successfully parsed the file.", rows
        except Exception as e:
            return False, str(e), []
    else:
        return False, 'Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl', []


def parse_credentials(file, encoding):
    read_map = {
        'xls': pd.read_excel, 'xlsx': pd.read_excel, 'csv': pd.read_csv,
        'gz': pd.read_csv, 'pkl': pd.read_pickle}
    ext = file.name.split('.')[-1]
    if read_map.get(ext, None):
        try:
            read_func = read_map.get(ext)
            content = read_func(file, encoding=encoding)

            content.columns = range(content.shape[1])
            columns = {"email": 1, "password": 2, "proxy": 3, "recovery_email": 5,
                "recovery_phone": 6, "has_linkedin": 4, "state": 7}
            for col in columns:
                content.rename(columns={content.columns[columns[col]]: col}, inplace=True)
            
            content = content[list(columns)]
            rows = [dict(row._asdict()) for row in content.itertuples()]
            # count = self.module.bulk_insert(rows, filename=secure_filename(file.filename))
            return True, "Successfully parsed the file.", rows
        except Exception as e:
            return False, str(e), []
    else:
        return False, 'Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl', []


def parse_urls(file, encoding='utf-8', is_test_data=False, has_header=False):
    read_map = {
        'xls': pd.read_excel, 'xlsx': pd.read_excel, 'csv': pd.read_csv,
        'gz': pd.read_csv, 'pkl': pd.read_pickle}
    ext = file.name.split('.')[-1]
    if read_map.get(ext, None):
        try:
            read_func = read_map.get(ext)
            content = read_func(file, encoding=encoding)

            content.columns = range(content.shape[1])
            if is_test_data:
                columns = {"url": 0, "number": 1, "first_name": 2, "last_name": 3,
                    "email": 4, "flag": 5, "social": 6}
            else:
                columns = {'url': 0}

            for col in columns:
                content.rename(columns={content.columns[columns[col]]: col}, inplace=True)
            
            content = content[list(columns)]
            rows = [dict(row._asdict()) for row in content.itertuples()]
            return True, "Successfully parsed the file.", rows
        except Exception as e:
            return False, str(e), []
    else:
        return False, 'Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl', []