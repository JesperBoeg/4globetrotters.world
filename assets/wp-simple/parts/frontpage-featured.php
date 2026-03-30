<?php
$nimbus_left_featured = nimbus_get_option('nimbus_left_featured');
$nimbus_center_left_featured = nimbus_get_option('nimbus_center_left_featured');
$nimbus_center_right_featured = nimbus_get_option('nimbus_center_right_featured');
$nimbus_right_featured = nimbus_get_option('nimbus_right_featured');
$nimbus_featured = array(
    'nimbus_left_featured'             =>  $nimbus_left_featured,
    'nimbus_center_left_featured'      =>  $nimbus_center_left_featured,
    'nimbus_center_right_featured'     =>  $nimbus_center_right_featured,
    'nimbus_right_featured'            =>  $nimbus_right_featured,
    );

if (!is_paged()) {
?>
    <div id="frontpage_featured_row">
        <div class="container">
            <div class="row">
                <?php
                foreach ($nimbus_featured as $key => $featured) {
                ?>
                    <div id="<?php echo $key; ?>" class="col-sm-3 featured">
                        <?php
                        if (!empty($featured)) {
                            $original_query = $wp_query;
                            $wp_query = null;
                            $wp_query = new WP_Query(array('page_id' => $featured, 'posts_per_page' => 1, 'post__not_in' => get_option( 'sticky_posts' )));
                            if (have_posts()) :
                                while (have_posts()) :
                                    the_post();
                                    get_template_part( 'parts/content', 'frontpage_featured');
                                endwhile;
                                else:
                                    get_template_part( 'parts/error', 'no_results');
                            endif;
                            $wp_query = null;
                            $wp_query = $original_query;
                            wp_reset_postdata();
                            unset($i);
                        }
                        ?>
                    </div>
                <?php
                }
                ?>
            </div>
        </div>
    </div>
<?php
}
?>