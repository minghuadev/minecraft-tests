/*
 * Copyright (C) 2012 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration.
 * All Rights Reserved.
 */

package gov.nasa.worldwind;

import gov.nasa.worldwind.geom.Position;
import gov.nasa.worldwind.geom.Vec4;
import gov.nasa.worldwind.globes.Globe;

/**
 * @author tag
 * @version $Id: MyWind.java $
 */
public class MyWind
{
    private static final MyWind _inst = new MyWind();
    private static double _viewlat = 0, _viewlon = 0, _viewalt = 0;
    private static double _centlat = 0, _centlon = 0, _centalt = 0;
    private static double _heading = 0, _pitch = 0, _roll = 0;
    private static double _p1lat = 0, _p1lon = 0, _p1alt = 0, _p1rad = 0;
    private static double _p2lat = 0, _p2lon = 0, _p2alt = 0, _p2rad = 0;

    public static String getShowString()
    {
        int malt = (int) _inst._viewalt;
        int mmalt = (int)( (_inst._viewalt - malt) * 100);
        int ctrmalt = (int) _inst._centalt;
        int ctrmmalt = (int)( (_inst._centalt - ctrmalt) * 100);
        return String.format(
             "eye %7.2f %7.2f %,7d.%02d  ctr %7.2f %7.2f %,7d.%02d  z %d %d %d", 
                            _inst._viewlat, _inst._viewlon, malt, mmalt, 
                            _inst._centlat, _inst._centlon, ctrmalt, ctrmmalt, 
                            Math.round(_inst._heading), 
                            Math.round(_inst._pitch), 
                            Math.round(_inst._roll));
    }

    private static void setEyePosition(double lat, double lon, double alt)
    {   _inst._viewlat = lat; _inst._viewlon = lon; _inst._viewalt = alt;
    }
    private static void setCentPosition(double lat, double lon, double alt)
    {   _inst._centlat = lat; _inst._centlon = lon; _inst._centalt = alt;
    }
    private static void setBearing(double h, double p, double r)
    {   _inst._heading = h; _inst._pitch = p; _inst._roll = r;
    }
    
    public static void setDisplayViewParams(View eyeview)
    {
        double eyelat = 0, eyelon = 0, eyealt = 0;
        double centlat = 0, centlon = 0, centalt = 0;
        double bearingh = 0, bearingp = 0, bearingr = 0;
        if ( eyeview != null ) {
            Position eyepos = eyeview.getCurrentEyePosition();
            if ( eyepos != null ) {
                eyelat = eyepos.getLatitude().getDegrees();
                eyelon = eyepos.getLongitude().getDegrees();
                eyealt = eyepos.getAltitude();
            }
            Globe eyeglobe = eyeview.getGlobe();
            if ( eyeglobe != null ) {
                Vec4 eyev4 = eyeview.getCenterPoint();
                if ( eyev4 != null ) {
                    Position ctrpos = 
                                eyeglobe.computePositionFromPoint(eyev4);
                    if ( ctrpos != null ) {
                        centlat = ctrpos.getLatitude().getDegrees();
                        centlon = ctrpos.getLongitude().getDegrees();
                        //centalt = ctrpos.getAltitude();
                        centalt = eyeglobe.getElevation(
                              ctrpos.getLatitude(), ctrpos.getLongitude());
                    }
                }
            }
            bearingh = eyeview.getHeading().getDegrees();
            bearingp = eyeview.getPitch().getDegrees();
            bearingr = eyeview.getRoll().getDegrees();
        }
        MyWind.setEyePosition(eyelat, eyelon, eyealt);
        MyWind.setCentPosition(centlat, centlon, centalt);
        MyWind.setBearing(bearingh, bearingp, bearingr);
    }
}
