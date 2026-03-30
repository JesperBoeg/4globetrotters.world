<?php
get_header();
if(nimbus_get_option('nimbus_fp_content_pos') == 'above') {
    get_template_part( 'parts/frontpage', 'content');
}
if (nimbus_get_option('nimbus_toggle_featured')) {
    get_template_part( 'parts/frontpage', 'featured');
}
if(nimbus_get_option('nimbus_fp_content_pos') == 'below') {
    get_template_part( 'parts/frontpage', 'content');
}
if ( 'posts' == get_option( 'show_on_front' ) ) {
    get_template_part( 'parts/content', 'blog');
} else {
    $nimbus_toggle_fp_blog = nimbus_get_option('nimbus_toggle_fp_blog');
    if (!empty($nimbus_toggle_fp_blog)) {
        get_template_part( 'parts/frontpage', 'blog');
    }
}
get_footer();
?>