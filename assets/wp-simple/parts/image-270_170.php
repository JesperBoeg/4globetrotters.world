<?php
if (has_post_thumbnail()) {
    the_post_thumbnail('nimbus_270_170', array('class' => 'nimbus_270_170 img-responsive'));
} else {
    if (nimbus_get_option('reminder_images') == "on" ) {
    ?>
        <img src="<?php echo get_template_directory_uri(); ?>/images/preview/simple_270x170_<?php echo rand(1,4); ?>.jpg" class="nimbus_270_170 img-responsive" alt="<?php the_title(); ?>" />
    <?php
    }
}
?>
