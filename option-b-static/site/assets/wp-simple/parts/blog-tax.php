<?php
$nimbus_post_meta_single = nimbus_get_option('nimbus_post_meta_single');
$nimbus_post_meta_blog = nimbus_get_option('nimbus_post_meta_blog');
if (has_category() || has_tag()) {
?>
    <div class="taxonomy">
        <?php
        if ((is_single() && ($nimbus_post_meta_single['categories'] == 1)) || ((is_home() || is_front_page || is_archive() || is_search) && ($nimbus_post_meta_blog['categories'] == 1))) {
            if (has_category()) {
                _e('Posted in: ', 'nimbus');
                the_category(', ');
            }
        }
        if (has_category() && has_tag()) {
            echo "<div class='clear10'></div>";
        }
        if ((is_single() && ($nimbus_post_meta_single['tags'] == 1)) || ((is_home() || is_front_page || is_archive() || is_search) && ($nimbus_post_meta_blog['tags'] == 1))) {
            if (has_tag()) {
                the_tags('Tagged: ', ', ', '');
            }
        }
        ?>
    </div>
<?php
}
?>
