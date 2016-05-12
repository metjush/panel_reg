# Panel Data Regression Methods in Python

This repository implements basic panel data regression methods (fixed effects, first differences) in Python, plus some other panel data utilities.

It is built on `numpy`, `pandas` and `statsmodels`.

## Wrapper Object

All functionality is neatly wrapped inside one object: `PanelReg()`. This wrapper class provides quick access to all other classes and methods, 
so you only need to import one class:
  
`from panel_reg import PanelReg`
 
Then, everything else then is implemented can be accessed from this object:
  
- Panel Builder: `PanelReg().build()`
- Fixed Effecst: `PanelReg().fe()`
- First Differences: `PanelReg().fd()`

Each method returns the object (e.g. `FixedEffects`), which you then instantiate based on the documention below.

## Fixed Effects

The `FixedEffects` class implements a standard fixed effects linear regression:

![Fixed Effects Model](http://www.codecogs.com/gif.latex?y_{it} = x_{it} \beta + a_i ( + d_t ) + u_{it})

To remove the unit-level effect `a` (and the time effect `d`), we demean the data:

![Unit mean](http://www.codecogs.com/gif.latex?y^'_i = \frac{\sum_{t}y_{it}}{T})

![Time mean](http://www.codecogs.com/gif.latex?y^'_t = \frac{\sum_{i}y_{it}}{n})

![Overall mean](http://www.codecogs.com/gif.latex?y^{''} = \frac{\sum_{t,i}y_{it}}{nT})

## First Differences

## Panel Builder

The `PanelBuilder` class is written to help you create a `pandas.Panel` from your data, which can then be passed into 
one of the estimation classes. The object instance takes no argument when created:
 
`pb = PanelBuilder()`

### pandas Panel

A `pandas.Panel` instance is essentially a 3D dataset. The first axis is called `item` (or `entity`, i.e. the 
units that we are following over time). The second axis is called `major` and is generally used for specifying time. 
The third axis is called `minor` and it refers to the actual variables we are measuring.

For more information and API reference for `pandas.Panel`, see: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Panel.html

### Naming dimensions

With the `PanelBuilder`, you can first only name/specify the three axes (without passing any data). The following methods
implement this:

```python
pb.specify_times(times)  # Specify the time dimension
pb.specify_entities(entities)  # Specify the entity/unit dimension
pb.specify_variables(variables)  # Specift the variable dimension
```

Where the argument passed into each of these methods is an array-like structure of unique names in that dimension.
 
For example, if my panel consisted of all years between 1960 and 2000, I could specify it as follows:

```python
years = np.arange(1960,2001)  # Create a numpy array of integers between 1960 and 2000 (inclusive), could also use range()
pb.specify_times(times)  # set the times
# > 'Time dimension set to size 41'
```

### Passing a 3D numpy array

As a `pandas.Panel` is just a "named"/"indexed" 3D `numpy.NDArray`, the `PanelBuilder` supports creation of the panel
from a multidimensional `numpy` array or standard Python `list`. This is done with the `pb.panel_from_array(multiarray)`
method, where `multiarray` is either a 3D `numpy` array or a 3D `list`.
  
When dimensions/index names have been passed before passing the 3D array, the dimensions of the array must match those
supplied when naming. You can also name the dimensions afterwards, but then again, the dimensions must match those of the
supplied array.

The dimensions of the array are expected to be `(entities, times, variables)`. 

### Passing a dictionary of slices by time

### Passing a dictionary of slices by entity

### Creating the panel

