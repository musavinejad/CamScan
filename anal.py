import numpy as np
import matplotlib.pyplot as mpl
import matplotlib.animation as ani
from pylablib.aux_libs.file_formats import waveguide,cam
from pylablib.core.datatable import table
from pylablib.core.utils import files as file_utils, dictionary, plotting
from pylablib.core.fileio import loadfile, savefile
import os.path
import pandas as pd

name = "2.txt"
# data=loadfile.load(name+".dat")
# reader=cam.CamReader(name+"_imagem.cam").read_all()
# reader = np.asarray(reader)
dt = pd.read_csv(name, delimiter=" ")
type(dt)
