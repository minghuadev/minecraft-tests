/*
 * Copyright (C) 2012 United States Government as represented by the Administrator of the
 * National Aeronautics and Space Administration.
 * All Rights Reserved.
 */
package gov.nasa.worldwindx.examples;

import gov.nasa.worldwind.*;
import gov.nasa.worldwind.event.*;
import gov.nasa.worldwind.avlist.*;
import gov.nasa.worldwind.geom.*;
import gov.nasa.worldwind.layers.*;
import gov.nasa.worldwind.render.*;
import gov.nasa.worldwind.view.orbit.BasicOrbitView;
import static gov.nasa.worldwindx.examples.ViewIteration.AppFrame.path;

import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;
import java.beans.*;
import java.util.*;

/**
 * A utility class to interactively build a polyline. When armed, the class monitors mouse events and adds new positions
 * to a polyline as the user identifies them. The interaction sequence for creating a line is as follows: <ul> <li> Arm
 * the line builder by calling its {@link #setArmed(boolean)} method with an argument of true. </li> <li> Place the
 * cursor at the first desired polyline position. Press and release mouse button one. </li> <li> Press button one near
 * the next desired position, drag the mouse to the exact position, then release the button. The proposed line segment
 * will echo while the mouse is dragged. Continue selecting new positions this way until the polyline contains all
 * desired positions. </li> <li> Disarm the <code>LineBuilder</code> object by calling its {@link #setArmed(boolean)}
 * method with an argument of false. </li> </ul>
 * <p/>
 * While the line builder is armed, pressing and immediately releasing mouse button one while also pressing the control
 * key (Ctl) removes the last position from the polyline. </p>
 * <p/>
 * Mouse events the line builder acts on while armed are marked as consumed. These events are mouse pressed, released,
 * clicked and dragged. These events are not acted on while the line builder is not armed. The builder can be
 * continuously armed and rearmed to allow intervening maneuvering of the globe while building a polyline. A user can
 * add positions, pause entry, maneuver the view, then continue entering positions. </p>
 * <p/>
 * Arming and disarming the line builder does not change the contents or attributes of the line builder's layer. </p>
 * <p/>
 * The polyline and a layer containing it may be specified when a <code>LineBuilder</code> is constructed. </p>
 * <p/>
 * This class contains a <code>main</code> method implementing an example program illustrating use of
 * <code>LineBuilder</code>. </p>
 *
 * @author tag
 * @version $Id: LineBuilder.java 1171 2013-02-11 21:45:02Z dcollins $
 */
public class LineBuilderNew1 extends AVListImpl
{
    private final WorldWindow wwd;
    private boolean armed = false;
    private ArrayList<Position> positions = new ArrayList<Position>();
    private final RenderableLayer layer;
    private final Polyline line;
    private boolean active = false;

