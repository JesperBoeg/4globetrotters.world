<?php
$nimbus_title = the_title('','',false);
if (empty($nimbus_title)) {
?>Post ID <?php
the_ID();
} else {
    the_title();
}
?>