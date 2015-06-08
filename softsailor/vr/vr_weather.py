class Weather:
    def load(self, settings):
        pass

    def wind_uri(self, latitude, longitude, dts): 
        # 10 is the tile size obtained from <TAILLE_ZONE_VENTS> in xml
        # retrieved 
        # by ?service=GetConfigFlash
        lat_i = int((latitude // 10) * 10 + 10)
        lon_i = int((longitude // 10) * 10)
        return lat_i,lon_i, wind_root + '/%d/meteo_%s_%d_%d.xml' % (lat_i, dts, lon_i, lat_i)

