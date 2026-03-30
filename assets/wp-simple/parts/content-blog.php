<div id="blog_content_row">
    <div class="container">
        <div class="row">
            <div class="col-md-8 editable">
                <div>
                    <?php

                    // Title on some archive views
                    get_template_part( 'parts/title', 'archive');

                    // display featured sometimes
                    if (!is_paged() && is_home()) {
                        $original_query = $wp_query;
                        $wp_query = null;
                        $wp_query = new WP_Query(array('posts_per_page' => 1, 'meta_key' => 'featured_post', 'meta_value' => 'true', 'post__not_in' => get_option( 'sticky_posts' )));
                        if ($wp_query->have_posts()) {
                        } else {
                            $wp_query = null;
                            $wp_query = new WP_Query(array('posts_per_page' => 1, 'post__not_in' => get_option( 'sticky_posts' )));
                        }
                        if (have_posts()) {
                            while (have_posts()) {
                                the_post();
                                $nimbus_feature_id = $post->ID;
                                get_template_part( 'parts/blog', 'featured');
                            }
                        } else {
                            // get_template_part( 'parts/error', 'no_results');
                        }
                        $wp_query = null;
                        $wp_query = $original_query;
                        wp_reset_postdata();
                    }

                    // display author stuff here
                    if (is_author()) {
                        get_template_part( 'parts/bio');
                    }

                    // display posts in columns
                    $posts_per_page = nimbus_get_option('posts_on_blog');
                    $post_count = $wp_query->post_count;
                    if ($posts_per_page > $post_count) {
                        $posts_per_page = $post_count;
                    }
                    $posts_per_row = ceil($posts_per_page / 2);
                    $i = 1;
                    if (have_posts()) {
                        ?>
                        <div class="row">
                            <div class="col-md-6 left_blog_column">
                                <?php
                                while (have_posts()) {
                                    the_post();
                                    if (isset($nimbus_feature_id)) {
                                        if ($post->ID == $nimbus_feature_id) {
                                            continue;
                                        }
                                    }
                                    if ($i == ($posts_per_row + 1)) {
                                        echo "</div><div class='col-md-6 right_blog_column'>";
                                    }
                                    get_template_part( 'parts/blog', 'small_content');
                                    $i++;
                                }
                                ?>
                            </div>
                        </div>
                        <?php
                        get_template_part( 'parts/blog', 'pagination');
                    } else {
                            get_template_part( 'parts/error', 'no_results');
                    }
                    ?>
                </div>
            </div>
            <?php

            // display sidebar.php unless on frontpage, then used embeded as below
            if (is_front_page()) {
                echo "<div class='col-md-4 sidebar sidebar_editable'>";
                if (is_active_sidebar( "sidebar_blog" )) {
                    dynamic_sidebar( "sidebar_blog" );
                } else {
                    get_template_part( 'parts/sidebar', 'example_widgets');
                }
                echo "</div>";
            } else {
                get_sidebar();
            }
            ?>
        </div>
    </div>
</div>

