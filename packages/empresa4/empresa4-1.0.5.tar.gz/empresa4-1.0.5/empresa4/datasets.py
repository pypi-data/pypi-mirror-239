import pandas as pd

nombres_datasets = ["01_producto_estrella", "01_productos_todos", "01_por_cliente"]


def get_nombres_datasets():
    return nombres_datasets


def get_dataset(dataset_name):
    df = None

    if dataset_name == "01_producto_estrella":
        df = pd.read_csv("./datasets/tb_sellout_01_producto_estrella.csv")

    elif dataset_name == "01_productos_todos":
        df = pd.read_csv("./datasets/tb_sellout_01_productos_todos.csv")

    elif dataset_name == "01_por_cliente":
        df = pd.read_csv("./datasets/tb_sellout_01_por_cliente.csv")

    else:
        raise Exception(
            f"Dataset not found. Usar uno de los siguientes: {nombres_datasets}"
        )

    return df
