<div id="page_content_row">
    <div class="container">
        <div class="row">
            <div class="col-md-8 editable">
                <div>
                    <h2>Pages</h2>
                    <ul>
                    <?php wp_list_pages('title_li='); ?>
                    </ul>
                    <div class="clear25"></div>
                    <h2>Posts</h2>
                    <ul>
                        <?php
                        $original_query = $wp_query;
                        $wp_query = null;
                        $wp_query = new WP_Query(array("post_type" => array('post'), "posts_per_page" => "-1"));
                        if (have_posts()) {
                            while (have_posts()) {
                                the_post();
                                ?>
                                <li><a href="<?php the_permalink(); ?>"><?php get_template_part( 'parts/title', 'post'); ?></a></li>
                            <?php
                            }
                        } else {
                            get_template_part( 'parts/error', 'no_results');
                        }
                        $wp_query = null;
                        $wp_query = $original_query;
                        wp_reset_postdata();
                        ?>
                    </ul>
                </div>
            </div>
            <?php
            get_sidebar();
            ?>
        </div>
    </div>
</div>

