import unittest
import pandas as pd
from main_etl import clean_columns_names, manage_duplicates

class TestCleanColumns(unittest.TestCase):
    def test_clean_columns(self):
        # Definir las columnas de entrada
        columns = ["Columna 1", "Columna 2", "ColuMna 3"]
        
        # Ejecutar la función clean_columns()
        result = clean_columns_names(columns)
        
        # Verificar el resultado esperado
        expected_result = ["COLUMNA_1", "COLUMNA_2", "COLUMNA_3"]
        self.assertEqual(result, expected_result)


class TestManageDuplicates(unittest.TestCase):
    def test_manage_duplicates(self):
        # Definir el DataFrame de entrada
        data = {'col1': [1, 2, 3, 4, 4, 5],
                'col2': ['a', 'b', 'c', 'd', 'd', 'e']}
        df = pd.DataFrame(data)
        
        # Ejecutar la función manage_duplicates()
        result = manage_duplicates(df, 'mi_dataframe')
        
        # Verificar el resultado esperado
        expected_result = pd.DataFrame({'col1': [1, 2, 3, 4, 5],
                                        'col2': ['a', 'b', 'c', 'd', 'e']})
        self.assertTrue(result.equals(expected_result))


if __name__ == '__main__':
    unittest.main()