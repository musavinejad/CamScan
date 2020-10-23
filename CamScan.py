import numpy as np
import matplotlib.pyplot as mpl
import matplotlib.animation as ani
from pylablib.aux_libs.file_formats import waveguide,cam
from pylablib.core.datatable import table
from pylablib.core.utils import files as file_utils, dictionary, plotting
from pylablib.core.fileio import loadfile, savefile
import os.path
import re
from pylablib import DataTable

#import progressbar

mpl.ioff()



def plot_tera(new_data,reader,center=(5,5),rngs=(3,3),save_name="tera_scan"):
    folder = "Tera_scans"
    # Create target Directory if don't exist
    if not os.path.exists(folder):
        os.mkdir(folder)
        print("Directory ", folder, " Created ")
    # create the path, where the video gets saved
    path = os.path.join(folder, save_name+".png")

    data=new_data.copy()
    frames=np.array(reader.read_all())
    fluor_trace=np.mean(np.mean(frames[:,center[0]-rngs[0]//2:center[0]+rngs[0]//2,center[1]-rngs[1]//2:center[1]+rngs[1]//2],axis=1),axis=1)
    data.c.append(fluor_trace,names="Fluor") #appends a new colum to data, new colum data is fluor_trace, name is "Fluor"
    waveguide.trim_jumps(data,jump_size=500*1e6,trim=3,x_column="Frequency")
    data=data.sort_by("Frequency")

    f=mpl.figure(figsize=(14,6))
    ax=f.add_subplot(111)
    ax.plot(data["Frequency"]/1e12,data["Fluor"])
    ax.set_xlim([382, 382.38])
    ax.set_xlabel("Frequency [THz]")
    ax.set_ylabel("Fluorescence [A. U.]")
    f.savefig(path,dpi=300)
    np.savetxt(save_name+"raw.txt" , data , delimiter=',')
    mpl.close(f)

def plot_all_pixel_centers(data,reader,name,rng=3,window=None):
    frame=reader[0]
    x_size=len(frame[:,0])
    y_size = len(frame[0,:])
    if window is not None:
        for i in np.arange(window[0],window[1],rng-1):
            for j in np.arange(window[2],window[3],rng-1):
                center=(i,j)
                plot_tera(data, reader, center=center, rngs=(rng, rng), save_name=name+"_mean_trace_center_x_{}_center_y_{}_".format(center[0],center[1]))
                print("center_x_{}_center_y_{}_".format(center[0],center[1]) + "saved.")

    else:
        for i in np.arange(1,x_size,rng-1):
            for j in np.arange(1,y_size,rng-1):
                center=(i,j)
                plot_tera(data, reader, center=center, rngs=(rng, rng), save_name=name+"_mean_trace_center_x_{}_center_y_{}".format(center[0],center[1]))
                print("center_x_{}_center_y_{}_".format(center[0], center[1]) + "saved.")

def max_bin_frames(reader,bin=10):
    ### takes a reader object and retuns a list of max-binned images ###
    frames_max_bin=[]
    for i in np.arange(reader.size()//bin):
        max_frame=reader[i*bin]
        for j in np.arange(bin):
            max_frame=np.max([max_frame,reader[i*bin+j]],axis=0)
        frames_max_bin.append(max_frame)
    return frames_max_bin

def get_differential_frames(frames):
    ### get the differential frames of a list of frames ###
    frames=np.array(frames)
    diff_frames=frames[1:,:,:]-frames[:-1,:,:]
    return diff_frames

def export_video(frames,fps=30,name="video.mp4"):
    folder="Video_new"
    # Create target Directory if don't exist
    if not os.path.exists(folder):
        os.mkdir(folder)
        print("Directory " , folder,  " Created ")
    # create the path, where the video gets saved
    else:
        print("Directory ", folder, " Already Exists. Saving in the same folder ... ")
    vidpath=os.path.join(folder,name)

    #Initialize the video Writer
    FFMpegWriter = ani.writers['ffmpeg']
    writer = FFMpegWriter(fps=fps)
    # prepare the figure
    f=mpl.figure()
    ax=f.add_subplot(111)
    img=ax.imshow(frames[0],vmin=np.min(frames[0]),vmax=np.max(frames[0]))
    with writer.saving(f, vidpath, 300): # whenever writer.grab_frame() is called it automatically saves a frame to the video
        for frame in frames:
            # update image
            img.set_data(frame[32:,:])
            writer.grab_frame()
    mpl.close(f)

def process(name):
    data=loadfile.load(name+".dat")
    reader=cam.CamReader(name+"_imagem.cam")
    #export_video(reader,fps=30, name=name+"_all_frames.mp4")
    binning_constant=10
    #max_binned_frames=max_bin_frames(reader, bin=binning_constant)
    #export_video(max_binned_frames, fps=15, name=name + "_frames_max_binned_{}.mp4".format(binning_constant))
    #diff_frames=get_differential_frames(max_binned_frames)
    #export_video(diff_frames, fps=15, name=name + "_frames_max_binned_{}_differential.mp4".format(binning_constant))
    plot_all_pixel_centers(data, reader, name, rng=6, window=[30, 90, 25, 90])

#molCenters = [[30,70],[35,32],[35,55] , [35,65] , [35,70] , [40,32], [40, 55], [40,70], [40,85], [45,45], [45,60], [45,63], [45,80], [45,85], [50,50], [50,64], [50,70] , [50,75] ,   ]
name = r"Crysta500ppm_3-4k-Tera_ND1_21mV_fineScan_100MHzps_hugescan"
process(name)
print("Processing finished!")