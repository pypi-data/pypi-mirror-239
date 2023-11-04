import pandas as pd

nombres_datasets = [
    "01_original",
    "01_producto_estrella",
    "01_productos_todos",
    "01_por_cliente",
    "maestro_productos",
]


def get_nombres_datasets():
    return nombres_datasets


def get_dataset(dataset_name):
    if dataset_name not in nombres_datasets:
        raise ValueError(
            f"Dataset not found. Usar uno de los siguientes: {nombres_datasets}"
        )

    df = None

    if dataset_name == "01_producto_estrella":
        df = pd.read_csv("empresa4/datasets/tb_sellout_01_producto_estrella.csv")

    elif dataset_name == "01_productos_todos":
        df = pd.read_csv("empresa4/datasets/tb_sellout_01_productos_todos.csv")

    elif dataset_name == "01_por_cliente":
        df = pd.read_csv("empresa4/datasets/tb_sellout_01_por_cliente.csv")

    elif dataset_name == "01_original":
        df = pd.read_csv("empresa4/datasets/tb_sellout_01_original.csv")

    elif dataset_name == "maestro_productos":
        df = pd.read_csv("empresa4/datasets/maestro_productos.csv")

    return df
