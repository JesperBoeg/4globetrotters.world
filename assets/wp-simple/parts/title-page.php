<?php
$nimbus_title = single_post_title('',false);
if (empty($nimbus_title)) {
    ?>Post ID <?php the_ID();
} else {
    single_post_title();
}
?>