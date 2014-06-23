<?php

    $errcnt = 0;
    $debug = 0;

do {
    $varptype = gettype($_GET);
    if ( $varptype != "array" ) {
        echo "Error: variable _GET not an array";  echo "<br />\n";  $errcnt = 1;  break;
    }

    if ( $debug ) {
        foreach($_GET as $x=>$x_value) {
            echo "Key=" . $x . ", Value=" . $x_value;
            echo "<br />";
            foreach($x_value as $y=>$y_value) {
                echo "Key=" . $x . ", Key=" . $y . ", Value=" . $y_value;
                echo "<br />\n";
            }
            echo "<br />\n";
        }
        var_dump($_GET);
        echo "<br />";
        echo "_GET array size " . count($_GET);
        echo "<br />\n";
    }

    // value check
    if ( ! in_array("file", array_keys($_GET) ) ) {
        echo "Error: variable _GET does not have a file key";  echo "<br />\n";  $errcnt = 1;  break;
    }
    $file = $_GET['file'];

    $upldir  = "/uploaddata";
    $uplpath = $_SERVER['DOCUMENT_ROOT'].$upldir;

    if ( ! file_exists($uplpath) ) {
        echo "No directory: " . $upldir . "<br />\n"; $errcnt = 1; break;
    }
    if ( ! is_dir($uplpath) ) {
        echo "Error: File exists: " . $upldir . "<br />\n"; $errcnt = 1; break;
    }
    if ( $debug ) {
        echo "Directory ok: " . $upldir . "<br />\n";
    }

    $filepath = $uplpath . "/" . $file;
    if ( ! file_exists($filepath) ) {
        echo "Error: File not exists: " . $file . "<br />\n"; $errcnt = 1; break;
    }

    $filecontent = file_get_contents($filepath);

    $m = $file;
    if ( strlen($file) >= 6 ) {
            $m = substr($file, 0, strlen($file)-4);
    }

    $mtype = 'application/octet-stream';
    if ( strlen($m) > 4 && substr($m, strlen($m)-4) == '.txt' ) {
        $mtype = 'text/plain';
    }
    if ( ! $debug ) {
        header('Content-disposition: attachment; filename=' . $m);
        header('Content-type: ' . $mtype);
        header('Content-Length: ' . strlen($filecontent));
        header("Pragma: no-cache");
        header("Expires: 0");
        echo $filecontent;
    } else {
        echo '<p>Content-disposition: attachment; filename=' . $m . '</p>' . "\n";
        echo '<p>Content-type: ' . $mtype . '</p>' . "\n";
        echo '<p>Content-Length: ' . strlen($filecontent) . '</p>' . "\n";
        echo '<p>Pragma: no-cache</p>' . "\n";
        echo '<p>Expires: 0</p>' . "\n";
        echo '<p> ... </p>' . "\n";
    }

} while(0);

?>

