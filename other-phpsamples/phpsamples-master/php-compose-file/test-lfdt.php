<?php 

    $op = $_GET['op'];
    $oc = $_GET['oc'];

    //date_default_timezone_set('EST');
    $dt = time() - 3600 * 3;
    $dtstr = date('D M d H:i:s', $dt);

    $fp = fopen('lidn.txt', 'a');
    if ( $op == 'lf' ) {
        fwrite($fp, "\n");
    } else if ( $op == 'dt' ) {
        fwrite($fp, ' ');
        echo $dtstr;
        fwrite($fp, $dtstr);
        fwrite($fp, ' ');
    } else {
        fwrite($fp, ' ');
        fwrite($fp, $oc);
        fwrite($fp, ' ');
    }
    fclose($fp);

?>