    /**
     * Construct a new line builder using the specified polyline and layer and drawing events from the specified world
     * window. Either or both the polyline and the layer may be null, in which case the necessary object is created.
     *
     * @param wwd       the world window to draw events from.
     * @param lineLayer the layer holding the polyline. May be null, in which case a new layer is created.
     * @param polyline  the polyline object to build. May be null, in which case a new polyline is created.
     */
    public LineBuilderNew1(final WorldWindow wwd, RenderableLayer lineLayer, Polyline polyline)
    {
        this.wwd = wwd;

        if (polyline != null)
        {
            line = polyline;
        }
        else
        {
            this.line = new Polyline();
            this.line.setFollowTerrain(true);
        }
        this.layer = lineLayer != null ? lineLayer : new RenderableLayer();
        this.layer.addRenderable(this.line);
        this.wwd.getModel().getLayers().add(this.layer);

        this.wwd.getInputHandler().addMouseListener(new MouseAdapter()
        {
            public void mousePressed(MouseEvent mouseEvent)
            {
                if (armed && mouseEvent.getButton() == MouseEvent.BUTTON1)
                {
                    if (armed && (mouseEvent.getModifiersEx() & MouseEvent.BUTTON1_DOWN_MASK) != 0)
                    {
                        if (!mouseEvent.isControlDown())
                        {
                            active = true;
                            addPosition();
                        }
                    }
                    mouseEvent.consume();
                }
            }

            public void mouseReleased(MouseEvent mouseEvent)
            {
                if (armed && mouseEvent.getButton() == MouseEvent.BUTTON1)
                {
                    if (positions.size() == 1)
                        removePosition();
                    active = false;
                    mouseEvent.consume();
                }
            }

            public void mouseClicked(MouseEvent mouseEvent)
            {
                if (armed && mouseEvent.getButton() == MouseEvent.BUTTON1)
                {
                    if (mouseEvent.isControlDown())
                        removePosition();
                    mouseEvent.consume();
                }
            }
        });

        this.wwd.getInputHandler().addMouseMotionListener(new MouseMotionAdapter()
        {
            public void mouseDragged(MouseEvent mouseEvent)
            {
                if (armed && (mouseEvent.getModifiersEx() & MouseEvent.BUTTON1_DOWN_MASK) != 0)
                {
                    // Don't update the polyline here because the wwd current cursor position will not
                    // have been updated to reflect the current mouse position. Wait to update in the
                    // position listener, but consume the event so the view doesn't respond to it.
                    if (active)
                        mouseEvent.consume();
                }
            }
        });

        this.wwd.addPositionListener(new PositionListener()
        {
            public void moved(PositionEvent event)
            {
                if (!active)
                    return;

                if (positions.size() == 1)
                    addPosition();
                else
                    replacePosition();
            }
        });
    }

    /**
     * Returns the layer holding the polyline being created.
     *
     * @return the layer containing the polyline.
     */
    public RenderableLayer getLayer()
    {
        return this.layer;
    }

    /**
     * Returns the layer currently used to display the polyline.
     *
     * @return the layer holding the polyline.
     */
    public Polyline getLine()
    {
        return this.line;
    }

    /**
     * Removes all positions from the polyline.
     */
    public void clear()
    {
        while (this.positions.size() > 0)
            this.removePosition();
    }

    /**
     * Identifies whether the line builder is armed.
     *
     * @return true if armed, false if not armed.
     */
    public boolean isArmed()
    {
        return this.armed;
    }

    /**
     * Arms and disarms the line builder. When armed, the line builder monitors user input and builds the polyline in
     * response to the actions mentioned in the overview above. When disarmed, the line builder ignores all user input.
     *
     * @param armed true to arm the line builder, false to disarm it.
     */
    public void setArmed(boolean armed)
    {
        this.armed = armed;
    }

    private void addPosition()
    {
        Position curPos = this.wwd.getCurrentPosition();
        if (curPos == null)
            return;

        this.positions.add(curPos);
        this.line.setPositions(this.positions);
        this.firePropertyChange("LineBuilder.AddPosition", null, curPos);
        this.wwd.redraw();
    }

    private void replacePosition()
    {
        Position curPos = this.wwd.getCurrentPosition();
        if (curPos == null)
            return;

        int index = this.positions.size() - 1;
        if (index < 0)
            index = 0;

        Position currentLastPosition = this.positions.get(index);
        this.positions.set(index, curPos);
        this.line.setPositions(this.positions);
        this.firePropertyChange("LineBuilder.ReplacePosition", currentLastPosition, curPos);
        this.wwd.redraw();
    }

    private void removePosition()
    {
        if (this.positions.size() == 0)
            return;

        Position currentLastPosition = this.positions.get(this.positions.size() - 1);
        this.positions.remove(this.positions.size() - 1);
        this.line.setPositions(this.positions);
        this.firePropertyChange("LineBuilder.RemovePosition", currentLastPosition, null);
        this.wwd.redraw();
    }

    // ===================== Control Panel ======================= //
    // The following code is an example program illustrating LineBuilder usage. It is not required by the
    // LineBuilder class, itself.

    private static class LinePanel extends JPanel
    {
        private final WorldWindow wwd;
        private final LineBuilderNew1 lineBuilder;
        private JButton newButton;
        private JButton pauseButton;
        private JButton endButton;
        private JLabel[] pointLabels;

