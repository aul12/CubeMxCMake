import sys
import re

if len(sys.argv) != 4:
    print("usage: cubeMxCmake.py template.txt project.ioc CMakeLists.txt")
    exit()

templateFName = sys.argv[1]
projectConfigFName = sys.argv[2]
outputFName = sys.argv[3]

projectContent = "".join(open(projectConfigFName, "r").readlines())
templateContent = "".join(open(templateFName, "r").readlines())

#ProjectManager.ProjectName
#PCC.Series (STM32L4)
#ProjectManager.DeviceId (STM32L432KCUx) maybe needs to be STM32L432xx
projectNameMatcher = re.search("ProjectManager\\.ProjectName=(.+)", projectContent)
seriesMatcher = re.search("PCC\\.Series=(.+)", projectContent)
deviceIdMatcher = re.search("ProjectManager.DeviceId=(.+)", projectContent)

if projectNameMatcher is None:
    print("Field ProjectManager.ProjectName not found in config")
    exit()

if seriesMatcher is None:
    print("Field PCC.Series not found in config")
    exit()

if deviceIdMatcher is None:
    print("Field ProjectManager.DeviceId not found in config")
    exit()

projectName = projectNameMatcher.group(1)
series = seriesMatcher.group(1)
deviceId = deviceIdMatcher.group(1)
shortDeviceId = deviceId[0:len(series)+2]

print("ProjectName:\t%s\nSeries:\t\t\t%s\nDeviceId:\t\t%s" % (projectName, series, deviceId))

templateContent = templateContent.replace("${SERIES}", series)
templateContent = templateContent.replace("${PROJECT}", projectName)
templateContent = templateContent.replace("{SHORT_DEVICE_ID}", shortDeviceId)

outputFile = open(outputFName, "w")
outputFile.write(templateContent)
