<?php

// Password protection.

// if (empty($_POST["password"]) || $_POST["password"] !== "password") {
//     header($_SERVER["SERVER_PROTOCOL"] . " 401 Unauthorized", true, 401);
//     exit();
// }

// Instance.

$instance = $_POST["instance"] ?? "";
if (!empty($instance)) {
    $instance .= "/";
}

// Log start/close.

if (!empty($_POST["log_start_close"])) {
    $save_path = "log/" . $instance;

    if (!is_dir($save_path)) {
        mkdir($save_path, 0777, true);
    }

    $f = fopen($save_path . "log.txt", "a");
    fwrite($f, $_POST["log_start_close"]);
    fclose($f);

    exit();
}

// Save screenshot.

if (
    !isset($_FILES["screenshot"]) ||
    $_FILES["screenshot"]["error"] !== UPLOAD_ERR_OK
) {
    header($_SERVER["SERVER_PROTOCOL"] . " 400 Bad Request", true, 400);
    exit();
}

$save_path = "log/" . $instance . date("Y-m/d");

if (!is_dir($save_path)) {
    mkdir($save_path, 0777, true);
}

$save_path .= "/" . $_FILES["screenshot"]["name"];

move_uploaded_file($_FILES["screenshot"]["tmp_name"], $save_path);