        public LinePanel(WorldWindow wwd, LineBuilderNew1 lineBuilder)
        {
            super(new BorderLayout());
            this.wwd = wwd;
            this.lineBuilder = lineBuilder;
            this.makePanel(new Dimension(200, 400));
            lineBuilder.addPropertyChangeListener(new PropertyChangeListener()
            {
                public void propertyChange(PropertyChangeEvent propertyChangeEvent)
                {
                    fillPointsPanel();
                }
            });
        }

        private void makePanel(Dimension size)
        {
            JPanel buttonPanel = new JPanel(new GridLayout(1, 2, 5, 5));
            newButton = new JButton("New");
            newButton.addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent actionEvent)
                {
                    lineBuilder.clear();
                    lineBuilder.setArmed(true);
                    pauseButton.setText("Pause");
                    pauseButton.setEnabled(true);
                    endButton.setEnabled(true);
                    newButton.setEnabled(false);
                    ((Component) wwd).setCursor(Cursor.getPredefinedCursor(Cursor.CROSSHAIR_CURSOR));
                }
            });
            buttonPanel.add(newButton);
            newButton.setEnabled(true);

            pauseButton = new JButton("Pause");
            pauseButton.addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent actionEvent)
                {
                    lineBuilder.setArmed(!lineBuilder.isArmed());
                    pauseButton.setText(!lineBuilder.isArmed() ? "Resume" : "Pause");
                    ((Component) wwd).setCursor(Cursor.getDefaultCursor());
                }
            });
            buttonPanel.add(pauseButton);
            pauseButton.setEnabled(false);

            endButton = new JButton("End");
            endButton.addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent actionEvent)
                {
                    lineBuilder.setArmed(false);
                    newButton.setEnabled(true);
                    pauseButton.setEnabled(false);
                    pauseButton.setText("Pause");
                    endButton.setEnabled(false);
                    ((Component) wwd).setCursor(Cursor.getDefaultCursor());
                }
            });
            buttonPanel.add(endButton);
            endButton.setEnabled(false);

            JPanel pointPanel = new JPanel(new GridLayout(0, 1, 0, 10));
            pointPanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

            this.pointLabels = new JLabel[20];
            for (int i = 0; i < this.pointLabels.length; i++)
            {
                this.pointLabels[i] = new JLabel("");
                pointPanel.add(this.pointLabels[i]);
            }

            // Put the point panel in a container to prevent scroll panel from stretching the vertical spacing.
            JPanel dummyPanel = new JPanel(new BorderLayout());
            dummyPanel.add(pointPanel, BorderLayout.NORTH);

            // Put the point panel in a scroll bar.
            JScrollPane scrollPane = new JScrollPane(dummyPanel);
            scrollPane.setBorder(BorderFactory.createEmptyBorder(0, 0, 0, 0));
            if (size != null)
                scrollPane.setPreferredSize(size);

            // Add the buttons, scroll bar and inner panel to a titled panel that will resize with the main window.
            JPanel outerPanel = new JPanel(new BorderLayout());
            outerPanel.setBorder(
                new CompoundBorder(BorderFactory.createEmptyBorder(9, 9, 9, 9), new TitledBorder("Line")));
            outerPanel.setToolTipText("Line control and info");
            outerPanel.add(buttonPanel, BorderLayout.NORTH);
            outerPanel.add(scrollPane, BorderLayout.CENTER);
            this.add(outerPanel, BorderLayout.CENTER);
        }

        private void fillPointsPanel()
        {
            int i = 0;
            Position lastpos = null;
            for (Position pos : lineBuilder.getLine().getPositions())
            {
                if (i == this.pointLabels.length)
                    break;

                ///String las = String.format("Lat %7.4f\u00B0", pos.getLatitude().getDegrees());
                ///String los = String.format("Lon %7.4f\u00B0", pos.getLongitude().getDegrees());
                String las = String.format("%7.4f\u00B0", pos.getLatitude().getDegrees());
                String los = String.format("%7.4f\u00B0", pos.getLongitude().getDegrees());
                
                if ( lastpos == null ) {
                    lastpos = pos;
                }
                double dist = MyWind.computeDistance(lastpos, pos);
                double gain = MyWind.computeElevGain(lastpos, pos);
                double slop = MyWind.computeSlope(lastpos, pos);
                String sls = String.format("%6.3f %5.2f %4.2f", slop,dist,gain);
                lastpos = pos;
                
                pointLabels[i++].setText(sls + " " + las + " " + los);
            }
            for (; i < this.pointLabels.length; i++)
                pointLabels[i++].setText("");
        }
    }

    /**
     * Marked as deprecated to keep it out of the javadoc.
     *
     * @deprecated
     */
    public static class AppFrame extends ApplicationTemplate.AppFrame
    {
        private JButton selLayerButton;
        private JButton selLinesButton;
        private JButton selPlacesButton;
        
        private WorldWindow thisWwd=null;
        private LayerPanel panelLayer=null;
        private LinePanel  panelLine=null;
        
        private JPanel     panelLeft=null;
        private JPanel     panelLeftTop=null;
        private JPanel     panelLeftMid=null;
        
        public AppFrame()
        {
            super(true, true, false);
            
            thisWwd = this.getWwd();

            LineBuilderNew1 lineBuilder = new LineBuilderNew1(thisWwd,null,null);
            panelLine = new LinePanel(thisWwd, lineBuilder);
            
            panelLayer = this.getLayerPanel();
            panelLeft = new JPanel(new BorderLayout());
            panelLeftTop = new JPanel();
            panelLeftMid = new JPanel(new BorderLayout());
            
            this.getContentPane().remove(panelLayer);
            this.getContentPane().add(panelLeft, BorderLayout.WEST);
            
            panelLeft.add(panelLeftTop, BorderLayout.NORTH);
            panelLeft.add(panelLeftMid, BorderLayout.CENTER);
            
            selLayerButton = new JButton("Layers");
            selLinesButton = new JButton("Lines");
            selPlacesButton = new JButton("Places");
            
            selLayerButton.addActionListener(new ActionListener()
                {
                    public void actionPerformed(ActionEvent actionEvent)
                    {
                        selLayerButton.setText("done");
                        selLayerButton.setEnabled(false);
                        selLinesButton.setText("Lines");
                        selLinesButton.setEnabled(true);
                        panelLeftMid.removeAll();
                        panelLeftMid.add(panelLayer, BorderLayout.CENTER);
                    }
                });
            panelLeftTop.add(selLayerButton);
            
            selLinesButton.addActionListener(new ActionListener()
                {
                    public void actionPerformed(ActionEvent actionEvent)
                    {
                        selLinesButton.setText("done");
                        selLinesButton.setEnabled(false);
                        selLayerButton.setText("Layers");
                        selLayerButton.setEnabled(true);
                        panelLeftMid.removeAll();
                        panelLeftMid.add(panelLine, BorderLayout.CENTER);
                    }
                });
            panelLeftTop.add(selLinesButton);
            
            selPlacesButton.addActionListener(new ActionListener()
                {
                    public void actionPerformed(ActionEvent actionEvent)
                    {
                        selPlacesButton.setText("done");
                        BasicOrbitView view = (BasicOrbitView) thisWwd.getView();
                        view.stopAnimations();
                        
                        final Position pos = view.getEyePosition();
                        view.setHeading(Angle.fromDegrees(90));
                        view.setPitch(Angle.fromDegrees(45));
                        view.setFieldOfView(Angle.fromDegrees(45));
                        view.setRoll(Angle.fromDegrees(0));
                        view.setEyePosition(pos);
                        
                        view.addEyePositionAnimator(4000, view.getEyePosition(), 
                                Position.fromDegrees(38.0080, -120.0082, 3000));
                    }
                });
            panelLeftTop.add(selPlacesButton);
        }
    }

    /**
     * Marked as deprecated to keep it out of the javadoc.
     *
     * @param args the arguments passed to the program.
     * @deprecated
     */
    public static void main(String[] args)
    {
        //noinspection deprecation
        ApplicationTemplate.start("World Wind Line Builder New1", LineBuilderNew1.AppFrame.class);
    }
}
