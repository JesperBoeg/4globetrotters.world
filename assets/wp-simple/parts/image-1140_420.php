<?php
if (has_post_thumbnail()) {
    the_post_thumbnail('nimbus_1140_420', array('class' => 'nimbus_1140_420 img-responsive'));
} else {
    if (nimbus_get_option('reminder_images') == "on" ) {
    ?>
        <img src="<?php echo get_template_directory_uri(); ?>/images/preview/simple_1140x420_<?php echo rand(1,3); ?>.jpg" class="nimbus_1140_420 img-responsive" alt="<?php the_title(); ?>" />
    <?php
    }
}
?>