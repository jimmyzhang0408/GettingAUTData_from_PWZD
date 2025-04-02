import os
import clr
from matplotlib import pyplot as plt
clr.AddReference(os.path.join(os.getcwd(), "Interop.RDTiffDataFile.dll"))


from RDTiffDataFile import RDTiffDataFile



def open_file(file_path):
    file = RDTiffDataFile()

    # get the file name from the file path
    file_name = file_path.split('\\')[-1]
    print(f'Opening file:{file_name}')
    file.OpenFile(file_path)


    print(f'Channel Count is: {file.Channels.Count}')
    plt.figure(figsize=(15,10))
    for indexChannel in range(1, file.Channels.Count+1):

        channel = file.Channels[indexChannel]
        # print(dir(channel))
        name = channel.Name
        # print(f"[Channel No. {indexChannel}] Name: {channel.Name}", end=' ')
        # print(f"Mode: {channel.Mode}")
        # print("[Channel] PulserVoltage: %d" % channel.PulserVoltage)
        # print("[Channel] PulseWidth: %d" % channel.PulseWidth)
        # print("[Channel] Averaging: %d" % channel.Averaging)
        # print("[Channel] Compression: %d" % channel.Compression)
        # print("[Channel] ConditionalAScan: %d" % channel.ConditionalAScan)
        # print("[Channel] DigitizingFrequency: %d" % channel.DigitizingFrequency)
        # print(f"Type:{channel.Type}")
        # print('=======================================================================')
        beams = channel.Beams
        # print(dir(beams), beams.Count)

        beam = beams[1]
        gates = beam.Gates
        # print(dir(gates), gates.Count)
        # I only need to extract the gate with name is Gate Main (A-Scan)
        for gate_index in range(1,gates.Count+1):
            gate = gates[gate_index]
            if gate.Name == 'Gate Main (A-Scan)':
                break

        dataGroup = gate.DataGroups[1]
        # print(dir(dataGroup))
        
        DataAccess = dataGroup.DataAccess
        ScanQuantity = dataGroup.ScanQuantity
        IndexQuantity = dataGroup.IndexQuantity

        # print(dir(DataAccess))
        data = DataAccess.ReadData()
        fullLengthAscan_array = [data[i] for i in range(data.Length)]
        # print(f'Length of A-Scan: {len(fullLengthAscan_array)}', end=' ')
        # print(fullLengthAscan_array)

        # do the subplots
        plt.subplot(1,file.Channels.Count,indexChannel)
        # fullLengthAscan_array is the x-axis, and the y-axis is the range of the length currently
        # set up the line width to be 0.5
        plt.plot(fullLengthAscan_array, range(len(fullLengthAscan_array)), linewidth=0.5)
        # hide the axises tick labels
        plt.xticks([])
        plt.yticks([])
        plt.title(f'{indexChannel}')
    plt.tight_layout()
    plt.savefig(f'ExportedAUT_fig/{file_name}.png')
    plt.close()
    # plt.show()
    file.CloseFile()
    print("======")
    
if __name__ == "__main__":
    # get the file list and only get the rdt files
    source_path = 'ExportedRDT'
    file_list = os.listdir(source_path)
    print(file_list)
    for file in file_list:
        file_path = os.path.join(source_path, file)
        print(file_path)
        if file_path.endswith('.rdt'):
            open_file(file_path)






