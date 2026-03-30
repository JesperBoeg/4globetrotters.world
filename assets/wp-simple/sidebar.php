<div class="col-md-4 sidebar sidebar_editable">
    <?php

    // Used to constrain the sidebar content on the frontpage content row
    if (is_front_page()) {
    echo "<div>";
    }

    // Social media buttons at the top of the sidebar
    $display_social_buttons = nimbus_get_option('nimbus_display_social_buttons');
    if (!empty($display_social_buttons)) {
        get_template_part( 'parts/sidebar', 'social_media');
    }

    // set conditions to show widget areas (the frontpage blog widget area is on content-blog.php)
    global $wp_query;
    $i = 1;
    if (is_404()) {

    } else if ( is_page() || is_single()) {
        $postid = $wp_query->post->ID;
        if (trim(get_post_meta($postid, 'alt_sidebar_select', true)) != "") {
            while ($i <= 20) {
                if (trim(get_post_meta($postid, 'alt_sidebar_select', true)) == $i) {
                    if (is_active_sidebar( "sidebar_" . $i )) {
                        dynamic_sidebar( "sidebar_" . $i );
                    }
                }
                $i++;
            }
        } else if (is_front_page()) {
            if (is_active_sidebar( "sidebar_fp" )) {
                dynamic_sidebar( "sidebar_fp" );
            }
        } else if ((trim(get_post_meta($postid, 'alt_sidebar_select', true)) == "") && is_page()) {
            if (is_active_sidebar( "sidebar_pages" )) {
                dynamic_sidebar( "sidebar_pages" );
            } else {
                if (nimbus_get_option('example_widgets') == "on") {
                    get_template_part( 'parts/sidebar', 'example_widgets');
                }
            }
        } else if ((trim(get_post_meta($postid, 'alt_sidebar_select', true)) == "") && is_single()) {
            if (is_active_sidebar( "sidebar_blog" )) {
                dynamic_sidebar( "sidebar_blog" );
            } else {
                if (nimbus_get_option('example_widgets') == "on") {
                    get_template_part( 'parts/sidebar', 'example_widgets');
                }
            }
        }
    } else if ((is_home() && !is_front_page()) || is_archive()) {
        if (is_active_sidebar( "sidebar_blog" )) {
            dynamic_sidebar( "sidebar_blog" );
        } else {
            if (nimbus_get_option('example_widgets') == "on") {
                get_template_part( 'parts/sidebar', 'example_widgets');
            }
        }
    }

    // Used to constrain the sidebar content on the frontpage content row
    if (is_front_page()) {
    echo "</div>";
    }

    ?>
</div>