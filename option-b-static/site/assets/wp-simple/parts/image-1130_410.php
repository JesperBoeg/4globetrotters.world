<?php
if (is_front_page() || is_page_template('alt_frontpage.php')) {
    $banner_class = "full_content_width_banner_border";
}
if (has_post_thumbnail()) {
    the_post_thumbnail('nimbus_1130_410', array('class' => 'nimbus_1130_410 img-responsive ' . $banner_class));
} else {
    if (nimbus_get_option('reminder_images') == "on" ) {
    ?>
        <img src="<?php echo get_template_directory_uri(); ?>/images/preview/simple_1130x410_<?php echo rand(1,3); ?>.jpg" class="nimbus_1130_410 img-responsive <?php echo $banner_class; ?>" alt="<?php the_title(); ?>" />
    <?php
    }
}

?>