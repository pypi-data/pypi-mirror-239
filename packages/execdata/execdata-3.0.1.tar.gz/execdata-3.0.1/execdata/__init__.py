'''
Date         : 2022-10-25 15:44:41
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-11-03 11:03:56
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\__init__.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''

from execdata import templateproj
from .data_preprocessing.data_conversion import *
from .data_preprocessing import _data_mining, _data_preprocess, _standardization
# from execdata.standardization import encode
from .data_modeling import _model_evaluate
from .analysis_graph import _data_analysis_graph
