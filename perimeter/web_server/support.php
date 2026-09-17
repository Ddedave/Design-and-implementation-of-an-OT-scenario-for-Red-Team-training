<?php
$uploads = __DIR__ . '/uploads';
if (!is_dir($uploads)) { @mkdir($uploads, 0777, true); }

$name  = $_POST['name']  ?? '';
$email = $_POST['email'] ?? '';
$phone = $_POST['phone'] ?? '';
$desc  = $_POST['desc']  ?? '';

$saved = null;
if (!empty($_FILES['file']['name'])) {
  $dest = $uploads . '/' . basename($_FILES['file']['name']);
  if (@move_uploaded_file($_FILES['file']['tmp_name'], $dest)) {
    @chmod($dest, 0777);
    $saved = 'uploads/' . basename($_FILES['file']['name']);
  }
}
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Ticket submitted</title>
  <style>
    body{margin:0;background:#0b0f14;color:#e6eef6;font:16px/1.6 system-ui,Segoe UI,Roboto}
    .wrap{max-width:780px;margin:60px auto;padding:0 20px}
    .card{background:#111823;border:1px solid #1e2a38;border-radius:14px;padding:20px}
    a{color:#6bd1ff;text-decoration:none}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h2>Ticket received ✅</h2>
      <p><strong>Name:</strong> <?=htmlspecialchars($name)?></p>
      <p><strong>Email:</strong> <?=htmlspecialchars($email)?></p>
      <p><strong>Phone:</strong> <?=htmlspecialchars($phone)?></p>
      <p><strong>Description:</strong><br><?=nl2br(htmlspecialchars($desc))?></p>
      <?php if ($saved): ?>
        <p><strong>Uploaded file:</strong> <a href="<?=htmlspecialchars($saved)?>" target="_blank"><?=htmlspecialchars($saved)?></a></p>
      <?php else: ?>
        <p><em>No file attached.</em></p>
      <?php endif; ?>
      <p><a href="index.html">Back to portal</a></p>
    </div>
  </div>
</body>
</html>
