<?php

	// Password protection

	/*
	if (empty($_POST['password']) || $_POST['password'] !== 'password') {
		header($_SERVER['SERVER_PROTOCOL'] . ' 401 Unauthorized', true, 401);
		exit;
	}
	*/

	// Instance

	$instance = $_POST['instance'] ?? '';

		if (!empty($instance))
			$instance .= '/';

	// Log start/close

	if (!empty($_POST['log_start_close'])) {

		$savePath = 'log/' . $instance;

		if (!is_dir($savePath))
			mkdir($savePath, 0777, true);

		$savePath .= 'log.txt';

		$f = fopen($savePath, 'a');
			fwrite($f, $_POST['log_start_close']);
			fclose($f);

		exit;
	}

	// Screenshot

	if (!isset($_FILES['screenshot']) || $_FILES['screenshot']['error'] !== UPLOAD_ERR_OK) {
		header($_SERVER['SERVER_PROTOCOL'] . ' 400 Bad Request', true, 400);
		exit;
	}

	$savePath = 'log/' . $instance . 'screenshots/' . date('Y/m/d');

	if (!is_dir($savePath))
		mkdir($savePath, 0777, true);

	$savePath .= '/' . $_FILES['screenshot']['name'];

	move_uploaded_file($_FILES['screenshot']['tmp_name'], $savePath);
