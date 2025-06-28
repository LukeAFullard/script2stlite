import pandas as pd
import numpy as np
def random_pandas_dataframe():
    return pd.DataFrame(np.random.randint(0, 100, size=(5, 3)), columns=['ColA', 'ColB', 'ColC'])
    
    