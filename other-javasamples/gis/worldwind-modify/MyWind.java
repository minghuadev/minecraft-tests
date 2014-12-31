/*
 * Copyright (C) 2012 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration.
 * All Rights Reserved.
 */

package gov.nasa.worldwind;

/**
 * @author tag
 * @version $Id: MyWind.java $
 */
public class MyWind
{
    private static final MyWind _inst = new MyWind();
    private static double _viewlat = 0, _viewlon = 0, _viewalt = 0;
    private static double _centlat = 0, _centlon = 0, _centalt = 0;
    private static double _p1lat = 0, _p1lon = 0, _p1alt = 0, _p1rad = 0;
    private static double _p2lat = 0, _p2lon = 0, _p2alt = 0, _p2rad = 0;

    public static String getShowString()
    {
        int malt = (int) _inst._viewalt;
        int mmalt = (int)( (_inst._viewalt - malt) * 1000);
        int ctrmalt = (int) _inst._centalt;
        int ctrmmalt = (int)( (_inst._centalt - ctrmalt) * 1000);
        return String.format(
               " -- eye %7.4f %7.4f %,7d.%03d -- ctr %7.4f %7.4f %,7d.%03d -- ", 
                            _inst._viewlat, _inst._viewlon, malt, mmalt, 
                            _inst._centlat, _inst._centlon, ctrmalt, ctrmmalt );
    }

    public static void setEyePosition(double lat, double lon, double alt) 
    {
        _inst._viewlat = lat; _inst._viewlon = lon; _inst._viewalt = alt;
    }
    
    public static void setCentPosition(double lat, double lon, double alt) 
    {
        _inst._centlat = lat; _inst._centlon = lon; _inst._centalt = alt;
    }
}
