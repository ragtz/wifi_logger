import numpy as np
import pickle
import rosbag
import sys

navdata = '/ardrone/navdata'
pose = '/ardrone/predictedPose'
channel = '/channel_quality'

def saveData(bag, out):
    bag = rosbag.Bag(bag)

    data = {'dynamics': {'t': [],
                         'v': [],
                         'a': []},
            'pose': {'t': [],
                     'x': []},
            'channel': {'t': [],
                        'q': []}}

    for topic, msg, t in bag.read_messages(topics=[navdata, pose, channel]):
        t = t.to_sec()

        if topic == navdata:
            data['dynamics']['t'].append(t)
            data['dynamics']['v'].append([msg.vx, msg.vy, msg.vz])
            data['dynamics']['a'].append([msg.ax, msg.ay, msg.az])

        elif topic == pose:
            data['pose']['t'].append(t)
            data['pose']['x'].append([msg.x, msg.y, msg.z])

        else:
            data['channel']['t'].append(t)
            data['channel']['q'].append(msg.signal_level)

    bag.close()

    data['dynamics']['t'] = np.array(data['dynamics']['t'])
    data['dynamics']['v'] = np.array(data['dynamics']['v'])
    data['dynamics']['a'] = np.array(data['dynamics']['a'])

    data['pose']['t'] = np.array(data['pose']['t'])
    data['pose']['x'] = np.array(data['pose']['x'])

    data['channel']['t'] = np.array(data['channel']['t'])
    data['channel']['q'] = np.array(data['channel']['q'])

    pickle.dump(data, open(out, 'w'))

if __name__ == '__main__':
    saveData(sys.argv[1], sys.argv[2])

