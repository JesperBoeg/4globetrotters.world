<?php
$nimbus_posts_on_home = nimbus_get_option('nimbus_posts_on_home');
?>

<div id="frontpage_blog_row">
    <div class="container">
        <div class="row">
            <div class="col-md-8 editable fp_blog_feature">
                <div>
                    <?php
                    // look for latest post set to featured. If none, then use latest post.
                    global $more;
                    $more = 0;
                    $original_query = $wp_query;
                    $wp_query = null;
                    $wp_query = new WP_Query(array('posts_per_page' => 1, 'meta_key' => 'featured_post', 'meta_value' => 'true', 'post__not_in' => get_option( 'sticky_posts' )));
                    if ($wp_query->have_posts()) {
                    } else {
                        $wp_query = null;
                        $wp_query = new WP_Query(array('posts_per_page' => 1, 'post__not_in' => get_option( 'sticky_posts' )));
                    }
                    // display post
                    if (have_posts()) {
                        while (have_posts()) {
                            the_post();
                            if (empty($nimbus_posts_on_home)) {
                                continue;
                            }
                            $nimbus_feature_id = $post->ID;
                            get_template_part( 'parts/blog', 'featured');
                        }
                    } else {
                        // not in use unless conditions above are revised
                        // get_template_part( 'parts/error', 'no_results');
                    }
                    $wp_query = null;
                    $wp_query = $original_query;
                    wp_reset_postdata();
                    ?>
                </div>
            </div>
            <div class="col-md-4">
                <?php
                $original_query = $wp_query;
                $wp_query = null;
                $wp_query = new WP_Query(array('posts_per_page' => nimbus_get_option('nimbus_posts_on_home')));
                if (have_posts()) {
                    while (have_posts()) {
                        the_post();
                        if (empty($nimbus_posts_on_home)) {
                            continue;
                        }
                        // if no posts
                        if ((isset($nimbus_feature_id)) && ($wp_query->post_count == 1)) {
                            // if showing example content
                            if (nimbus_get_option('nimbus_example_content') == "on") {
                                $i = 1;
                                while ($i <= nimbus_get_option('nimbus_posts_on_home')) {
                                    get_template_part( 'parts/example', 'blog_small_content');
                                    $i++;
                                }
                            }
                        }
                        // skip featured from left column
                        if (isset($nimbus_feature_id)) {
                            if ($post->ID == $nimbus_feature_id) {
                                continue;
                            }
                        }
                        // display post if avalible
                        get_template_part( 'parts/blog', 'small_content');
                    }
                } else {
                    get_template_part( 'parts/error', 'no_results');
                }
                $wp_query = null;
                unset($nimbus_feature_id);
                $wp_query = $original_query;
                wp_reset_postdata();
                ?>
            </div>
        </div>
    </div>
</div>

