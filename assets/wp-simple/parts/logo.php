<?php
$nimbus_image_logo = trim(nimbus_get_option('nimbus_image_logo'));
$nimbus_text_logo = trim(nimbus_get_option('nimbus_text_logo'));
if (empty($nimbus_image_logo)) {
    if (!empty($nimbus_text_logo)) {
    ?>
        <h1 class="text_logo"><a href="<?php echo esc_url(home_url('/')); ?>"><?php echo $nimbus_text_logo; ?></a></h1>
    <?php
    }
} else {
?>
    <a class="" href="<?php echo esc_url(home_url('/')); ?>"><img class="image_logo" src="<?php echo $nimbus_image_logo; ?>" alt="<?php echo get_bloginfo('name', 'display'); ?>" /></a>
<?php
}
?>

