<?php
global $post;

// set variables
    $nimbus_banner_option = nimbus_get_option('nimbus_banner_option');
    $nimbus_full_width_banner_url = nimbus_get_option('nimbus_full_width_banner');
    if (empty($nimbus_full_width_banner_url)) {
        $nimbus_full_width_banner_url = get_template_directory_uri() . '/images/preview/crater-lake.jpg';
    }


// Do frontpage banner options
if (is_front_page() && !is_paged()) {

    // Full width image with fixed positioning
    if ($nimbus_banner_option == 'image_full_fixed') {
    ?>
        <div id="fixed_banner" class="">
            <img src="<?php echo $nimbus_full_width_banner_url; ?>" class="img-responsive visible-xs">
            <?php
            get_template_part( 'parts/banner', 'full_content');
            ?>
        </div>
    <?php

    // Content width banner
    } else if ($nimbus_banner_option == 'image_content_width') {
    ?>
        <div class="container">
            <?php
            get_template_part( 'parts/image', '1140_420');
            ?>
        </div>
    <?php
    }

// Not on frontpage, do standard layout
} else {
?>
    <div class="container">
        <?php
        get_template_part( 'parts/logo');
        ?>
    </div>
<?php
}
?>