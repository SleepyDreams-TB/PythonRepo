<?php
// Configuration
$organisationId = "15974";
$organisationSalt = "PKnO1sf8zAbDeSqcwa-QRH"; // Keep this secret
$timestamp = time();

// Generate Auth Token
$combined = $organisationSalt . '_' . $organisationId . '_' . $timestamp;
$authToken = hash("sha256", $combined);

// Request data
$postData = [
  'amount' => 1,
  'merchant_reference' => 'Test',
  'payment_type' => 'eft'
];

// Initialize cURL
$ch = curl_init('https://services.callpay.com/api/v2/payment-key');
curl_setopt_array($ch, [
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_POST => true,
  CURLOPT_POSTFIELDS => http_build_query($postData),
  CURLOPT_HTTPHEADER => [
    "Auth-Token: $authToken",
    "Org-Id: $organisationId",
    "Timestamp: $timestamp",
    "Content-Type: application/x-www-form-urlencoded"
  ],
  CURLOPT_SSL_VERIFYPEER => false,  // Disable SSL certificate verification
  CURLOPT_SSL_VERIFYHOST => false   // Disable host verification
]);

// Execute request and handle response
try {
  $response = curl_exec($ch);

  if (curl_errno($ch)) {
    throw new Exception("cURL Error: " . curl_error($ch));
  }

  $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
  curl_close($ch);

  if ($httpCode !== 200) {
    throw new Exception("Callpay API returned HTTP $httpCode: $response");
  }

  $json = json_decode($response, true);
  if (json_last_error() !== JSON_ERROR_NONE) {
    throw new Exception("Failed to parse JSON: " . json_last_error_msg());
  }

  // Successfully received payment key
  $paymentUrl = $json['url'];
  echo "Redirect user to: $paymentUrl\n";
} catch (Exception $e) {
  error_log($e->getMessage());
  echo "Something went wrong. Please try again later.";
}
