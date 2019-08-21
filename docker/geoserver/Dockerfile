FROM winsent/geoserver:2.9
LABEL maintainer="Damien Ayers <damien@omad.net>"

ENV http_proxy http://10.0.2.2:3128
ENV https_proxy https://10.0.2.2:3128

# Get ImagePyramid plugin
RUN wget -c http://downloads.sourceforge.net/project/geoserver/GeoServer/$GEOSERVER_VERSION/extensions/geoserver-$GEOSERVER_VERSION-pyramid-plugin.zip -O ~/geoserver-pyramid-plugin.zip &&\
    unzip -o ~/geoserver-pyramid-plugin.zip -d /opt/geoserver/webapps/geoserver/WEB-INF/lib/ && \
    rm ~/geoserver-pyramid-plugin.zip


# Get NetCDF plugin
RUN wget -c http://downloads.sourceforge.net/project/geoserver/GeoServer/$GEOSERVER_VERSION/extensions/geoserver-$GEOSERVER_VERSION-netcdf-plugin.zip -O ~/geoserver-netcdf-plugin.zip &&\
    unzip -o ~/geoserver-netcdf-plugin.zip -d /opt/geoserver/webapps/geoserver/WEB-INF/lib/ && \
    rm ~/geoserver-netcdf-plugin.zip



# Get WCS 2.0 EO plugin
RUN wget -c http://downloads.sourceforge.net/project/geoserver/GeoServer/$GEOSERVER_VERSION/extensions/geoserver-$GEOSERVER_VERSION-wcs2_0-eo-plugin.zip -O ~/geoserver-wcs2_0-eo-plugin.zip &&\
    unzip -o ~/geoserver-wcs2_0-eo-plugin.zip -d /opt/geoserver/webapps/geoserver/WEB-INF/lib/ && \
    rm ~/geoserver-wcs2_0-eo-plugin.zip
