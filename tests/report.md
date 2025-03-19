| commit_hash | author | date | severity | cve_details | owasp_category | filename | diff_preview |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 101597a89519343e1681b9c31a077a367a128921 | g0tmi1k | 2015-09-11 13:36:18+01:00 | Critical | No CVE found | Unknown Category | main.css | @@ -8,7 +8,7 @@ body{
 }
 
 body.home{
-	background: #e7e7e7;	
+	background: #e7e7e7;
 }
 
 d |
| 101597a89519343e1681b9c31a077a367a128921 | g0tmi1k | 2015-09-11 13:36:18+01:00 | Critical | No CVE found | Unknown Category | dvwaPage.inc.php | @@ -261,7 +261,7 @@ function dvwaHtmlEcho( $pPage ) {
 
 		}
 
-		$menuHtml .= "<ul>{$menuBlockHt |
| 4073d00ebc265450e40edfd4160e9c97d1d1cec8 | g0tmi1k | 2015-09-12 19:50:30+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -12,16 +12,11 @@ if(isset($_GET[ 'Submit' ])) {
 		$result = mysql_query( $getid ); // Removed 'o |
| 4073d00ebc265450e40edfd4160e9c97d1d1cec8 | g0tmi1k | 2015-09-12 19:50:30+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -9,16 +9,11 @@ if(isset($_GET[ 'Submit' ])) {
 	$result = mysql_query( $getid ); // Removed 'or d |
| 4073d00ebc265450e40edfd4160e9c97d1d1cec8 | g0tmi1k | 2015-09-12 19:50:30+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -10,16 +10,11 @@ if(isset($_GET[ 'Submit' ])) {
 	$result = mysql_query( $getid ); // Removed 'or |
| 56864d300be750e24a4b3e5d536b0a1561adae9a | g0tmi1k | 2015-09-12 20:13:39+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -16,6 +16,7 @@ if(isset($_GET[ 'Submit' ])) {
 			$html .= '<pre>User ID exists in the database.< |
| 56864d300be750e24a4b3e5d536b0a1561adae9a | g0tmi1k | 2015-09-12 20:13:39+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -13,6 +13,7 @@ if(isset($_GET[ 'Submit' ])) {
 		$html .= '<pre>User ID exists in the database.</ |
| 56864d300be750e24a4b3e5d536b0a1561adae9a | g0tmi1k | 2015-09-12 20:13:39+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -14,6 +14,7 @@ if(isset($_GET[ 'Submit' ])) {
 		$html .= '<pre>User ID exists in the database.</ |
| 76851d7935bdfd3ae5d02d6bb345349c2a14b07d | g0tmi1k | 2015-09-14 16:28:28+01:00 | Critical | No CVE found | A03:2021 - Injection | dvwaPage.inc.php | @@ -440,6 +440,7 @@ function dvwaDatabaseConnect() {
 	global $_DVWA;
 	global $DBMS;
 	global $DB |
| 76851d7935bdfd3ae5d02d6bb345349c2a14b07d | g0tmi1k | 2015-09-14 16:28:28+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -3,24 +3,16 @@
 if(isset($_GET[ 'Submit' ])) {
 	// Retrieve data
 	$id = $_GET[ 'id' ];
-	$id |
| 76851d7935bdfd3ae5d02d6bb345349c2a14b07d | g0tmi1k | 2015-09-14 16:28:28+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -3,15 +3,10 @@
 if(isset($_GET[ 'Submit' ])) {
 	// Retrieve data
 	$id = $_GET[ 'id' ];
-	$id |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,7 +1,6 @@
 <?php
 
 if( isset( $_GET[ 'Login' ] ) ) {
-
 	$user = $_GET[ 'username' ];
  |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Change' ])) {
+if( isset( $_GET[ 'Change' ] ) ) {
 	/ |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,7 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Change' ])) {
-
+if( isset( $_GET[ 'Change' ] ) ) {
 |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | medium.php | @@ -1,7 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Change' ])) {
-
+if( isset( $_GET[ 'Change' ] ) ) {
 |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,7 +1,6 @@
 <?php
 
 if( isset( $_POST[ 'submit' ] ) ) {
-
 	$target = $_REQUEST[ 'ip' ];
 |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | medium.php | @@ -1,7 +1,6 @@
 <?php
 
 if( isset( $_POST[ 'submit' ] ) ) {
-
 	$target = $_REQUEST[ 'ip' ];
 |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Submit' ])) {
+if( isset( $_GET[ 'Submit' ] ) ) {
 	/ |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Submit' ])) {
+if( isset($_GET[ 'Submit' ] ) ) {
 	// |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | medium.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Submit' ])) {
+if( isset( $_GET[ 'Submit' ] ) ) {
 	/ |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Submit' ])) {
+if( isset( $_GET[ 'Submit' ] ) ) {
 	/ |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Submit' ])) {
+if( isset($_GET[ 'Submit' ] ) ) {
 	// |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | medium.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset($_GET[ 'Submit' ])) {
+if( isset( $_GET[ 'Submit' ] ) ) {
 	/ |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -1,9 +1,9 @@
 <?php
 
-if(!array_key_exists ("name", $_GET) || $_GET[ 'name' ] == NULL || $_GET |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,9 +1,6 @@
 <?php
 
-if(!array_key_exists ("name", $_GET) || $_GET[ 'name' ] == NULL || $_GET |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | medium.php | @@ -1,12 +1,6 @@
 <?php
 
-if(!array_key_exists ("name", $_GET) || $_GET[ 'name' ] == NULL || $_GE |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -1,24 +1,24 @@
 <?php
 
-if(isset( $_POST[ 'btnSign' ] )) {
+if( isset( $_POST[ 'btnSign' ] )  |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset( $_POST[ 'btnSign' ] )) {
+if( isset( $_POST[ 'btnSign' ] ) )  |
| 7ae63158824d784730f0fcda8c3ec4be54e70f46 | g0tmi1k | 2015-09-16 13:25:23+01:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | medium.php | @@ -1,6 +1,6 @@
 <?php
 
-if(isset( $_POST[ 'btnSign' ] )) {
+if( isset( $_POST[ 'btnSign' ] ) )  |
| 188cf5406c8e5ef58da356b209b2c30eff1130ce | g0tmi1k | 2015-09-18 10:19:40+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -2,7 +2,7 @@
 
 if( isset( $_GET[ 'Login' ] ) ) {
 	// Anti-CSRF
-	checkTokens( $_POST[ 'token |
| 188cf5406c8e5ef58da356b209b2c30eff1130ce | g0tmi1k | 2015-09-18 10:19:40+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -2,16 +2,23 @@
 
 if( isset( $_POST[ 'Upload' ] ) ) {
 	// Anti-CSRF
-	checkTokens( $_POST[ 't |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | MySQL.php | @@ -44,8 +44,8 @@ dvwaMessagePush( "'users' table was created." );
 // Insert some data into users
 |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | dvwaPage.inc.php | @@ -9,7 +9,6 @@ session_start(); // Creates a 'Full Path Disclosure' vuln.
 
 // Include configs
  |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | login.php | @@ -1,7 +1,6 @@
 <?php
 
 define( 'DVWA_WEB_PAGE_TO_ROOT', '' );
-
 require_once DVWA_WEB_PAGE_T |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | security.php | @@ -12,7 +12,7 @@ $page[ 'page_id' ] = 'security';
 $securityHtml = '';
 if( isset( $_POST['seclev_ |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | setup.php | @@ -11,7 +11,7 @@ $page[ 'page_id' ] = 'setup';
 
 if( isset( $_POST[ 'create_db' ] ) ) {
 	// Ant |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | index.php | @@ -50,7 +50,7 @@ $page[ 'body' ] .= "
 			<input type=\"submit\" value=\"Login\" name=\"Login\">
  |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -2,7 +2,7 @@
 
 if( isset( $_GET[ 'Login' ] ) ) {
 	// Anti-CSRF
-	checkTokens( $_POST[ 'token |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | session-input.php | @@ -1,4 +1,5 @@
 <?php
+
 define( 'DVWA_WEB_PAGE_TO_ROOT', '../../' );
 require_once DVWA_WEB_PAG |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | cookie-input.php | @@ -1,4 +1,5 @@
 <?php
+
 define( 'DVWA_WEB_PAGE_TO_ROOT', '../../' );
 require_once DVWA_WEB_PAG |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | index.php | @@ -53,7 +53,7 @@ $page[ 'body' ] .= "
 
 	<div class=\"vulnerable_code_area\">";
 if( $vulnerabil |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -2,7 +2,7 @@
 
 if( isset( $_POST[ 'Upload' ] ) ) {
 	// Anti-CSRF
-	checkTokens( $_POST[ 'tok |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | view_source.php | @@ -60,7 +60,7 @@ $page[ 'body' ] .= "
 	<br /> <br />
 
 	<form>
-		<input type=\"button\" value |
| 87c1a30a9f96490788674cd1441b2ee5c755bebb | g0tmi1k | 2015-09-20 16:31:01+01:00 | Critical | No CVE found | A07:2021 - Identification & Authentication Failures | view_source_all.php | @@ -62,7 +62,7 @@ $page[ 'body' ] .= "
 	<h3>Impossible {$vuln} Source</h3>
 	<table width='100%' b |
| 58e0cc7a622b9d263ec95a4740d850a3cc420cf1 | g0tmi1k | 2015-09-20 16:32:38+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -23,6 +23,7 @@ if( isset( $_GET[ 'Login' ] ) ) {
 	}
 	else {
 		// Login failed
+		sleep(2); |
| 58e0cc7a622b9d263ec95a4740d850a3cc420cf1 | g0tmi1k | 2015-09-20 16:32:38+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,12 +1,19 @@
 <?php
 
 if( isset( $_POST[ 'submit' ] ) ) {
-	$target = $_REQUEST[ 'ip' ];
+ |
| 9f0549b88d01d89284dd889230ff4f7f94abbfcb | g0tmi1k | 2015-09-21 18:30:18+01:00 | Critical | No CVE found | Unknown Category | MySQL.php | @@ -33,7 +33,7 @@ if( !@mysql_select_db( $_DVWA[ 'db_database' ] ) ) {
 	dvwaPageReload();
 }
 
- |
| 9f0549b88d01d89284dd889230ff4f7f94abbfcb | g0tmi1k | 2015-09-21 18:30:18+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -24,7 +24,7 @@ if( isset( $_GET[ 'Login' ] ) ) {
 
 		// Login Successful
 		$html .= "<p>Welco |
| 9f0549b88d01d89284dd889230ff4f7f94abbfcb | g0tmi1k | 2015-09-21 18:30:18+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -19,9 +19,6 @@ if( isset( $_GET[ 'Login' ] ) ) {
 	$lockout_time       = '15';
 	$account_locked |
| 9f0549b88d01d89284dd889230ff4f7f94abbfcb | g0tmi1k | 2015-09-21 18:30:18+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -15,7 +15,7 @@ if( isset( $_GET[ 'Login' ] ) ) {
 
 		// Login Successful
 		$html .= "<p>Welco |
| 9f0549b88d01d89284dd889230ff4f7f94abbfcb | g0tmi1k | 2015-09-21 18:30:18+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -19,7 +19,7 @@ if( isset( $_GET[ 'Login' ] ) ) {
 
 		// Login Successful
 		$html .= "<p>Welco |
| 3c2a9c4eacc2600b8ed1edaa7ec42798333bf77c | g0tmi1k | 2015-09-22 23:36:54+01:00 | High | No CVE found | A03:2021 - Injection | README.md | @@ -143,7 +143,7 @@ ### Troubleshooting
 </IfModule>
 ```
 
-+Q. Command execution won't work.
+ |
| 3c2a9c4eacc2600b8ed1edaa7ec42798333bf77c | g0tmi1k | 2015-09-22 23:36:54+01:00 | High | No CVE found | A03:2021 - Injection | dvwaPage.inc.php | @@ -188,7 +188,7 @@ function dvwaHtmlEcho( $pPage ) {
 	if( dvwaIsLoggedIn() ) {
 		$menuBlocks[ 'v |
| 3c2a9c4eacc2600b8ed1edaa7ec42798333bf77c | g0tmi1k | 2015-09-22 23:36:54+01:00 | High | No CVE found | A03:2021 - Injection | help.php | @@ -1,5 +1,5 @@
 <div class="body_padded">
-	<h1>Help - Command Execution</h1>
+	<h1>Help - Comman |
| 3c2a9c4eacc2600b8ed1edaa7ec42798333bf77c | g0tmi1k | 2015-09-22 23:36:54+01:00 | High | No CVE found | A03:2021 - Injection | index.php | @@ -6,7 +6,7 @@ require_once DVWA_WEB_PAGE_TO_ROOT.'dvwa/includes/dvwaPage.inc.php';
 dvwaPageStartu |
| 3c2a9c4eacc2600b8ed1edaa7ec42798333bf77c | g0tmi1k | 2015-09-22 23:36:54+01:00 | High | No CVE found | A03:2021 - Injection | view_source.php | @@ -22,7 +22,7 @@ elseif( $id == 'csrf' ) {
 	$vuln = 'CSRF';
 }
 elseif( $id == 'exec' ) {
-	$vu |
| 3c2a9c4eacc2600b8ed1edaa7ec42798333bf77c | g0tmi1k | 2015-09-22 23:36:54+01:00 | High | No CVE found | A03:2021 - Injection | view_source_all.php | @@ -36,7 +36,7 @@ elseif( $id == 'csrf' ) {
 	$vuln = 'CSRF';
 }
 elseif( $id == 'exec' ) {
-	$vu |
| 5e0982cefa6614baf7bf708642ea656c26a5be14 | g0tmi1k | 2015-09-24 16:10:32+01:00 | Critical | No CVE found | Unknown Category | index.php | @@ -54,7 +54,7 @@ $page[ 'body' ] .= "
 if( ( $hide_form ) || $_DVWA[ 'recaptcha_public_key' ] == "" |
| 5e0982cefa6614baf7bf708642ea656c26a5be14 | g0tmi1k | 2015-09-24 16:10:32+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,6 +1,6 @@
 <?php
 
-if( isset( $_POST[ 'Change' ] ) && ( $_POST[ 'step' ] == '1' ) ) {
+if( |
| 5e0982cefa6614baf7bf708642ea656c26a5be14 | g0tmi1k | 2015-09-24 16:10:32+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -1,6 +1,6 @@
 <?php
 
-if( isset( $_POST[ 'Change' ] ) && ( $_POST[ 'step' ] == '1' ) ) {
+if( |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -15,14 +15,15 @@ if( isset( $_GET[ 'Login' ] ) ) {
 	$pass = mysql_real_escape_string( $pass );
 |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -15,61 +15,74 @@ if( isset( $_GET[ 'Login' ] ) ) {
 	$pass = mysql_real_escape_string( $pass );
 |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,19 +1,22 @@
 <?php
 
 if( isset( $_GET[ 'Login' ] ) ) {
+	// Get username
 	$user = $_GET[ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -10,14 +10,15 @@ if( isset( $_GET[ 'Login' ] ) ) {
 	$pass = mysql_real_escape_string( $pass );
 |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,16 +1,20 @@
 <?php
 
 if( isset( $_POST[ 'Change' ] ) ) {
+	// Hide the CAPTCHA form
 	$hi |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -4,8 +4,10 @@ if( isset( $_POST[ 'Change' ] ) ) {
 	// Check Anti-CSRF token
 	checkToken( $_REQ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,16 +1,20 @@
 <?php
 
 if( isset( $_POST[ 'Change' ] ) && ( $_POST[ 'step' ] == '1' ) ) {
+	 |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,24 +1,30 @@
 <?php
 
 if( isset( $_POST[ 'Change' ] ) && ( $_POST[ 'step' ] == '1' ) ) {
+	 |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -4,22 +4,29 @@ if( isset( $_GET[ 'Change' ] ) ) {
 	// Check Anti-CSRF token
 	checkToken( $_REQ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -4,7 +4,7 @@ if( isset( $_GET[ 'Change' ] ) ) {
 	// Check Anti-CSRF token
 	checkToken( $_REQUE |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,22 +1,29 @@
 <?php
 
 if( isset( $_GET[ 'Change' ] ) ) {
-	// Turn requests into variables |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,28 +1,36 @@
 <?php
 
 if( isset( $_GET[ 'Change' ] ) ) {
-	// Checks the http referer heade |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | index.php | @@ -42,7 +42,7 @@ $page[ 'body' ] .= "
 			<p>
 				Enter an IP address:
 				<input type=\"text\" |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,9 +1,10 @@
 <?php
 
-if( isset( $_POST[ 'submit' ] ) ) {
+if( isset( $_POST[ 'Submit' ]  )  |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -1,9 +1,10 @@
 <?php
 
-if( isset( $_POST[ 'submit' ] ) ) {
+if( isset( $_POST[ 'Submit' ]  )  |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,17 +1,21 @@
 <?php
 
-if( isset( $_POST[ 'submit' ] ) ) {
+if( isset( $_POST[ 'Submit' ]  ) |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,25 +1,30 @@
 <?php
 
-if( isset( $_POST[ 'submit' ] ) ) {
+if( isset( $_POST[ 'Submit' ]  ) |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,8 +1,11 @@
 <?php
 
-$file = $_GET[ 'page' ]; // The page we wish to display
+// The page w |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -1,9 +1,11 @@
 <?php
 
-$file = $_GET[ 'page' ]; // The page we wish to display
+// The page w |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,5 +1,6 @@
 <?php
 
-$file = $_GET[ 'page' ]; // The page we wish to display
+// The page we |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,6 +1,7 @@
 <?php
 
-$file = $_GET[ 'page' ]; // The page we wish to display
+// The page we |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,26 +1,29 @@
 <?php
 
 if( isset( $_SESSION [ 'id' ] ) ) {
-	// Retrieve data
+	// Get inpu |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -1,23 +1,29 @@
 <?php
 
-if( isset( $_GET[ 'Submit' ] ) ) {
+if( isset( $_GET[ 'Submit' ]  ) ) |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,24 +1,29 @@
 <?php
 
-if( isset( $_REQUEST[ 'Submit' ] ) ) {
-	// Retrieve data
+if( isset |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,25 +1,30 @@
 <?php
 
-if( isset( $_POST[ 'Submit' ] ) ) {
-	// Retrieve data
+if( isset( $ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,23 +1,33 @@
 <?php
 
 if( isset( $_COOKIE[ 'id' ] ) ) {
-	// Retrieve data
+	// Get input |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -1,19 +1,27 @@
 <?php
 
-if( isset( $_GET[ 'Submit' ] ) ) {
+if( isset( $_GET[ 'Submit' ]  ) ) |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,20 +1,28 @@
 <?php
 
-if( isset( $_GET[ 'Submit' ] ) ) {
-	// Retrieve data
+if( isset( $_ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,21 +1,26 @@
 <?php
 
-if( isset( $_POST[ 'Submit' ] ) ) {
-	// Retrieve data
+if( isset( $ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,29 +1,35 @@
 <?php
 
 if( isset( $_POST[ 'Upload' ] ) ) {
-	$target_path   = DVWA_WEB_PAGE_ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -4,24 +4,28 @@ if( isset( $_POST[ 'Upload' ] ) ) {
 	// Check Anti-CSRF token
 	checkToken( $_RE |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,17 +1,19 @@
 <?php
 
 if( isset( $_POST[ 'Upload' ] ) ) {
-	$target_path = DVWA_WEB_PAGE_TO |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,27 +1,33 @@
 <?php
 
 if( isset( $_POST[ 'Upload' ] ) ) {
-	$target_path   = DVWA_WEB_PAGE_ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,9 +1,12 @@
 <?php
 
+// Is there any input?
 if( array_key_exists( "name", $_GET ) && $_GET |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -1,12 +1,15 @@
 <?php
 
+// Is there any input?
 if( array_key_exists( "name", $_GET ) && $_GE |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,9 +1,9 @@
 <?php
 
+// Is there any input?
 if( array_key_exists( "name", $_GET ) && $_GET[ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,9 +1,12 @@
 <?php
 
+// Is there any input?
 if( array_key_exists( "name", $_GET ) && $_GET |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | high.php | @@ -1,11 +1,12 @@
 <?php
 
 if( isset( $_POST[ 'btnSign' ] ) ) {
+	// Get input
 	$message = tri |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | impossible.php | @@ -4,6 +4,7 @@ if( isset( $_POST[ 'btnSign' ] ) ) {
 	// Check Anti-CSRF token
 	checkToken( $_REQ |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,6 +1,7 @@
 <?php
 
 if( isset( $_POST[ 'btnSign' ] ) ) {
+	// Get input
 	$message = trim( |
| d41ae43d18aa0eb128ca324f8ebd4e2a9ff210ae | g0tmi1k | 2015-09-27 19:15:44+01:00 | Critical | No CVE found | Unknown Category | medium.php | @@ -1,11 +1,12 @@
 <?php
 
 if( isset( $_POST[ 'btnSign' ] ) ) {
+	// Get input
 	$message = tri |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | MySQL.php | @@ -6,7 +6,7 @@ This file contains all of the code to setup the initial MySQL database. (setup.p
 
 |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | dvwaPage.inc.php | @@ -458,8 +458,8 @@ function dvwaDatabaseConnect() {
 	global $db;
 
 	if( $DBMS == 'MySQL' ) {
- |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | login.php | @@ -13,26 +13,26 @@ if( isset( $_POST[ 'Login' ] ) ) {
 
 	$user = $_POST[ 'username' ];
 	$user = |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -7,19 +7,19 @@ if( isset( $_GET[ 'Login' ] ) ) {
 	// Sanitise username input
 	$user = $_GET[ ' |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | impossible.php | @@ -7,12 +7,12 @@ if( isset( $_POST[ 'Login' ] ) ) {
 	// Sanitise username input
 	$user = $_POST[ |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -10,9 +10,9 @@ if( isset( $_GET[ 'Login' ] ) ) {
 
 	// Check the database
 	$query  = "SELECT  |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -3,18 +3,18 @@
 if( isset( $_GET[ 'Login' ] ) ) {
 	// Sanitise username input
 	$user = $_GET[ |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -24,12 +24,12 @@ if( isset( $_POST[ 'Change' ] ) ) {
 	else {
 		// CAPTCHA was correct. Do both |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | impossible.php | @@ -10,17 +10,17 @@ if( isset( $_POST[ 'Change' ] ) ) {
 	// Get input
 	$pass_new  = $_POST[ 'pass |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -53,12 +53,12 @@ if( isset( $_POST[ 'Change' ] ) && ( $_POST[ 'step' ] == '2' ) ) {
 	// Check to |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -61,12 +61,12 @@ if( isset( $_POST[ 'Change' ] ) && ( $_POST[ 'step' ] == '2' ) ) {
 	// Check to |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -11,12 +11,12 @@ if( isset( $_GET[ 'Change' ] ) ) {
 	// Do the passwords match?
 	if( $pass_new |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | impossible.php | @@ -11,7 +11,7 @@ if( isset( $_GET[ 'Change' ] ) ) {
 
 	// Sanitise current password input
 	$pas |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -8,12 +8,12 @@ if( isset( $_GET[ 'Change' ] ) ) {
 	// Do the passwords match?
 	if( $pass_new = |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -10,12 +10,12 @@ if( isset( $_GET[ 'Change' ] ) ) {
 		// Do the passwords match?
 		if( $pass_n |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | index.php | @@ -61,7 +61,7 @@ else {
 	if( $vulnerabilityFile == 'medium.php' ) {
 		$page[ 'body' ] .= "\n				 |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -6,10 +6,10 @@ if( isset( $_SESSION [ 'id' ] ) ) {
 
 	// Check database
 	$query  = "SELECT fi |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -6,10 +6,10 @@ if( isset( $_REQUEST[ 'Submit' ] ) ) {
 
 	// Check database
 	$query  = "SELECT |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -3,14 +3,14 @@
 if( isset( $_POST[ 'Submit' ] ) ) {
 	// Get input
 	$id = $_POST[ 'id' ];
-	$ |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | index.php | @@ -61,7 +61,7 @@ else {
 	if( $vulnerabilityFile == 'medium.php' ) {
 		$page[ 'body' ] .= "\n				 |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -6,10 +6,10 @@ if( isset( $_COOKIE[ 'id' ] ) ) {
 
 	// Check database
 	$getid  = "SELECT firs |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -6,10 +6,10 @@ if( isset( $_GET[ 'Submit' ] ) ) {
 
 	// Check database
 	$getid  = "SELECT fir |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -3,14 +3,14 @@
 if( isset( $_POST[ 'Submit' ]  ) ) {
 	// Get input
 	$id = $_POST[ 'id' ];
-	 |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -7,16 +7,16 @@ if( isset( $_POST[ 'btnSign' ] ) ) {
 
 	// Sanitize message input
 	$message =  |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | impossible.php | @@ -10,12 +10,12 @@ if( isset( $_POST[ 'btnSign' ] ) ) {
 
 	// Sanitize message input
 	$message  |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -7,14 +7,14 @@ if( isset( $_POST[ 'btnSign' ] ) ) {
 
 	// Sanitize message input
 	$message =  |
| d185522a990df19485233b1351b8c09fe5b30daf | Diego Blanco | 2016-02-23 16:53:01+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -7,16 +7,16 @@ if( isset( $_POST[ 'btnSign' ] ) ) {
 
 	// Sanitize message input
 	$message =  |
| 45eb7da35a8f12f43f9fe5903d30cc4c3fdf60c6 | Nick Armstrong | 2016-08-24 18:45:08+10:00 | Critical | No CVE found | A03:2021 - Injection | index.php | @@ -62,7 +62,7 @@ else {
 		$page[ 'body' ] .= "\n				<select name=\"id\">";
 		$query  = "SELECT C |
| 45eb7da35a8f12f43f9fe5903d30cc4c3fdf60c6 | Nick Armstrong | 2016-08-24 18:45:08+10:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -9,18 +9,13 @@ if( isset( $_SESSION [ 'id' ] ) ) {
 	$result = mysqli_query($GLOBALS["___mysqli_s |
| 45eb7da35a8f12f43f9fe5903d30cc4c3fdf60c6 | Nick Armstrong | 2016-08-24 18:45:08+10:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -9,18 +9,13 @@ if( isset( $_REQUEST[ 'Submit' ] ) ) {
 	$result = mysqli_query($GLOBALS["___mysql |
| 45eb7da35a8f12f43f9fe5903d30cc4c3fdf60c6 | Nick Armstrong | 2016-08-24 18:45:08+10:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -10,18 +10,13 @@ if( isset( $_POST[ 'Submit' ] ) ) {
 	$result = mysqli_query($GLOBALS["___mysqli |
| b4e5c6f6fda801681d2883bd4645a2dd8a4f4e4b | Nick Armstrong | 2016-08-24 18:45:27+10:00 | Critical | No CVE found | A03:2021 - Injection | index.php | @@ -62,7 +62,7 @@ else {
 		$page[ 'body' ] .= "\n				<select name=\"id\">";
 		$query  = "SELECT C |
| ccff8f650bf1c1ce4ad166f8bf0271444b2f00f7 | Nick Armstrong | 2016-08-24 18:45:48+10:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -21,7 +21,8 @@ if( isset( $_GET[ 'Login' ] ) ) {
 
 	if( $result && mysqli_num_rows( $result ) = |
| ccff8f650bf1c1ce4ad166f8bf0271444b2f00f7 | Nick Armstrong | 2016-08-24 18:45:48+10:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -14,7 +14,8 @@ if( isset( $_GET[ 'Login' ] ) ) {
 
 	if( $result && mysqli_num_rows( $result ) = |
| ccff8f650bf1c1ce4ad166f8bf0271444b2f00f7 | Nick Armstrong | 2016-08-24 18:45:48+10:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -16,7 +16,8 @@ if( isset( $_GET[ 'Login' ] ) ) {
 
 	if( $result && mysqli_num_rows( $result ) = |
| c93b7715c8d81d21a06814b05fe2d065baac3c67 | Michael Hanon | 2016-10-28 20:02:32-07:00 | Critical | No CVE found | A03:2021 - Injection | dvwaPage.inc.php | @@ -549,7 +549,7 @@ $phpMagicQuotes   = 'PHP function magic_quotes_gpc: <span class="' . ( ini_get(
 |
| 3671ae793b6ba42a0f166c09d472557cf91d56ae | Michael Hanon | 2016-10-28 20:13:15-07:00 | Critical | No CVE found | A03:2021 - Injection | dvwaPage.inc.php | @@ -549,7 +549,7 @@ $phpMagicQuotes   = 'PHP function magic_quotes_gpc: <span class="' . ( ini_get(
 |
| 80f682e4afdaea07d9aa4465d74e4061bc20dbfd | Robin Wood | 2017-04-12 04:30:04+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -6,7 +6,7 @@ if( isset( $_SESSION [ 'id' ] ) ) {
 
 	// Check database
 	$query  = "SELECT firs |
| 80f682e4afdaea07d9aa4465d74e4061bc20dbfd | Robin Wood | 2017-04-12 04:30:04+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -6,7 +6,7 @@ if( isset( $_REQUEST[ 'Submit' ] ) ) {
 
 	// Check database
 	$query  = "SELECT f |
| 80f682e4afdaea07d9aa4465d74e4061bc20dbfd | Robin Wood | 2017-04-12 04:30:04+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -3,11 +3,11 @@
 if( isset( $_POST[ 'Submit' ] ) ) {
 	// Get input
 	$id = $_POST[ 'id' ];
-	$ |
| 965c92b63e7caef953a503b1887be75420e4c768 | Robin Wood | 2017-04-17 22:37:22+01:00 | Critical | No CVE found | A03:2021 - Injection | index.php | @@ -60,11 +60,8 @@ else {
 				User ID:";
 	if( $vulnerabilityFile == 'medium.php' ) {
 		$page[ ' |
| 965c92b63e7caef953a503b1887be75420e4c768 | Robin Wood | 2017-04-17 22:37:22+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -6,7 +6,7 @@ if( isset( $_SESSION [ 'id' ] ) ) {
 
 	// Check database
 	$query  = "SELECT firs |
| 965c92b63e7caef953a503b1887be75420e4c768 | Robin Wood | 2017-04-17 22:37:22+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -6,7 +6,7 @@ if( isset( $_REQUEST[ 'Submit' ] ) ) {
 
 	// Check database
 	$query  = "SELECT f |
| 965c92b63e7caef953a503b1887be75420e4c768 | Robin Wood | 2017-04-17 22:37:22+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -3,11 +3,11 @@
 if( isset( $_POST[ 'Submit' ] ) ) {
 	// Get input
 	$id = $_POST[ 'id' ];
-	$ |
| 4fb32fb9276181b041ca24eba42df506ce804de1 | Steve Pinkham | 2017-05-08 18:25:52-04:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | index.php | @@ -45,7 +45,7 @@ $page[ 'body' ] = <<<EOF
  
  		<p>Please choose a language:</p>
 
-		<form nam |
| 086d116b19e3762f1c8fab952c2b155f60ff6995 | Robin Wood | 2017-05-12 21:31:56+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -6,7 +6,7 @@ if( isset( $_SESSION [ 'id' ] ) ) {
 
 	// Check database
 	$query  = "SELECT firs |
| 086d116b19e3762f1c8fab952c2b155f60ff6995 | Robin Wood | 2017-05-12 21:31:56+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -4,9 +4,12 @@ if( isset( $_REQUEST[ 'Submit' ] ) ) {
 	// Get input
 	$id = $_REQUEST[ 'id' ];
 |
| 086d116b19e3762f1c8fab952c2b155f60ff6995 | Robin Wood | 2017-05-12 21:31:56+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -3,11 +3,11 @@
 if( isset( $_POST[ 'Submit' ] ) ) {
 	// Get input
 	$id = $_POST[ 'id' ];
-	$ |
| 6b00d1bf42f2ac31616f546f60ac3d8abc28bd1c | Robin Wood | 2017-11-03 17:50:22+00:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | high.php | @@ -1,5 +1,7 @@
 <?php
 
+header ("X-XSS-Protection: 0");
+
 // Is there any input?
 if( array_ |
| 6b00d1bf42f2ac31616f546f60ac3d8abc28bd1c | Robin Wood | 2017-11-03 17:50:22+00:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | low.php | @@ -1,5 +1,7 @@
 <?php
 
+header ("X-XSS-Protection: 0");
+
 // Is there any input?
 if( array_ |
| 6b00d1bf42f2ac31616f546f60ac3d8abc28bd1c | Robin Wood | 2017-11-03 17:50:22+00:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | medium.php | @@ -1,5 +1,7 @@
 <?php
 
+header ("X-XSS-Protection: 0");
+
 // Is there any input?
 if( array_ |
| dc492b983803de66825b24d665624aa44c8d9a22 | Michael Bailey | 2017-12-07 02:08:50-05:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | README.md | @@ -37,6 +37,8 @@ ## License
 ## Download and install as a docker container
 - [dockerhub page](htt |
| 54574c839dd272550f261c84d72dd91ca78bf4dc | Shaunak Sontakke | 2020-05-20 23:52:52-06:00 | Critical | No CVE found | A03:2021 - Injection | MySQL.php | @@ -11,7 +11,7 @@ if( !defined( 'DVWA_WEB_PAGE_TO_ROOT' ) ) {
 }
 
 if( !@($GLOBALS["___mysqli_sto |
| 1c2c645809b70b2db825552ddb0db1bbe2fa83a8 | kevin | 2020-09-12 13:32:27+07:00 | Critical | No CVE found | Unknown Category | help.php | @@ -18,7 +18,7 @@
 
 		<h3>Low Level</h3>
 		<p>Examine the policy to find all the sources that ca |
| 1c2c645809b70b2db825552ddb0db1bbe2fa83a8 | kevin | 2020-09-12 13:32:27+07:00 | Critical | No CVE found | Unknown Category | low.php | @@ -1,9 +1,10 @@
 <?php
 
-$headerCSP = "Content-Security-Policy: script-src 'self' https://pastebin |
| 8421018f3581b70559092b808f983652c5b1d4a2 | Robin Wood | 2020-09-15 09:34:39+01:00 | Critical | No CVE found | Unknown Category | index.php | @@ -57,7 +57,7 @@ $page[ 'body' ] .= "
 
 	<h2>More Information</h2>
 	<ul>
-		<li>" . dvwaExtern |
| cabfbc478fe89c0d1db33a2e86b947afab80c197 | Robin Wood | 2021-08-11 22:32:03+01:00 | Critical | No CVE found | A03:2021 - Injection | create_sqlite_db.sql | @@ -0,0 +1,25 @@
+CREATE TABLE `users` (
+`user_id` int NOT NULL,
+`first_name` text DEFAULT NULL,
+ |
| cabfbc478fe89c0d1db33a2e86b947afab80c197 | Robin Wood | 2021-08-11 22:32:03+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -4,21 +4,45 @@ if( isset( $_REQUEST[ 'Submit' ] ) ) {
 	// Get input
 	$id = $_REQUEST[ 'id' ]; |
| cabfbc478fe89c0d1db33a2e86b947afab80c197 | Robin Wood | 2021-08-11 22:32:03+01:00 | Critical | No CVE found | A03:2021 - Injection | sqli.db | Binary files /dev/null and b/vulnerabilities/sqli/source/sqli.db differ
 |
| 459bcc3ddbac8d5edf20a504073791a867eb7341 | Robin Wood | 2021-09-07 22:40:42+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -4,21 +4,50 @@ if( isset( $_SESSION [ 'id' ] ) ) {
 	// Get input
 	$id = $_SESSION[ 'id' ];
  |
| 459bcc3ddbac8d5edf20a504073791a867eb7341 | Robin Wood | 2021-09-07 22:40:42+01:00 | Critical | No CVE found | A03:2021 - Injection | impossible.php | @@ -9,20 +9,52 @@ if( isset( $_GET[ 'Submit' ] ) ) {
 
 	// Was a number entered?
 	if(is_numeric( |
| 459bcc3ddbac8d5edf20a504073791a867eb7341 | Robin Wood | 2021-09-07 22:40:42+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -23,6 +23,28 @@ if( isset( $_POST[ 'Submit' ] ) ) {
 			break;
 		case SQLITE:
 			global $sqli |
| 13d8b636959ed096dcb634dab9a886b889b8a324 | Robin Wood | 2021-10-07 21:06:27+01:00 | Critical | No CVE found | A03:2021 - Injection | high.php | @@ -3,14 +3,39 @@
 if( isset( $_COOKIE[ 'id' ] ) ) {
 	// Get input
 	$id = $_COOKIE[ 'id' ];
+	$ |
| 6b33c820410d3bd1198bfd42b5e6a19e7dca1436 | Robin Wood | 2021-10-07 21:14:45+01:00 | Critical | No CVE found | A03:2021 - Injection | low.php | @@ -3,18 +3,41 @@
 if( isset( $_GET[ 'Submit' ] ) ) {
 	// Get input
 	$id = $_GET[ 'id' ];
+	$ex |
| b2cbb3b42131396c3b512530f60bf7461f87c53e | Robin Wood | 2021-10-07 21:21:28+01:00 | Critical | No CVE found | A03:2021 - Injection | medium.php | @@ -3,24 +3,45 @@
 if( isset( $_POST[ 'Submit' ]  ) ) {
 	// Get input
 	$id = $_POST[ 'id' ];
-	 |
| 27f744f671fe7c5ae588a9c3748c63fbf8c44845 | Robin Wood | 2021-10-28 22:38:16+01:00 | Critical | No CVE found | A03:2021 - Injection | README.md | @@ -93,6 +93,8 @@ ### Database Setup
 The variables are set to the following by default:
 
 ```php
+ |
| c2763a1f0159069e4b5d005029dfe33e595aa57f | Robin Wood | 2021-10-27 23:21:18+01:00 | Critical | No CVE found | A03:2021 - Injection | create_sqlite_db.sql | @@ -18,10 +18,10 @@ PRIMARY KEY (`comment_id`)
 );
 
 
-insert into users values ('1','admin','admin |
| c2763a1f0159069e4b5d005029dfe33e595aa57f | Robin Wood | 2021-10-27 23:21:18+01:00 | Critical | No CVE found | A03:2021 - Injection | sqli.db.dist | Binary files /dev/null and b/database/sqli.db.dist differ
 |
| 87642b94d96bcfc762ee49c75a1ee9994c0f6cad | Robin Wood | 2023-02-27 14:47:35+00:00 | High | No CVE found | A07:2021 - Identification & Authentication Failures | README.md | @@ -372,7 +372,7 @@ ### Why can't the database connect on CentOS?
 setsebool -P httpd_can_network_co |
| b3f84d0835a266d0edc092c9adba462dfc2b6d67 | ranemirusG | 2024-04-24 12:12:48-03:00 | Critical | No CVE found | Unknown Category | main.css | @@ -163,9 +163,14 @@ div#main_menu li {
 div#main_menu li a {
 	color: #000000;
 	text-decoration: |
| 6e41e1d9ed397fc63bc8e301d0a9c96c6572033c | Robin Wood | 2024-10-16 10:20:29+01:00 | Critical | No CVE found | Unknown Category | GenericController.php | @@ -17,6 +17,12 @@ class GenericController
 		$this->command = $command;
 	}
 
+	private function op |
| 6e41e1d9ed397fc63bc8e301d0a9c96c6572033c | Robin Wood | 2024-10-16 10:20:29+01:00 | Critical | No CVE found | Unknown Category | HealthController.php | @@ -18,9 +18,54 @@ class HealthController
 		$this->command = $command;
 	}
 
+    #[OAT\Post(
+		ta |
| 6e41e1d9ed397fc63bc8e301d0a9c96c6572033c | Robin Wood | 2024-10-16 10:20:29+01:00 | Critical | No CVE found | Unknown Category | UserController.php | @@ -59,7 +59,7 @@ class UserController
 
     #[OAT\Get(
 		tags: ["user"],
-        path: '/vulnera |
