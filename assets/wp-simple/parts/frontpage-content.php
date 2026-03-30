<?php
if (!is_paged()) {
?>
    <div id="frontpage_content_row">
        <div class="container">
            <?php
            // check to see if this if a page is set as frontpage in Reading Settings
            if (is_page()) {
            ?>
                <h1><?php get_template_part( 'parts/title', 'page'); ?></h1>
            <?php
            } else {
            // if not, display alt below
                if (nimbus_get_option('nimbus_example_content') == "on") {
                ?>
                    <h1><?php _e('Welcome to the Simple Theme', 'nimbus'); ?></h1>
                <?php
                }
            }
            ?>
            <div class="row">
                <div class="editable <?php if (nimbus_get_option('nimbus_fp_content_sidebar') == 'sidebar') { ?>col-md-8<?php } else { ?>col-md-12<?php } ?>">
                    <div>
                        <?php
                        // check to see if this if a page is set as frontpage in Reading Settings
                        if (is_page()) {
                            if (have_posts()) {
                                while (have_posts()) {
                                    the_post();
                                    the_content();
                                }
                            } else {
                                    get_template_part( 'parts/error', 'no_results');
                            }

                        // if not, display alt below
                        } else {
                            if (nimbus_get_option('nimbus_example_content') == "on") {
                            ?>
                                <p><?php _e('To get the most out of this theme you will want to set a static frontpage. You can do this by logging into your WordPress Dashboard >> Settings >> Reading, and selecting the option for a static page. Be sure to choose a Front Page option and a Posts Page option before you save.', 'nimbus'); ?></p>
                                <p><?php _e('If you would prefer to use the "Your Latest Posts" option that\'s fine also. You can turn off this content row in the Simple Theme options panel. Just log into your WordPress Dashbaord and look for the link to the Options Panel in the left side menu. Navigate to the Frontpage tab and look for the section titled Display Content Position. Select the option Don\'t Display Content and save your changes.', 'nimbus'); ?></p>
                            <?php
                            }
                        }
                        ?>
                    </div>
                </div>
                <?php
                if (nimbus_get_option('nimbus_fp_content_sidebar') == 'sidebar') {
                    get_sidebar();
                }
                ?>
            </div>
        </div>
    </div>
<?php
}
?>
