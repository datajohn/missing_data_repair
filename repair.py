# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# ![rmotr](https://i.imgur.com/jiPp4hj.png)
# <hr style="margin-bottom: 40px;">
# 
# <img src="https://user-images.githubusercontent.com/7065401/39117440-24199c72-46e7-11e8-8ffc-25c6e27e07d4.jpg"
#     style="width:300px; float: right; margin: 0 40px 40px 40px;"></img>
# 
# # Handling Missing Data with Pandas
# 
# pandas borrows all the capabilities from numpy selection + adds a number of convenient methods to handle missing values. Let's see one at a time:
# %% [markdown]
# ![separator2](https://i.imgur.com/4gX5WFr.png)
# 
# ## Hands on! 

# %%
import numpy as np
import pandas as pd

# %% [markdown]
# ### Pandas utility functions
# 
# Similarly to `numpy`, pandas also has a few utility functions to identify and detect null values:

# %%
pd.isnull(np.nan)


# %%
pd.isnull(None)


# %%
pd.isna(np.nan)


# %%
pd.isna(None)

# %% [markdown]
# The opposite ones also exist:

# %%
pd.notnull(None)


# %%
pd.notnull(np.nan)


# %%
pd.notna(np.nan)


# %%
pd.notnull(3)

# %% [markdown]
# These functions also work with Series and `DataFrame`s:

# %%
pd.isnull(pd.Series([1, np.nan, 7]))


# %%
pd.notnull(pd.Series([1, np.nan, 7]))


# %%
pd.isnull(pd.DataFrame({
    'Column A': [1, np.nan, 7],
    'Column B': [np.nan, 2, 3],
    'Column C': [np.nan, 2, np.nan]
}))

# %% [markdown]
# ![separator1](https://i.imgur.com/ZUWYTii.png)
# 
# ### Pandas Operations with Missing Values
# 
# Pandas manages missing values more gracefully than numpy. `nan`s will no longer behave as "viruses", and operations will just ignore them completely:

# %%
pd.Series([1, 2, np.nan]).count()


# %%
pd.Series([1, 2, np.nan]).sum()


# %%
pd.Series([2, 2, np.nan]).mean()

# %% [markdown]
# ### Filtering missing data
# 
# As we saw with numpy, we could combine boolean selection + `pd.isnull` to filter out those `nan`s and null values:

# %%
s = pd.Series([1, 2, 3, np.nan, np.nan, 4])


# %%
pd.notnull(s)


# %%
pd.isnull(s)


# %%
pd.notnull(s).sum()


# %%
pd.isnull(s).sum()


# %%
s[pd.notnull(s)]

# %% [markdown]
# But both `notnull` and `isnull` are also methods of `Series` and `DataFrame`s, so we could use it that way:

# %%
s.isnull()


# %%
s.notnull()


# %%
s[s.notnull()]

# %% [markdown]
# ![separator1](https://i.imgur.com/ZUWYTii.png)
# 
# ### Dropping null values
# %% [markdown]
# Boolean selection + `notnull()` seems a little bit verbose and repetitive. And as we said before: any repetitive task will probably have a better, more DRY way. In this case, we can use the `dropna` method:

# %%
s


# %%
s.dropna()

# %% [markdown]
# ### Dropping null values on DataFrames
# 
# You saw how simple it is to drop `na`s with a Series. But with `DataFrame`s, there will be a few more things to consider, because you can't drop single values. You can only drop entire columns or rows. Let's start with a sample `DataFrame`:

# %%
df = pd.DataFrame({
    'Column A': [1, np.nan, 30, np.nan],
    'Column B': [2, 8, 31, np.nan],
    'Column C': [np.nan, 9, 32, 100],
    'Column D': [5, 8, 34, 110],
})


# %%
df


# %%
df.shape


# %%
df.info()


# %%
df.isnull()


# %%
df.isnull().sum()

# %% [markdown]
# The default `dropna` behavior will drop all the rows in which _any_ null value is present:

# %%
df.dropna()

# %% [markdown]
# In this case we're dropping **rows**. Rows containing null values are dropped from the DF. You can also use the `axis` parameter to drop columns containing null values:

