# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Exploración de ventas diarias por tienda
#
# Notebook de DEV sobre la muestra anonimizada. Se versiona como `.py` exportado con
# jupytext. El `.ipynb`, con sus salidas, no entra a Git.

# %%
import pandas as pd

ventas = pd.read_csv("../data/raw/ventas.csv", parse_dates=["fecha"])
ventas.head()

# %%
ventas.describe()

# %% [markdown]
# ## Ventas promedio por día de la semana

# %%
ventas.assign(dia=ventas["fecha"].dt.day_name()).groupby("dia")["ventas"].mean().sort_values()

# %% [markdown]
# ## Porcentaje de nulos por columna

# %%
ventas.isna().mean().mul(100).round(2)
