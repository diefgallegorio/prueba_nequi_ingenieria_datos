import pandas as pd

LIMIT = 10000000

def clean_columns_names(columns):
    try:
        columns_clean = []
        for column in columns:
            column = column.replace("-", "").upper()
            column = "_".join(column.split())
            columns_clean.append(column)
        return columns_clean
    except Exception as e:
        print(e)


def manage_duplicates(dataframe:pd.DataFrame(), df_name):
    try:
        df = dataframe.copy()
        print(f"Cantidad de archivos duplicados en {df_name}: {df[df.duplicated()].shape[0]}")
        df = df.drop_duplicates().reset_index(drop=True)
        return df
    except Exception as e:
        print(e)


def transform_columns_users(dataframe:pd.DataFrame()):
    try:
        df = dataframe.copy()
        df = df.reset_index().rename(columns={'index': 'ID_user',
                                              'Person': 'user_full_name'})
        df.columns = clean_columns_names(df.columns)
        df['PER_CAPITA_INCOME_ZIPCODE'] = df['PER_CAPITA_INCOME_ZIPCODE'].str[1:].astype(float)
        df['YEARLY_INCOME_PERSON'] = df['YEARLY_INCOME_PERSON'].str[1:].astype(float)
        df['TOTAL_DEBT'] = df['TOTAL_DEBT'].str[1:].astype(float)
        df['ZIPCODE'] = df['ZIPCODE'].astype(str)
        df['APARTMENT'] = df['APARTMENT'].fillna(0).astype(int).astype(str)
        df = manage_duplicates(df, 'users')
        data_validation_users(df)
        return df
    except Exception as e:
        print(e)


def transform_columns_cards(dataframe:pd.DataFrame()):
    try:
        df = dataframe.copy()
        df = df.rename(columns={'CARD INDEX': 'ID_card',
                                'User': 'ID_user'})
        df.columns = clean_columns_names(df.columns)
        df['CREDIT_LIMIT'] = df['CREDIT_LIMIT'].str[1:].astype(float)
        df['HAS_CHIP'] =  df['HAS_CHIP'].replace({'YES': True, 'NO': False}).astype(bool)
        df['CARD_ON_DARK_WEB'] =  df['CARD_ON_DARK_WEB'].replace({'YES': True, 'NO': False}).astype(bool)
        df[['CARD_NUMBER', 'CVV']] = df[['CARD_NUMBER', 'CVV']].astype(str)
        df = manage_duplicates(df, 'cards')
        data_validation_cards(df)
        return df
    except Exception as e:
        print(e)

def transform_columns_transactions(dataframe:pd.DataFrame()):
    try:
        df = dataframe.copy()
        # Rename columns of user and card ID's and clean columns on transactions data
        df = df.reset_index().rename(columns={
                                        'User': 'ID_user',
                                        'Card': 'ID_card',
                                        'index': 'ID_transaction'
                                    })
        df.columns = clean_columns_names(df.columns)
        df['AMOUNT'] = df['AMOUNT'].str[1:].astype(float)
        df['MERCHANT_NAME'] = df['MERCHANT_NAME'].astype(str)
        df['MCC'] = df['MCC'].astype(str)
        df['IS_FRAUD?'] = df['IS_FRAUD?'].replace({'Yes': True, 'No': False}).astype(bool)
        df['ZIP'] = df['ZIP'].fillna(0).astype(int).astype(str).replace({'0': 'N/A'})
        df['ERRORS?'] = df['ERRORS?'].fillna('N/A')
        df['TRANSACTION_DATE'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']])
        df = manage_duplicates(df, 'transactions')
        data_validation_transactions(df)
        return df
    except Exception as e:
        print(e)


def data_validation_users(df_users:pd.DataFrame()):
    try:
        print(f"Validación clave primaria: {df_users.ID_USER.nunique() == len(df_users)}")
        print(f"Validación completitud de los datos: {df_users.isnull().sum().sum() == 0}")
        print(f"Validación duplicidad de datos: {len(df_users[df_users.duplicated()]) == 0}")
    except Exception as e:
        print(e)


def data_validation_cards(df_cards:pd.DataFrame()):
    try:
        print(f"Validación clave primaria: {df_cards.ID_USER.apply(str).str.cat(df_cards.ID_CARD.apply(str), sep=' - ').nunique() == len(df_cards)}")
        print(f"Validación completitud de los datos: {df_cards.isnull().sum().sum() == 0}")
        print(f"Validación duplicidad de datos: {len(df_cards[df_cards.duplicated()]) == 0}")
    except Exception as e:
        print(e)


def data_validation_transactions(df_transactions:pd.DataFrame()):
    try:
        print(f"Validación clave primaria: {df_transactions.ID_TRANSACTION.nunique() == len(df_transactions)}")
        print(f"Validación completitud de los datos: {df_transactions.isnull().sum().sum() == 0}")
        print(f"Validación duplicidad de datos: {len(df_transactions[df_transactions.duplicated()]) == 0}")
    except Exception as e:
        print(e)

if __name__ == '__main__':

    print('------------ data users ------------')
    df_users = pd.read_csv("./../data/raw/sd254_users.csv")
    df_users = transform_columns_users(df_users)
    df_users.to_parquet("./../data/processed/data_users.parquet", engine='fastparquet')

    print('------------ data cards ------------')
    df_cards = pd.read_csv("./../data/raw/sd254_cards.csv")
    df_cards = transform_columns_cards(df_cards)
    df_cards.to_parquet("./../data/processed/data_cards.parquet", engine='fastparquet')

    print('------------ data transactions ------------')
    df_transactions = pd.read_csv("./../data/raw/credit_card_transactions-ibm_v2.csv").tail(LIMIT)
    df_transactions = transform_columns_transactions(df_transactions)
    df_transactions.to_parquet("./../data/processed/data_transactions.parquet", engine='fastparquet')

    df_trans_users = df_transactions.merge(df_users, how='left', on='ID_USER')
    df_complete = df_trans_users.merge(df_cards, how='left', on=['ID_USER', 'ID_CARD'])
    df_complete.to_parquet("./../data/processed/data_complete.parquet", engine='fastparquet')
    print('------------ data completed ------------')
    