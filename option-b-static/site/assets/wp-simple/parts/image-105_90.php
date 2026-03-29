<?php
if (has_post_thumbnail()) {
    the_post_thumbnail('nimbus_105_90', array('class' => 'nimbus_105_90'));
} else {
    if (nimbus_get_option('reminder_images') == "on"  || (in_the_loop() == false) ) {
    ?>
        <img class="nimbus_105_90" src="<?php echo get_template_directory_uri(); ?>/images/preview/simple_105x90_<?php echo rand(1,5); ?>.jpg" alt="<?php the_title(); ?>" />
    <?php
    }
}
?>