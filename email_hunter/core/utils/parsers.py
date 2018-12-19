import pandas as pd


def parse_target(file, encoding):
    read_map = {
        'xls': pd.read_excel, 'xlsx': pd.read_excel, 'csv': pd.read_csv,
        'gz': pd.read_csv, 'pkl': pd.read_pickle}
    ext = file.name.split('.')[-1]
    if read_map.get(ext, None):
        read_func = read_map.get(ext)
        content = read_func(file, encoding=encoding)

        content.columns = range(content.shape[1])
        columns = {"url": 0, "first_name": 1, "last_name": 2}
        for col in columns:
            content.rename(columns={content.columns[columns[col]]: col}, inplace=True)
        
        content = content[list(columns)]
        rows = [dict(row._asdict()) for row in content.itertuples()]
        # count = self.module.bulk_insert(rows, filename=secure_filename(file.filename))
        return True, rows
    else:
        return False, []