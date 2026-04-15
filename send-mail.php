<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Mailgun Configuration
$MAILGUN_API_KEY = getenv('MAILGUN_API_KEY') ?: 'YOUR_MAILGUN_API_KEY';
$MAILGUN_DOMAIN = 'berkleysecurity.com';
$RECIPIENT_EMAIL = 'staff@berkleysecurity.com';

// Get form data
$name = trim($_POST['name'] ?? '');
$email = trim($_POST['email'] ?? '');
$phone = trim($_POST['phone'] ?? '');
$serviceArea = trim($_POST['service_area'] ?? '');
$serviceType = trim($_POST['service_type'] ?? '');
$propertyType = trim($_POST['property_type'] ?? '');
$message = trim($_POST['message'] ?? '');

// Honeypot spam check
$honeypot = trim($_POST['website'] ?? '');
if (!empty($honeypot)) {
    // Bot detected - silently succeed to not alert the bot
    echo json_encode(['success' => true]);
    exit;
}

// Server-side validation
if (empty($name) || empty($email) || empty($phone) || empty($serviceArea) || empty($serviceType) || empty($propertyType)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'All required fields must be filled out.']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid email address.']);
    exit;
}

// Format service labels
$serviceAreaLabels = [
    'clinton' => 'Clinton, MS',
    'natchez' => 'Natchez, MS',
    'jackson' => 'Jackson, MS',
    'byram' => 'Byram, MS',
    'madison' => 'Madison, MS',
    'canton' => 'Canton, MS',
    'ridgeland' => 'Ridgeland, MS',
    'flowood' => 'Flowood, MS',
    'richland' => 'Richland, MS',
    'brandon' => 'Brandon, MS',
    'hattiesburg' => 'Hattiesburg, MS',
    'vidalia' => 'Vidalia, LA',
    'rayville' => 'Rayville, LA',
    'brookhaven' => 'Brookhaven, MS',
    'mccomb' => 'McComb, MS',
    'other' => 'Other'
];

$serviceTypeLabels = [
    'security-alarm' => 'Security Alarm',
    'video-surveillance' => 'Video Surveillance',
    'fire-system' => 'Fire System',
    'medical-alert' => 'Medical Alert',
    'home-automation' => 'Home Automation',
    'home-theater' => 'Home Theater',
    'other' => 'Other'
];

$areaLabel = $serviceAreaLabels[$serviceArea] ?? ucfirst($serviceArea);
$typeLabel = $serviceTypeLabels[$serviceType] ?? ucfirst($serviceType);
$propertyLabel = ucfirst($propertyType);

// Build email HTML
$timestamp = date('F j, Y \a\t g:i A T');
$htmlBody = "
<div style='font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;'>
    <div style='background-color: #1a2744; padding: 24px; text-align: center;'>
        <h1 style='color: #ffffff; margin: 0; font-size: 22px;'>New Consultation Request</h1>
        <p style='color: #9ca3af; margin: 8px 0 0; font-size: 14px;'>Submitted on {$timestamp}</p>
    </div>
    <div style='padding: 24px; background-color: #f8fafc; border: 1px solid #e2e8f0;'>
        <table style='width: 100%; border-collapse: collapse;'>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #1a2744; width: 140px;'>Name</td>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; color: #374151;'>" . htmlspecialchars($name) . "</td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #1a2744;'>Email</td>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0;'><a href='mailto:" . htmlspecialchars($email) . "' style='color: #3182ce;'>" . htmlspecialchars($email) . "</a></td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #1a2744;'>Phone</td>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0;'><a href='tel:" . htmlspecialchars($phone) . "' style='color: #3182ce;'>" . htmlspecialchars($phone) . "</a></td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #1a2744;'>Service Area</td>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; color: #374151;'>" . htmlspecialchars($areaLabel) . "</td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #1a2744;'>Service Type</td>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; color: #374151;'>" . htmlspecialchars($typeLabel) . "</td>
            </tr>
            <tr>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #1a2744;'>Property Type</td>
                <td style='padding: 12px; border-bottom: 1px solid #e2e8f0; color: #374151;'>" . htmlspecialchars($propertyLabel) . "</td>
            </tr>
            <tr>
                <td style='padding: 12px; font-weight: bold; color: #1a2744; vertical-align: top;'>Message</td>
                <td style='padding: 12px; color: #374151;'>" . nl2br(htmlspecialchars($message ?: 'No message provided.')) . "</td>
            </tr>
        </table>
    </div>
    <div style='padding: 16px; background-color: #1a2744; text-align: center;'>
        <p style='color: #9ca3af; margin: 0; font-size: 12px;'>This is an automated message from berkleysecurity.com</p>
    </div>
</div>";

$textBody = "NEW CONSULTATION REQUEST\n"
    . "========================\n\n"
    . "Name: {$name}\n"
    . "Email: {$email}\n"
    . "Phone: {$phone}\n"
    . "Service Area: {$areaLabel}\n"
    . "Service Type: {$typeLabel}\n"
    . "Property Type: {$propertyLabel}\n"
    . "Message: " . ($message ?: 'No message provided.') . "\n\n"
    . "Submitted: {$timestamp}\n";

// Send via Mailgun API
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://api.mailgun.net/v3/{$MAILGUN_DOMAIN}/messages");
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
curl_setopt($ch, CURLOPT_USERPWD, "api:{$MAILGUN_API_KEY}");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, [
    'from' => "Berkley Security Website <noreply@{$MAILGUN_DOMAIN}>",
    'to' => $RECIPIENT_EMAIL,
    'h:Reply-To' => $email,
    'subject' => "New Consultation Request from {$name} - {$typeLabel}",
    'text' => $textBody,
    'html' => $htmlBody
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($httpCode === 200) {
    echo json_encode(['success' => true, 'message' => 'Your request has been sent successfully.']);
} else {
    error_log("Mailgun API Error: HTTP {$httpCode} - {$response} - cURL Error: {$curlError}");
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Unable to send your message. Please call us at 1-800-778-3173.']);
}
?>
