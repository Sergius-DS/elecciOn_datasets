import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# crear funcion para transformar columnas en valores binarios
def categorizar_columnas(df, columnas):
    for columna in columnas:
        df[columna] = df[columna].apply(lambda x: 1 if x == 'SI' else 0).astype(int)
    return df[columnas].head()



# FUNCIÓN PARA VERFICAR FILAS

def verifica_consistencia_filas(df):

    """
    Comprueba si el contenido de las filas coincide con la descripción de dtypes del DataFrame.

    Args:
    df (pd.DataFrame): El DataFrame que se va a comprobar.

    Lo que será Retornado:
    pd.DataFrame: Un DataFrame con valores booleanos que indican si los valores de cada
    fila son coherentes con los tipos de datos de la columna.
    True indica coherencia, False indica incoherencia.
    """

    # Crea un Data Frame vacío para guardar los resultados
    result_df = pd.DataFrame(index=df.index, columns=df.columns, dtype=bool)

    # Recorre cada columna y fila para revisar consistencia
    for col in df.columns:
        # Verifica si el tipo de dato es numéric0 (int o float)
        is_numeric = pd.api.types.is_numeric_dtype(df[col].dtype)

        # Verifica la consistencia de cada fila en la columna actual
        if is_numeric:
            result_df[col] = pd.to_numeric(df[col], errors='coerce').notna()
        else:
            # Verifica que los datos son del tipo string, object
            result_df[col] = df[col] == df[col].astype('object')

    return result_df

# crear funcion para transformar columna a fecha
def columnas_a_fecha(df, columnas):
    for columna in columnas:
        df[columna] = pd.to_datetime(df[columna], format='%Y%m%d', errors='coerce')
    return df[columnas].head()

# Crear función para ver la frecuencia y porcentaje de los valores únicos de cada columna categórica
def valores_unicos(df, c: str):
    """
    Función para ver la frecuencia y porcentaje de los valores únicos de cada columna categórica
    """
    # Contar las frecuencias de los valores únicos
    frecuencias = df[c].dropna().value_counts()

    # Calcular el porcentaje para cada valor único
    total = frecuencias.sum()
    porcentajes = (frecuencias / total) * 100

    # Mostrar los valores únicos, sus frecuencias y porcentajes
    resultado = pd.DataFrame({
        'Frecuencia': frecuencias,
        'Porcentaje': porcentajes,
    })
    # Formatear la columna de porcentaje
    resultado['Porcentaje'] = resultado['Porcentaje'].map(lambda x: f"{x:.2f}%")

    print(resultado)

# Función para crear aplicar get dummies a variables categóricas
def dummies(df, column_name):
    """
    Crea variables Dummies a partir de una columna categórica
    Borra columna original
    Concatena las variables dummies al DataFrame original

    Ejemplo de uso:
    df = apply_get_dummies(df, 'Nombre_columna')
    """
    dummy = pd.get_dummies(df[column_name])
    df = df.drop(columns=[column_name])
    return pd.concat([df, dummy], axis=1)


def v_count_por_columna(df, columnas):
  # Iterar sobre cada columna categórica e imprimir value_counts()
  for col in columnas:
      print(f"Value counts for {col}:")
      print(ds[col].value_counts())
      print("\n")


def plot_categorical_columns_topn(df, column_names, top_n=10):
    """
    Plots the distribution of multiple categorical columns showing top N categories.

    Args:
        df: The pandas DataFrame containing the data.
        column_names: A list or Index of column names to plot.
        top_n: Number of top categories to display; others are grouped as 'Other'.
    """
    for column_name in column_names:
        num_unique = df[column_name].nunique()

        if num_unique > 15:
            print(f"Skipping column '{column_name}' due to high cardinality ({num_unique} categories).")
            continue  # Skip plotting for this column
            counts = df[column_name].value_counts()
            top_counts = counts.nlargest(top_n)
            other_count = counts.sum() - top_counts.sum()
            top_counts['Other'] = other_count
            num_unique = top_counts.size
        else:
            top_counts = df[column_name].value_counts()

        if num_unique <= 15:
            # Proceed with plotting as before
            if num_unique > 2:
                fig, ax = plt.subplots(figsize=(10, max(6, num_unique * 0.5)))
                ax.barh(top_counts.index, top_counts.values)
                ax.set_xlabel('Count')
                ax.set_ylabel(column_name)
                ax.set_title(f'Distribution of {column_name}')

                for i, v in enumerate(top_counts.values):
                    ax.text(v + max(top_counts.values)*0.01, i, str(v), va='center')
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(top_counts.index, top_counts.values)
                ax.set_xlabel(column_name)
                ax.set_ylabel('Count')
                ax.set_title(f'Distribution of {column_name}')

                for i, v in enumerate(top_counts.values):
                    ax.text(i, v + max(top_counts.values)*0.01, str(v), ha='center')

            plt.tight_layout()
            plt.show()

            print("\n" + "-"*40 + "\n")
        else:
            print(f"Skipping column '{column_name}' as it has more than 15 categories even after grouping.")


def plot_numerical_columns_histograma(df, column_names):
    for column_name in column_names:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df[column_name], kde=True, ax=ax)
        ax.set_xlabel(column_name)
        ax.set_ylabel('Frequency')
        ax.set_title(f'Distribution of {column_name}')
        plt.tight_layout()
        plt.show()
        #print("\n" + "-"*40 + "\n")


def plot_numerical_columns_vcount(df, column_names):
    for column_name in column_names:
        fig, ax = plt.subplots(figsize=(10, 6))
        value_counts = df[column_name].value_counts()
        value_counts.plot(kind='bar', ax=ax)

        # Annotate each bar with its value
        for p in ax.patches:
            ax.annotate(str(p.get_height()),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom')

        ax.set_xlabel(column_name)
        ax.set_ylabel('Frequency')
        ax.set_title(f'Distribution of {column_name}')
        plt.tight_layout()
        plt.show()
        #print("\n" + "-"*40 + "\n")

