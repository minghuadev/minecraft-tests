<?php
    // http://www.w3schools.com/php/php_file_upload.asp

    session_name("upload"); session_start();

    $errcnt = 0;
    $debug = 0;

    //$allowedExts = array("gif", "jpeg", "jpg", "png", "<none>");
    $allowedExts = array("txt", "tgz", "<none>");

do {
    $varptype = gettype($_POST);
    if ( $varptype != "array" ) {
        echo "Error: _POST not an array";  echo "<br />";  $errcnt = 1;  break;
    }

    // text field value check
    if ( ! in_array("text", array_keys($_POST) ) ) {
        echo "Error: _POST does not have a text key";  echo "<br />";  $errcnt = 1;  break;
    }
    {
        // string crypt ( string $str, string $salt )
        //      sha256 salt: $5$ + 16 character 
        // int    strcmp ( string $str, string $str ) : return 0 if equal
        $rxtxt = $_POST['text'];
        $basesalt = '$5$DTEXdghLhZCea2wV';
        $basehash = '$5$DTEXdghLhZCea2wV$.NvcxTlULnTBjZLylFJi94rM9JQtCNGJHp..JLknbm.';
                   //123456789 123456789 223456789 323456789 423456789 523456789 623
        $basehashlen = 63;

        if ( substr( $rxtxt, 0, 3) != '$5$' ) {
            if (strlen($rxtxt) > 16 ) {
                echo "Error: _POST text failed raw length limit of 16 <br />";  $errcnt = 1;  break;
            }
            $rxhash = crypt( $rxtxt, $basesalt );
            $rxlen  = strlen($rxhash);
            if ( strcmp($basehash, $rxhash) != 0 ) {
                echo "Hash len: " . $rxlen . "<br />\n";
                echo "Hash between &lt;colon&gt;&lt;space&gt; and &lt;space&gt;&lt;colon&gt;<br />\n";
                echo "Hash: " . $rxhash . " :<br />\n";
                //echo "Base hash: " . $basehash . "<br />\n";
                //echo "Rcvd hash: " . $rxhash . "<br />\n";
                //echo "Rcvd text: " . $rxtxt . "<br />\n";
                $rl = strlen($rxtxt);
                echo "Rcv len:  " . $rl . "<br />\n";
                echo "Rcv tail: " . substr( $rxtxt, $rl-3, 3) . "<br />\n";
                echo "Error: variable _POST failed raw value check <br />";  $errcnt = 1;  break;
                break;
            }
        } else {
          // validate
          if ($basehashlen != strlen($rxtxt) ) {
            echo "Error: variable _POST failed hashed length check <br />";  $errcnt = 1;  break;
          }
          if ( strcmp($basehash, $rxtxt) != 0 ) {
            //echo "Base hash: " . $basehash . "<br />\n";
            //echo "Rcvd hash: " . $rxtxt . "<br />\n";
            echo "Error: variable _POST failed hashed value check <br />";  $errcnt = 1;  break;
          }
        }
    }

    $varftype = gettype($_FILES);
    if ( $varftype != "array" ) {
        echo "Error: variable _FILES not an array";  echo "<br />";  $errcnt = 1;  break;
    }

    $temp = explode(".", $_FILES["file"]["name"]);
    $extension = end($temp);
    if ( count($temp) < 2 ) {
        $extension = "<none>";
    }

    if ( $debug ) {
        foreach($_FILES as $x=>$x_value) {
            echo "Key=" . $x . ", Value=" . $x_value;
            echo "<br />";
            foreach($x_value as $y=>$y_value) {
                echo "Key=" . $x . ", Key=" . $y . ", Value=" . $y_value;
                echo "<br />";
            }
            echo "<br />";
        }
        var_dump($_FILES);
        echo "<br />";
        echo "_FILES array size " . count($_FILES);
        echo "<br />";
        var_dump($_POST);
        echo "<br />";
        echo "_POST array size " . count($_POST);
        echo "<br />";
    }


    if ( !( ( ($_FILES["file"]["type"] == "image/gif")
           || ($_FILES["file"]["type"] == "application/octet-stream")
           || ($_FILES["file"]["type"] == "application/x-compressed-tar")
           || ($_FILES["file"]["type"] == "text/plain")
           || ($_FILES["file"]["type"] == "image/jpeg")
           || ($_FILES["file"]["type"] == "image/jpg")
           || ($_FILES["file"]["type"] == "image/pjpeg")
           || ($_FILES["file"]["type"] == "image/x-png")
           || ($_FILES["file"]["type"] == "image/png")   )
         && ($_FILES["file"]["size"] < 20000000)
         && in_array($extension, $allowedExts) ) ) 
    {
        echo "Error: Invalid file. type: " . ($_FILES["file"]["type"]) . "<br />";
        echo "Error: Invalid file. ext:  " . ($extension) . "<br />";
        echo "Error: Invalid file. size: " . ($_FILES["file"]["size"]) . "<br />";
        $errcnt = 1;
        break;
    }
    if ($_FILES["file"]["error"] > 0) {
        echo "Error: Return Code: " . $_FILES["file"]["error"] . "<br />";
        $errcnt = 1;
        break;
    }

            echo "Upload:    " . $_FILES["file"]["name"] . "<br />\n";
            echo "Type:      " . $_FILES["file"]["type"] . "<br />\n";
            echo "Size:      " . ($_FILES["file"]["size"] / 1024) . " kB<br />\n";
            //echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />\n";

            $upldir  = "/uploaddata";
            $uplpath = $_SERVER['DOCUMENT_ROOT'].$upldir;
            $ultpath = $_SERVER['DOCUMENT_ROOT']."/uploadlist";
            $cntpath = $_SERVER['DOCUMENT_ROOT']."/uploadlist/upload_file_cnt.txt";
            $lstpath = $_SERVER['DOCUMENT_ROOT']."/uploadlist/upload_file_list.txt";
        
            // check /uploadlist/
            if ( ! file_exists($ultpath) ) {
                echo "Create directory: " . "/uploadlist" . "<br />\n";
                mkdir($ultpath);
            }
            if ( ! is_dir($ultpath) ) {
                echo "Error: File already exists: " . "/uploadlist" . "<br />";
                $errcnt = 1;
                break;
            }

            // check /uploaddata/
            if ( ! file_exists($uplpath) ) {
                echo "Create directory: " . $upldir . "<br />\n";
                mkdir($uplpath);
            }
            //if ( file_type($uplpath) != "dir" ) {  // file_type crashes?
            if ( ! is_dir($uplpath) ) {
                echo "Error: File already exists: " . $upldir . "<br />";
                $errcnt = 1;
                break;
            }
            echo "Directory ok: " . $upldir . "<br />\n";

            // file count starting from "001"
            $filecnt = "001";
            if ( file_exists($cntpath) ) {
                $filecnt = file_get_contents($cntpath);
                $filecnt = sprintf("%03u", $filecnt + 1);
            }
            file_put_contents($cntpath, $filecnt);

            $foname = $_FILES["file"]["name"];
            echo "Original file: " . $foname . "<br />\n";
            $fnname = $_FILES["file"]["name"] . "-" . $filecnt;
            echo "To save file: " . $fnname . "<br />\n";
            $fnpath = $uplpath . "/" . $fnname;
        
            if ( file_exists( $fnpath ) ) {
                echo "Error: File already exists: " . $fnname . "<br />";
                $errcnt = 1;
                break;
            }
            if ( $errcnt != 0 ) {
                echo "Ignored file: " . $foname . "<br />";
                break;
            }

            move_uploaded_file($_FILES["file"]["tmp_name"], $fnpath );
            //echo "Stored in: " . $fnpath . "<br />";
            echo "Stored in: " . $fnname . "<br />\n";
        
            // date format:  D 3letter Mon thr Sun, Y 4digit eg 1918 or 2012, 
            //               m 01 thr 12, d 01 thr 31, H 00 thr 23, i 00 thr 59
            $datestr = date('D-Y-md-Hi'); //len: 3-4-4-4 , total 18.

            $filelist = "";
            if ( file_exists($lstpath) ) {
                $filelist = file_get_contents($lstpath);
            }
            $filelist = $filelist . $fnname . " " . $datestr . "\n";
            file_put_contents($lstpath, $filelist);

} while(0);

?>

