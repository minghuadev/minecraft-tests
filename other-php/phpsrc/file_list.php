<?php
    session_name("upload"); session_start();

    $errcnt = 0;
    $debug = 0;

do {
    $rawlistfile = $_SERVER['DOCUMENT_ROOT'] . '/uploadlist/upload_file_list.txt';
    if ( ! file_exists($rawlistfile) ) {
        echo "Error: File list does not exist: " . '/upload_file_list.txt' . "<br />\n"; $errcnt = 1; break;
    }

    $filecontent = file_get_contents($rawlistfile);

    $in_temp = explode("\n", $filecontent);
    
    //var_dump($in_temp);
    echo "Size in_temp: " . count($in_temp) . '<br />' . "\n";
    $templen = count($in_temp);
    if ( $templen < 1 ) {
        echo "No file<br />\n";
    }

    $prefixpath = $_SERVER['DOCUMENT_ROOT'] . '/uploaddata';
    for ( $i = 0; $i < $templen; $i ++ ) {
        $a = $in_temp[$i];
        $b = explode(" ", $a);
        $n = $a;
        $m = "<no_date>";
        if ( count($b) == 2 ) {
            $n = $b[0];
            $m = $b[1];
        }
        if ( strlen($n) < 6 ) {
            echo "Skip line " . $i . "<br />\n"; continue;
        }
        $fpth = $prefixpath . "/" . $n;
        if ( file_exists($fpth) ) {
            $x = substr($n, 0, strlen($n)-4);
            echo '<p> File: <a href="/phpsrc/file_download.php?file=' . $n . '">' . $x . "</a>";
            echo " (" . $n . " " . $m . ")</p>\n";
        } else {
            echo '<p> File: ' . $n . " " . $m . "</a></p>\n";
        }
    }

} while(0);

?>

