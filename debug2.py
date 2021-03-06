## add local modules
import sys, os
sys.path.insert(0, os.path.join(sys.path[0], 'modules'))

## imports
from mne import read_epochs
from evaluation import EEGNet, get_fold, add_kernel_dim, onehot, test_rest_split, test_model, stratify, test_model_confidence
from preparation import separateXY, load_comp, prep_comp, epoch_comp, loadall_pilot, epoch_pilot, readall_comp_epochs, comp_channel_map3, load_pilot
from pathlib import Path
from tensorflow.python.keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split, StratifiedKFold

## constants
CLASSES = 3
FOLDS = 5
REPEATS = 10
GOODS = ['FC3','C3','CP3','Fz','Cz','POz','FC4','C4','CP4']
T_RANGE = [0.5, 2.5]
RESAMPLE = 125
KERNELS = 1
EPOCHS = 200
TRANSFER_EPOCHS = 300
LO_FREQ = 2.
HI_FREQ = 32.
WEIGHT_PATH = f"weights"
CONFIDENCE = 0.66


### script start
# _compX, _compY = epoch_comp(prep_comp(load_comp(True), comp_channel_map3, GOODS, l_freq=LO_FREQ, h_freq=HI_FREQ), CLASSES, resample=RESAMPLE, trange=T_RANGE)
# _pilotX, _pilotY = epoch_pilot(load_pilot('data/rivet/raw/pilot2/BCI_imaginedmoves_3class_7-4-21.vhdr'), CLASSES, GOODS, resample=RESAMPLE, trange=T_RANGE, l_freq=LO_FREQ, h_freq=HI_FREQ)

from mne import pick_types, Epochs, events_from_annotations, create_info
from mne.io import RawArray
from integration import stream_channels, GOODS
pilot = load_pilot('data/rivet/raw/pilot2/BCI_imaginedmoves_3class_7-4-21.vhdr')
picks = pick_types(pilot.info, meg=False, eeg=True, stim=False, eog=False)
data = pilot.get_data(picks=picks)
print(data.shape)

stream_info = create_info(pilot.ch_names[:-3], 500, 'eeg')
raw = RawArray(data=data, info=stream_info)
print(raw)

pilot = pilot.filter(LO_FREQ, HI_FREQ, method='fir', fir_design='firwin', phase='zero')
raw = raw.filter(LO_FREQ, HI_FREQ, method='fir', fir_design='firwin', phase='zero')
# raw = raw.crop(tmin=2.)

pilot = pilot.resample(125)
raw = raw.resample(125)

pilot_data = pilot.get_data(picks=sorted(GOODS)) * 1000
raw_data = raw.get_data(picks=sorted(GOODS)) * 1000


# print(pilot.ch_names)
# print(stream_channels)
print(pilot_data.shape)
print(raw_data.shape)
print(sorted(GOODS))

import numpy as np
from matplotlib import pyplot as plt
t = np.arange(0, 100)

# plt.plot(t, pilot_data[0,0:100], t, raw_data[0,0:100])
fig, axs = plt.subplots(8, 8)
print(axs.shape)
p = 0
for i in range(3):
    for j in range(3):
        # , t, realtime[p]
        axs[i, j].plot(t, pilot_data[p,0:100], t, raw_data[p,0:100])
        # plt.plot(t, _pilotX[0][p], t, realtime[p])
        p += 1
        # plt.show()

fig.tight_layout()
plt.show()


# realtime = raw.get_data(picks=sorted(GOODS))*1000





# t = np.arange(0, 2, 0.008)
# fig, axs = plt.subplots(3, 3)

# p = 0
# for i in range(3):
#     for j in range(3):
#         # , t, realtime[p]
#         axs[i, j].plot(t, _pilotX[4][p], t, realtime[p])
#         # plt.plot(t, _pilotX[0][p], t, realtime[p])
#         p += 1
#         # plt.show()

# # fig.tight_layout()
# plt.show()



