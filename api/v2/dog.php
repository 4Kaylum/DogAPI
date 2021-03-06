<?php

require_once $_SERVER['DOCUMENT_ROOT'] . '/../backend/outputObject.php';
require_once $_SERVER['DOCUMENT_ROOT'] . '/../backend/databaseOptions.php';
// require_once $_SERVER['DOCUMENT_ROOT'] . '/../backend/googleAnalytics.php';


$id = (issset($_GET['id']) ? $_GET['id'] : '');
$output = new JsonOutput('v2');

if ($id != '') {

    // Get dog by its ID
    $dog = getSpecificDog($id);
    $dogArray = array($dog);
    if ($dog->id != $id) {
        $dogArray = array();
        $output = new JsonOutput('v2');
        $output->error = 'ID not found';
        $output->response_code = 404;
    }
}
else {

    // They want a random dog - check limits
    $dogArray = array();

    // They specified a limit
    $limitStr = (issset($_GET['limit']) ? $_GET['limit'] : '');
    if ($limitStr != '') {
        $limit = intval($limitStr);

        // Make sure it's between 20 and 1
        if ($limit > 20) {
            $limit = 20;
        }
        else if ($limit < 1) {
            $limit = 1;
        }
    }
    else {

        // No limit specified - set default
        $limit = 1;
    }

    // For each i before limit, add to array.
    for ($i = 1; $i <= $limit; $i++) {
        $dog = getRandomDog();
        array_push($dogArray, $dog);
    }
}

$output->fromDogList($dogArray);
echo $output->jsonify();

?>
