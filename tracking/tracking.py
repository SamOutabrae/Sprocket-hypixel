def trackContains(workingDirectory, uuid):
    f = open(workingDirectory + "/data/trackedplayers.txt", "r")
    data = f.readlines()
    for i in data:
        if((uuid + "\n") == i):
            return True
    return False


def trackAdd(workingDirectory, uuid):
    f = open(workingDirectory + "/data/trackedplayers.txt", "a")
    f.write(uuid + "\n")
    return True


def trackRemove(workingDirectory, uuid):
    f = open(workingDirectory + "/data/trackedplayers.txt", "r")
    data = f.readlines()
    f.close()

    updatedData = []
    for i in data:
        if(i == (uuid + "\n")):
            continue
        
        updatedData.append(i)

    f = open(workingDirectory + "/data/trackedplayers.txt", "w")
    data = f.writelines(updatedData)
    f.close()

    return True