# %%
df.dropna(axis=1)  # axis='columns' also works

# %% [markdown]
# In this case, any row or column that contains **at least** one null value will be dropped. Which can be, depending on the case, too extreme. You can control this behavior with the `how` parameter. Can be either `'any'` or `'all'`:

# %%
df2 = pd.DataFrame({
    'Column A': [1, np.nan, 30],
    'Column B': [2, np.nan, 31],
    'Column C': [np.nan, np.nan, 100]
})


# %%
df2


# %%
df.dropna(how='all')


# %%
df.dropna(how='any')  # default behavior

# %% [markdown]
# You can also use the `thresh` parameter to indicate a _threshold_ (a minimum number) of non-null values for the row/column to be kept:

# %%
df


# %%
df.dropna(thresh=3)


# %%
df.dropna(thresh=3, axis='columns')

# %% [markdown]
# ![separator1](https://i.imgur.com/ZUWYTii.png)
# 
# ### Filling null values
# 
# Sometimes instead than dropping the null values, we might need to replace them with some other value. This highly depends on your context and the dataset you're currently working. Sometimes a `nan` can be replaced with a `0`, sometimes it can be replaced with the `mean` of the sample, and some other times you can take the closest value. Again, it depends on the context. We'll show you the different methods and mechanisms and you can then apply them to your own problem.

# %%
s

# %% [markdown]
# **Filling nulls with a arbitrary value**

# %%
s.fillna(0)


# %%
s.fillna(s.mean())


# %%
s

# %% [markdown]
# **Filling nulls with contiguous (close) values**
# 
# The `method` argument is used to fill null values with other values close to that null one:

# %%
s.fillna(method='ffill')


# %%
s.fillna(method='bfill')

# %% [markdown]
# This can still leave null values at the extremes of the Series/DataFrame:

# %%
pd.Series([np.nan, 3, np.nan, 9]).fillna(method='ffill')


# %%
pd.Series([1, np.nan, 3, np.nan, np.nan]).fillna(method='bfill')

# %% [markdown]
# ### Filling null values on DataFrames
# 
# The `fillna` method also works on `DataFrame`s, and it works similarly. The main differences are that you can specify the `axis` (as usual, rows or columns) to use to fill the values (specially for methods) and that you have more control on the values passed:

# %%
df


# %%
df.fillna({'Column A': 0, 'Column B': 99, 'Column C': df['Column C'].mean()})


# %%
df.fillna(method='ffill', axis=0)


# %%
df.fillna(method='ffill', axis=1)

# %% [markdown]
# ![separator1](https://i.imgur.com/ZUWYTii.png)
# 
# ### Checking if there are NAs
# 
# The question is: Does this `Series` or `DataFrame` contain any missing value? The answer should be yes or no: `True` or `False`. How can you verify it?
# 
# **Example 1: Checking the length**
# 
# If there are missing values, `s.dropna()` will have less elements than `s`:

# %%
s.dropna().count()


# %%
missing_values = len(s.dropna()) != len(s)
missing_values

# %% [markdown]
# There's also a `count` method, that excludes `nan`s from its result:

# %%
len(s)


# %%
s.count()

# %% [markdown]
# So we could just do:

# %%
missing_values = s.count() != len(s)
missing_values

# %% [markdown]
# **More Pythonic solution `any`**
# 
# The methods `any` and `all` check if either there's `any` True value in a Series or `all` the values are `True`. They work in the same way as in Python:

# %%
pd.Series([True, False, False]).any()


# %%
pd.Series([True, False, False]).all()


# %%
pd.Series([True, True, True]).all()

# %% [markdown]
# The `isnull()` method returned a Boolean `Series` with `True` values wherever there was a `nan`:

# %%
s.isnull()

# %% [markdown]
# So we can just use the `any` method with the boolean array returned:

# %%
pd.Series([1, np.nan]).isnull().any()


# %%
pd.Series([1, 2]).isnull().any()


# %%
s.isnull().any()

# %% [markdown]
# A more strict version would check only the `values` of the Series:

# %%
s.isnull().values


# %%
s.isnull().values.any()

# %% [markdown]
# ![separator2](https://i.imgur.com/4gX5WFr.png)

