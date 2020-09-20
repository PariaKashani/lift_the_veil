import sys
import os
import gpxpy
import gpxpy.gpx


def clean_gpx_file(file_name):
    # file_name : gpx_file(with complete path)
    # return : name of created file
    # at this stage, due to have n/a fields we cannot use 'pygpx' to open this file
    # replace n/a with 0
    fin = open(file_name, "rt")
    data = fin.read()
    fin.close()
    data = data.replace('n/a', '0')
    fout = open(file_name, "wt")
    fout.write(data)
    fout.close()
    # read the file with gpxpy
    gpx_file = open(file_name, 'r')
    gpx = gpxpy.parse(gpx_file)
    # find 0 lat/lon fields and fill them by
    # interpolate between geometries around them
    wpts_len = len(gpx.waypoints)
    wpts = gpx.waypoints
    i = 1
    last_valid_lat = float(wpts[0].latitude)
    last_valid_lon = float(wpts[0].longitude)
    while i < wpts_len:
        j = 1
        lat_1 = float(wpts[i].latitude)
        lon_1 = float(wpts[i].longitude)
        if lat_1 == 0:
            lat_2 = 0
            lon_2 = 0
            while (j + i) < wpts_len and lat_2 == 0:
                lat_2 = float(wpts[i + j].latitude)
                lon_2 = float(wpts[i + j].longitude)
                j += 1
            lat_offset = (lat_2 - last_valid_lat) / j
            lon_offset = (lon_2 - last_valid_lon) / j
            for k in range(j - 1):
                gpx.waypoints[k + i].latitude = str(last_valid_lat + (k + 1) * lat_offset)
                # print(gpx1.waypoints[k+i].latitude, k)
                gpx.waypoints[k + i].longitude = str(last_valid_lon + (k + 1) * lon_offset)
            # print(gpx1.waypoints[i+1].latitude,i)
            last_valid_lat = lat_2
            last_valid_lon = lon_2
        else:
            last_valid_lat = lat_1
            last_valid_lon = lon_1
        i += j

    # save new file
    new_file = open(file_name[:-4]+'_cleaned.gpx', 'w')
    new_file.write(gpx.to_xml())
    new_file.close()
    # remove last file
    gpx_file.close()
    os.remove(file_name)
    return file_name[:-4]+'_cleaned.gpx'


if __name__ == "__main__":
    clean_gpx_file(sys.argv[1])