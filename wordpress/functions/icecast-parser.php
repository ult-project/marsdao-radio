<?php
  // set the error handler to catch issues
  set_error_handler(function ($level, $message, $file = '', $line = 0) {
    throw new ErrorException($message, 0, $level, $file, $line);
  });

  function getMp3StreamTitle($streamingUrl, $interval, $offset = 0, $headers = true) {
    $required = 'StreamTitle=';
    $user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36';
    $options = [
      'http' => [
        'method' => 'GET',
        'header' => 'Icy-MetaData: 1',
        'user_agent' => $user_agent
      ]
    ];
    if (($headers = get_headers($streamingUrl)))
      foreach ($headers as $h)
        if (strpos(strtolower($h), 'icy-metaint') !== false && ($interval = explode(':', $h)[1]))
          break;
        $context = stream_context_create($options);
        if ($stream = fopen($streamingUrl, 'r', false, $context)) {
          while($buffer = stream_get_contents($stream, $interval, $offset)) {
            if (strpos($buffer, $required) !== false) {
              fclose($stream);
            $title = explode($required, $buffer)[1];
            return substr($title, 1, strpos($title, ';') - 2);
            }
            $offset += $interval;
          }
        }
  }

  // if the request successfully completed
  try {
    print(getMp3StreamTitle('https://onair.example.com/live', 443)); // replace with your Icecast2 stream URL
  }

  // if the request returns an error
  catch (Throwable $e) {
    echo '<span style="color:#ff7831;">radio stream unavailable</span>';
  }
?>
