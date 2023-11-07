""" Chart Serie type """
from enum import Enum


class ChartDataSerieType(Enum):
  """
  Chart data serie type
  """
  NONE = None
  LINE = 'line'
  AREA = 'area'
  SCATTER = 'scatter'
