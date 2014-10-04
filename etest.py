import exifread
from array import array


def convert_to_degrees(ifIdVal):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    print "Value to convert", ifIdVal

    value = []
    for i in range(30):
       value.append("")

    i = 0
    for val in ifIdVal.values:
        print "i:" + str(i) + " val is ", val
        value[i] = val
        i+=1

    for i in range(10):
       print "value is : ", value[i] 
       print "value is : ", value[i][0]

    print "degrees: ", float(value[0][0]) / float(value[0][1])

    return 0, 3
    #s = float(s0) / float(s1)
 
    #return d + (m / 60.0) + (s / 3600.0)
 


def get_lat_long(f):
    tags = exifread.process_file(f)

    for tag in tags.keys():

        if "GPS GPSLongitude" == tag:
            gps_long = tags[tag] 

        if "GPS GPSLatitude" == tag:
            gps_latt = tags[tag] 

        if "GPS GPSLongitudeRef" == tag:
            gps_long_ref = tags[tag] 
            #print "long ref", gps_long_ref

        if "GPS GPSLatitudeRef" == tag:
            gps_latt_ref = tags[tag] 
            print "latt ref", gps_latt_ref

    if gps_long and gps_latt and gps_long_ref and gps_latt_ref:
        lat = convert_to_degrees(gps_latt)
        if gps_latt_ref != "N":                     
            lat = 0 - lat
        lon = convert_to_degrees(gps_long)
        if gps_long_ref != "E":
            lon = 0 - lon
        return lat, lon

    return None, None


f = open("../GermanCemetery/IMG_5408-001.JPG", 'rb')

print get_lat_long(f)


#print "long ", gps_long
#print "latt ", gps_latt
#print "long ref", gps_long_ref
#print "latt ref", gps_latt_ref
#

