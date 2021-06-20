# -*- coding: utf-8 -*-

import micropyGPS
import threading
import time
from staticmap import StaticMap, CircleMarker
from staticmap import Line
import numpy as np
import sys

def cal_rho(lon_a,lat_a,lon_b,lat_b):
    ra=6378.140  # equatorial radius (km)
    rb=6356.755  # polar radius (km)
    F=(ra-rb)/ra # flattening of the earth
    rad_lat_a=np.radians(lat_a)
    rad_lon_a=np.radians(lon_a)
    rad_lat_b=np.radians(lat_b)
    rad_lon_b=np.radians(lon_b)
    pa=np.arctan(rb/ra*np.tan(rad_lat_a))
    pb=np.arctan(rb/ra*np.tan(rad_lat_b))
    xx=np.arccos(np.sin(pa)*np.sin(pb)+np.cos(pa)*np.cos(pb)*np.cos(rad_lon_a-rad_lon_b))
    c1=(np.sin(xx)-xx)*(np.sin(pa)+np.sin(pb))**2/np.cos(xx/2)**2
    c2=(np.sin(xx)+xx)*(np.sin(pa)-np.sin(pb))**2/np.sin(xx/2)**2
    dr=F/8*(c1-c2)
    rho=ra*(xx+dr)
    return rho



# 以下メイン
def main():
    point = []

    gps = micropyGPS.MicropyGPS(9,'dd') 
    assert gps.start_logging('test.txt', mode="new")
    # assert gps.write_log('micropyGPS test log\n')
    # f = open('FILE210312-223327-000860-N.NMEA', 'r')
    f = open(sys.argv[1], 'r')
    print(sys.argv[1])

    while True:
        data = f.readline()
        # EofCheck
        if not data:
            break
        if data.startswith('<EOF/>') == True:
            break;
        #print (data)
        #if data.startswith('$GPGSV') == True:
        for y in data:
            #$ print(y)
            gps.update(y)
        # print('UTC Timestamp:', gps.timestamp)
        # print( gps.fix_time)
        # print(gps.latitude_string(), gps.longitude_string())
        # print( "[%2.8f, %2.8f]" % (gps.latitude [0], gps.longitude[0]))
        if gps.latitude [0] != 0 or gps.longitude[0] != 0:
            point.append( [gps.latitude [0], gps.longitude[0]] )
        # print(gps.speed_string('kph'))

    f.close()

    assert gps.stop_logging()

    map = StaticMap(512, 512)

    # print(point)
    # print( "map = [%2.8f, %2.8f]" % (point[0][0],point[0][1]))
    for ii in range(len(point) - 1):
        map.add_line(Line(((point[ii][1],point[ii][0]), (point[ii+1][1],point[ii+1][0])), 'blue', 3))
    p2 = np.mean(point, axis=0)

    marker_outline = CircleMarker((point[0][1],point[0][0]), 'white', 18)
    marker = CircleMarker((point[0][1],point[0][0]), '#FF3600', 12)
    map.add_marker(marker_outline)
    map.add_marker(marker)

    end_num = len(point) - 1
    marker_outline = CircleMarker((point[end_num][1],point[end_num][0]), 'white', 18)
    marker = CircleMarker((point[end_num][1],point[end_num][0]), '#0036FF', 12)
    map.add_marker(marker_outline)
    map.add_marker(marker)

    # map level
    p_min = np.min(point, axis=0)
    p_max = np.max(point, axis=0)
    # 2点間から距離を取得
    rho = cal_rho(p_min[1], p_min[0], p_max[1], p_max[0])
    print( rho)
    print(p2)
    p_sub = p_max - p_min
    print(p_sub)

    lev_sum  = rho
    print(lev_sum)
    # 最大1分間に5km(時速300km)で計算
    lev = int(((5.0 - lev_sum) * (7.5/5.0)) + 9)
    print(lev)
    image = map.render(zoom=lev, center=[p2[1],p2[0]])
    image.save(sys.argv[1] + '_map.png')

if __name__ == "__main__":
    main()


