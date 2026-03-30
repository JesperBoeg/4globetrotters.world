<?php
if (has_post_thumbnail()) {
    the_post_thumbnail('nimbus_740_420', array('class' => 'nimbus_740_420 img-responsive'));
} else {
    if ((nimbus_get_option('reminder_images') == "on") || (in_the_loop() == false) ) {
    ?>
    <img src="<?php echo get_template_directory_uri(); ?>/images/preview/simple_740x420_<?php echo rand(1,2); ?>.jpg" class="nimbus_740_420 img-responsive" alt="<?php the_title(); ?>" />
    <?php
    }
}
?>