<?php
$nimbus_post_meta = nimbus_get_option('nimbus_post_meta_single');
if ($nimbus_post_meta['tags'] == 1) {
    if (has_tag()) {
    ?>
        <div id="tags_wrap">
            <?php the_tags('Tagged: ', ', ', ''); ?>
        </div>
    <?php
    }
}
?>